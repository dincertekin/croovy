import redis
import json
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
redis_search_client = redis.Redis(host='localhost', port=6380, decode_responses=True)

def index_existing_data():
    urls = redis_client.keys('*')

    for url in urls:
        try:
            url_data = redis_client.json().get(url)
            if url_data is None:
                raw_json = redis_client.get(url)
                if raw_json:
                    url_data = json.loads(raw_json)

            if url_data is None:
                print(f"Could not retrieve data for {url}")
                continue

            if isinstance(url_data, list):
                url_data = url_data[0] if url_data else {}

            title = url_data.get('title', 'No title')
            description = url_data.get('description', 'No description')
            content = url_data.get('content', 'No content')
            score = 1.0

            print(f"Indexing: {url}")
            print(f"Title: {title}")
            print(f"Description: {description}")

            redis_search_client.execute_command('FT.ADD', 'my_index', url, score, 
                 'FIELDS', 'title', title, 'description', description, 'content', content)

        except json.JSONDecodeError as e:
            print(f"[JSON Decode Error] URL: {url}, Error: {e}")
        except Exception as e:
            print(f"[Unexpected Error in index_existing_data()] URL: {url}, Error: {e}")

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '').strip()

    if not query:
        return jsonify({'error': 'Query parameter is required and cannot be empty.'}), 400

    if len(query) < 2 or len(query) > 100:
        return jsonify({'error': 'Query must be between 2 and 100 characters.'}), 400

    sanitized_query = re.sub(r'[<>\'";()]', '', query)

    malicious_patterns = [
        r'<script>',
        r'javascript:',
        r'onerror=',
        r'alert\(',
        r'eval\b'
    ]
    
    for pattern in malicious_patterns:
        if re.search(pattern, sanitized_query, re.IGNORECASE):
            print(f"[Security Alert] Potential threat detected: {query}")
            return jsonify({'error': 'Invalid search query'}), 400

    try:
        search_results = redis_search_client.execute_command(
            'FT.SEARCH', 'my_index', sanitized_query.lower()
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

        return jsonify({
            'query': sanitized_query,
            'results': formatted_results
        }), 200

    except redis.exceptions.RedisError as e:
        print(f"[Redis Error] Query: {sanitized_query}, Error: {e}")
        return jsonify({'error': 'Database search failed'}), 500
    
    except Exception as e:
        print(f"[Unexpected Error in search()] Query: {sanitized_query}, Error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    # index_existing_data()
    app.run(debug=True)
