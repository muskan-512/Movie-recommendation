from flask import request
from routes import search_bp
from services.trie_service import build_trie
trie = build_trie()
@search_bp.route('/autocomplete', methods=['GET'])
def autocomplete():
    prefix = request.args.get('prefix', '').strip()
    if not prefix:
        return {'suggestions': []}
    suggestions = trie.autocomplete(prefix)
    return {'suggestions': suggestions}
