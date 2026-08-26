from flask import Blueprint, request, jsonify
from services.search_service import execute_search

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['POST'])
def search():
    req_data = request.get_json(silent=True) or {}
    query = req_data.get('query', '')

    result = execute_search(query)

    if "error" in result:
        return jsonify({'error': result['error']}), result['status']

    return jsonify(result['data']), 200
