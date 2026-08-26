import re
import redis
from config import Config
from services.redis_client import redis_search_client

def escape_redis_search_query(query: str) -> str:
    special_chars = r'[,.<>{}\[\]"\':;!@#$%^&*()\-+=~|/\\]'
    return re.sub(f'({special_chars})', r'\\\1', query)

def execute_search(query: str):
    sanitized_query = query.strip()

    if not (2 <= len(sanitized_query) <= 100):
        return {"error": "Query length must be between 2 and 100 characters.", "status": 400}

    malicious_patterns = [r'<script>', r'javascript:', r'onerror=', r'alert\(', r'eval\b']
    for pattern in malicious_patterns:
        if re.search(pattern, sanitized_query, re.IGNORECASE):
            return {"error": "Invalid search query.", "status": 400}

    escaped_query = escape_redis_search_query(sanitized_query)

    try:
        search_results = redis_search_client.execute_command(
            'FT.SEARCH', Config.INDEX_NAME, f"{escaped_query}*"
        )

        formatted_results = []
        for i in range(1, len(search_results), 2):
            url = search_results[i]
            fields = search_results[i + 1]

            result_dict = {}
            for j in range(0, len(fields), 2):
                result_dict[fields[j]] = fields[j + 1]

            formatted_results.append({
                'url': url,
                'title': result_dict.get('title', 'No title'),
                'description': result_dict.get('description', 'No description available'),
            })

        return {
            "data": {
                'query': sanitized_query,
                'results': formatted_results
            },
            "status": 200
        }

    except redis.exceptions.RedisError as e:
        print(f"[Redis Error] Query: {sanitized_query}, Error: {e}")
        return {"error": "Database search failed.", "status": 500}
