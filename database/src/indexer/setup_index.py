import redis

def create_search_index(host='localhost', port=6380, index_name='my_index'):
    client = redis.Redis(host=host, port=port, decode_responses=True)

    try:
        client.execute_command('FT.INFO', index_name)
        print(f"Index '{index_name}' already exists.")
    except redis.exceptions.ResponseError:
        print(f"Creating RediSearch index '{index_name}'...")
        client.execute_command(
            'FT.CREATE', index_name,
            'ON', 'JSON',
            'PREFIX', '1', 'url:',
            'SCHEMA',
            '$.title', 'AS', 'title', 'TEXT', 'WEIGHT', '5.0',
            '$.description', 'AS', 'description', 'TEXT', 'WEIGHT', '1.0',
            '$.content', 'AS', 'content', 'TEXT', 'WEIGHT', '1.0'
        )
        print("Index created successfully.")

if __name__ == "__main__":
    create_search_index()
