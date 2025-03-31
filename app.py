from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from db import init_db, get_all_projects, get_projects_by_category, get_project_by_id
import os

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Initialize database
print("Initializing database...")
init_db()
print("Database initialized")

def format_project(project):
    return {
        'id': project[0],
        'title': project[1],
        'description': project[2],
        'tech_stack': project[3],
        'github_url': project[4],
        'category': project[5],
        'created_at': project[6]
    }

@app.route('/api/projects', methods=['GET'])
def projects():
    try:
        category = request.args.get('category')
        project_id = request.args.get('id')
        
        if project_id:
            project = get_project_by_id(int(project_id))
            if project:
                return jsonify(format_project(project))
            return jsonify({'error': 'Project not found'}), 404
            
        if category:
            projects = get_projects_by_category(category)
        else:
            projects = get_all_projects()
            
        return jsonify([format_project(p) for p in projects])
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    return send_from_directory('.', path)

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Available endpoints:")
    print("- http://localhost:8000/")
    print("- http://localhost:8000/api/projects")
    print("- http://localhost:8000/api/projects?category=ml-ai")
    print("- http://localhost:8000/api/projects?id=1")
    app.run(host='0.0.0.0', port=8000, debug=True) 