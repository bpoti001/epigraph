import json
import time
import logging
from typing import Dict, Any, Optional

try:
    import redis
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False

logger = logging.getLogger("epigraph.streams")

class StreamsPipeline:
    """Decoupled dual-write streaming pipeline using Redis Streams with Consumer Groups and DLQ."""

    def __init__(self, host: str = "localhost", port: int = 6379, stream_name: str = "stream:memory_ingest", dlq_name: str = "stream:memory_dlq", group_name: str = "epigraph_workers"):
        self.host = host
        self.port = port
        self.stream_name = stream_name
        self.dlq_name = dlq_name
        self.group_name = group_name
        self.client: Optional[Any] = None
        self.is_connected = False
        self._fallback_queue: list = []
        self._fallback_dlq: list = []

        if HAS_REDIS:
            try:
                self.client = redis.Redis(host=self.host, port=self.port, decode_responses=True)
                self.client.ping()
                self.is_connected = True
                self._init_group()
            except Exception as e:
                logger.warning(f"Redis Streams not reachable ({e}). Operating in in-memory fallback queue mode.")
                self.is_connected = False
        else:
            self.is_connected = False

    def _init_group(self):
        if not self.is_connected or not self.client:
            return
        try:
            self.client.xgroup_create(self.stream_name, self.group_name, id="0", mkstream=True)
        except Exception:
            # Group already exists
            pass

    def enqueue_ingestion(self, payload: Dict[str, Any]) -> str:
        """Enqueue memory ingestion event into the stream."""
        data_str = json.dumps(payload)
        if self.is_connected and self.client:
            msg_id = self.client.xadd(self.stream_name, {"payload": data_str, "retries": 0, "timestamp": time.time()})
            return msg_id
        else:
            msg_id = f"mem_msg_{len(self._fallback_queue)}"
            self._fallback_queue.append({"id": msg_id, "payload": data_str, "retries": 0, "timestamp": time.time()})
            return msg_id

    def process_batch(self, handler_fn, consumer_id: str = "worker_1", batch_size: int = 10) -> int:
        """Process stream events with automatic retry and DLQ routing on unrecoverable failures."""
        processed_count = 0

        if self.is_connected and self.client:
            try:
                messages = self.client.xreadgroup(self.group_name, consumer_id, {self.stream_name: ">"}, count=batch_size, block=1000)
            except Exception as e:
                logger.error(f"Error reading from stream: {e}")
                return 0

            if not messages:
                return 0

            for stream, msg_list in messages:
                for msg_id, fields in msg_list:
                    payload = json.loads(fields["payload"])
                    retries = int(fields.get("retries", 0))

                    try:
                        handler_fn(payload)
                        self.client.xack(self.stream_name, self.group_name, msg_id)
                        processed_count += 1
                    except Exception as err:
                        logger.error(f"Error processing {msg_id}: {err}")
                        pipe = self.client.pipeline(transaction=True)
                        if retries >= 3:
                            # Move to Dead Letter Queue atomically
                            pipe.xadd(self.dlq_name, {"failed_id": msg_id, "payload": json.dumps(payload), "error": str(err)})
                            pipe.xack(self.stream_name, self.group_name, msg_id)
                        else:
                            # Re-enqueue retry with backoff tracking atomically
                            pipe.xadd(self.stream_name, {"payload": json.dumps(payload), "retries": retries + 1, "timestamp": time.time()})
                            pipe.xack(self.stream_name, self.group_name, msg_id)
                        pipe.execute()
        else:
            batch = self._fallback_queue[:batch_size]
            self._fallback_queue = self._fallback_queue[batch_size:]
            for item in batch:
                payload = json.loads(item["payload"])
                retries = item["retries"]
                try:
                    handler_fn(payload)
                    processed_count += 1
                except Exception as err:
                    if retries >= 3:
                        self._fallback_dlq.append({**item, "error": str(err)})
                    else:
                        self._fallback_queue.append({**item, "retries": retries + 1})

        return processed_count
