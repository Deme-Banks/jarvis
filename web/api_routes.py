"""
API Routes - Additional API endpoints for web dashboard
"""
from flask import Blueprint, request, jsonify
from features.command_history_search import CommandHistorySearch
from features.sound_effects_library import SoundEffectsLibrary
from integration.plugin_marketplace import PluginMarketplace

api_bp = Blueprint('api', __name__)

# Initialize components
history_search = CommandHistorySearch()
sound_effects = SoundEffectsLibrary()
plugin_marketplace = PluginMarketplace()


@api_bp.route('/api/history/search', methods=['POST'])
def search_history():
    """Search command history"""
    data = request.json
    query = data.get('query', '')
    limit = data.get('limit', 10)
    
    results = history_search.search(query, limit)
    return jsonify({"results": results})


@api_bp.route('/api/history/recent', methods=['GET'])
def get_recent_history():
    """Get recent command history"""
    limit = request.args.get('limit', 10, type=int)
    results = history_search.get_recent(limit)
    return jsonify({"results": results})


@api_bp.route('/api/sounds/play', methods=['POST'])
def play_sound():
    """Play a sound effect"""
    data = request.json
    sound_name = data.get('sound', 'notification')
    
    success = sound_effects.play_sound(sound_name)
    return jsonify({"success": success, "sound": sound_name})


@api_bp.route('/api/plugins/search', methods=['GET'])
def search_plugins():
    """Search plugins in marketplace"""
    query = request.args.get('query', '')
    category = request.args.get('category')
    
    results = plugin_marketplace.search_plugins(query, category)
    return jsonify({"plugins": results})


@api_bp.route('/api/plugins/install', methods=['POST'])
def install_plugin():
    """Install a plugin"""
    data = request.json
    plugin_id = data.get('plugin_id')
    
    result = plugin_marketplace.install_plugin(plugin_id)
    return jsonify(result)


@api_bp.route('/api/plugins/featured', methods=['GET'])
def get_featured_plugins():
    """Get featured plugins"""
    plugins = plugin_marketplace.get_featured_plugins()
    return jsonify({"plugins": plugins})
