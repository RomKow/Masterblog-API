import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

# Swagger UI configuration
SWAGGER_URL = "/api/docs"            # (1) Swagger UI Endpoint
API_URL     = "/static/masterblog.json"  # (2) JSON-Spec
swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Masterblog API"}  # (3) API-Name
)
app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

# Path to the JSON data file
DATA_FILE = os.path.join(os.path.dirname(__file__), 'posts.json')


def load_posts():
    """Load all posts from the JSON file. Return empty list if file not found."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # Invalid JSON
        raise


def save_posts(posts):
    """Save all posts to the JSON file."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)


@app.errorhandler(json.JSONDecodeError)
def handle_json_error(e):
    return jsonify({"error": "Data file contains invalid JSON"}), 500


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Return all posts, optionally sorted."""
    try:
        posts = load_posts()
    except json.JSONDecodeError:
        raise

    sort_field = request.args.get('sort', type=str)
    direction = request.args.get('direction', type=str)

    # If you prefer to have the latest post displayed first, enable this:
    # if not sort_field and not direction:
    #     posts.reverse()

    if sort_field:
        # Validate sort field
        if sort_field not in ('title', 'content'):
            return jsonify({
                "error": f"Invalid sort field '{sort_field}'. Must be 'title' or 'content'."
            }), 400
        # Validate direction
        if direction and direction not in ('asc', 'desc'):
            return jsonify({
                "error": f"Invalid direction '{direction}'. Must be 'asc' or 'desc'."
            }), 400

        reverse = (direction == 'desc')
        posts = sorted(
            posts,
            key=lambda p: p.get(sort_field, '').lower(),
            reverse=reverse
        )

    return jsonify(posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Add a new post. Expects JSON with 'title' and 'content'."""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    missing = []
    title = data.get('title')
    content = data.get('content')

    if not title:
        missing.append('title')
    if not content:
        missing.append('content')
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        posts = load_posts()
    except json.JSONDecodeError:
        raise

    new_id = max((p.get('id', 0) for p in posts), default=0) + 1
    new_post = {"id": new_id, "title": title, "content": content}
    posts.append(new_post)

    save_posts(posts)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update an existing post. Optional 'title' and/or 'content' in JSON."""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    try:
        posts = load_posts()
    except json.JSONDecodeError:
        raise

    for post in posts:
        if post.get('id') == post_id:
            if 'title' in data and data['title']:
                post['title'] = data['title']
            if 'content' in data and data['content']:
                post['content'] = data['content']
            save_posts(posts)
            return jsonify(post), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by its ID."""
    try:
        posts = load_posts()
    except json.JSONDecodeError:
        raise

    for post in posts:
        if post.get('id') == post_id:
            posts.remove(post)
            save_posts(posts)
            return jsonify({
                "message": f"Post with id {post_id} has been deleted successfully."
            }), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search posts by title and/or content via query params."""
    title_q = request.args.get('title', type=str)
    content_q = request.args.get('content', type=str)

    if not title_q and not content_q:
        return jsonify([]), 200

    try:
        posts = load_posts()
    except json.JSONDecodeError:
        raise

    title_q = title_q.lower() if title_q else None
    content_q = content_q.lower() if content_q else None

    results = [
        p for p in posts
        if (title_q and title_q in p.get('title', '').lower())
        or (content_q and content_q in p.get('content', '').lower())
    ]
    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
