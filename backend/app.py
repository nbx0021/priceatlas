import os
from flask import Flask, send_from_directory
from modules.api.routes import api_bp
from modules.services.supabase_client import supabase

# Point Flask to the folder where Docker put the React files
app = Flask(__name__, static_folder='static_react', static_url_path='/')

# Register API Blueprint
app.register_blueprint(api_bp)

@app.route('/')
def serve():
    """Serve the React App (index.html)"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    """
    Serve static files (JS, CSS, Images) from the React build.
    If file doesn't exist, return index.html (for Client-Side Routing).
    """
    file_name = path.split('/')[-1]
    dir_name = os.path.join(app.static_folder, '/'.join(path.split('/')[:-1]))
    
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Local Development
    print("🚀 PriceAtlas Server starting...")
    app.run(debug=True, port=5000)