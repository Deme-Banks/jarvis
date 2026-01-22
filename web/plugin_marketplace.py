"""
Plugin Marketplace Web UI - Discovery and installation
"""
from flask import Blueprint, render_template_string, request, jsonify
from integration.plugin_marketplace import PluginMarketplace
from plugins.plugin_system import PluginSystem

marketplace_bp = Blueprint('marketplace', __name__)

marketplace = PluginMarketplace()
plugin_system = PluginSystem()


@marketplace_bp.route('/marketplace')
def marketplace_page():
    """Plugin marketplace page"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>JARVIS Plugin Marketplace</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background: #1a1a1a;
                color: #fff;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .search-bar {
                width: 100%;
                max-width: 600px;
                margin: 20px auto;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #555;
                background: #2a2a2a;
                color: #fff;
                font-size: 16px;
            }
            .plugin-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }
            .plugin-card {
                background: #2a2a2a;
                border-radius: 8px;
                padding: 20px;
                border: 1px solid #555;
                transition: transform 0.2s;
            }
            .plugin-card:hover {
                transform: translateY(-5px);
                border-color: #4CAF50;
            }
            .plugin-header {
                display: flex;
                justify-content: space-between;
                align-items: start;
                margin-bottom: 15px;
            }
            .plugin-name {
                font-size: 20px;
                font-weight: bold;
                color: #4CAF50;
            }
            .plugin-rating {
                color: #ffd700;
            }
            .plugin-description {
                color: #ccc;
                margin-bottom: 15px;
                line-height: 1.5;
            }
            .plugin-meta {
                display: flex;
                justify-content: space-between;
                color: #888;
                font-size: 14px;
                margin-bottom: 15px;
            }
            .install-btn {
                width: 100%;
                padding: 10px;
                background: #4CAF50;
                color: #fff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                transition: background 0.2s;
            }
            .install-btn:hover {
                background: #45a049;
            }
            .install-btn.installed {
                background: #666;
                cursor: not-allowed;
            }
            .categories {
                display: flex;
                gap: 10px;
                margin: 20px 0;
                flex-wrap: wrap;
                justify-content: center;
            }
            .category-btn {
                padding: 8px 16px;
                background: #333;
                color: #fff;
                border: 1px solid #555;
                border-radius: 20px;
                cursor: pointer;
                transition: all 0.2s;
            }
            .category-btn.active {
                background: #4CAF50;
                border-color: #4CAF50;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔌 JARVIS Plugin Marketplace</h1>
            <p>Discover and install plugins to extend JARVIS</p>
        </div>
        
        <input type="text" id="searchInput" class="search-bar" placeholder="Search plugins...">
        
        <div class="categories">
            <button class="category-btn active" data-category="all">All</button>
            <button class="category-btn" data-category="integration">Integrations</button>
            <button class="category-btn" data-category="voice">Voice</button>
            <button class="category-btn" data-category="security">Security</button>
            <button class="category-btn" data-category="automation">Automation</button>
            <button class="category-btn" data-category="ai">AI</button>
        </div>
        
        <div id="pluginGrid" class="plugin-grid"></div>
        
        <script>
            let allPlugins = [];
            let currentCategory = 'all';
            
            // Load plugins
            async function loadPlugins() {
                const response = await fetch('/api/plugins/search?query=');
                const data = await response.json();
                allPlugins = data.plugins || [];
                displayPlugins(allPlugins);
            }
            
            // Display plugins
            function displayPlugins(plugins) {
                const grid = document.getElementById('pluginGrid');
                grid.innerHTML = plugins.map(plugin => `
                    <div class="plugin-card">
                        <div class="plugin-header">
                            <div class="plugin-name">${plugin.name}</div>
                            <div class="plugin-rating">⭐ ${plugin.rating || 0}</div>
                        </div>
                        <div class="plugin-description">${plugin.description || 'No description'}</div>
                        <div class="plugin-meta">
                            <span>By ${plugin.author}</span>
                            <span>${plugin.downloads || 0} downloads</span>
                        </div>
                        <button class="install-btn" onclick="installPlugin('${plugin.id}')">
                            Install
                        </button>
                    </div>
                `).join('');
            }
            
            // Search
            document.getElementById('searchInput').addEventListener('input', (e) => {
                const query = e.target.value.toLowerCase();
                const filtered = allPlugins.filter(p => 
                    p.name.toLowerCase().includes(query) ||
                    p.description.toLowerCase().includes(query)
                );
                displayPlugins(filtered);
            });
            
            // Category filter
            document.querySelectorAll('.category-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentCategory = btn.dataset.category;
                    
                    const filtered = currentCategory === 'all' 
                        ? allPlugins 
                        : allPlugins.filter(p => p.category === currentCategory);
                    displayPlugins(filtered);
                });
            });
            
            // Install plugin
            async function installPlugin(pluginId) {
                const response = await fetch('/api/plugins/install', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({plugin_id: pluginId})
                });
                const result = await response.json();
                if (result.success) {
                    alert(`Plugin '${pluginId}' installed successfully!`);
                    loadPlugins();
                } else {
                    alert(`Error: ${result.error}`);
                }
            }
            
            // Load on page load
            loadPlugins();
        </script>
    </body>
    </html>
    '''
    return html


@marketplace_bp.route('/api/plugins/featured')
def get_featured():
    """Get featured plugins"""
    plugins = marketplace.get_featured_plugins()
    return jsonify({"plugins": plugins})


@marketplace_bp.route('/api/plugins/popular')
def get_popular():
    """Get popular plugins"""
    plugins = marketplace.get_popular_plugins()
    return jsonify({"plugins": plugins})
