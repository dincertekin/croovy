import redis

class RedisCrawlQueue:
    def __init__(self, host='localhost', port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
        self.queue_key = "crawler:queue"
        self.visited_key = "crawler:visited"

    def push_url(self, url: str):
        if not self.client.sismember(self.visited_key, url):
            self.client.rpush(self.queue_key, url)

    def pop_url(self):
        return self.client.lpop(self.queue_key)

    def mark_visited(self, url: str) -> bool:
        # Returns True if added, False if already present
        return bool(self.client.sadd(self.visited_key, url))

    def store_document(self, normalized_url: str, doc_data: dict):
        key = f"url:{normalized_url}"
        self.client.json().set(key, "$", doc_data)
