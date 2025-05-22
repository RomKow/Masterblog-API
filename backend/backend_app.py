from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Return all posts."""
    return jsonify(POSTS)


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

    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {"id": new_id, "title": title, "content": content}
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update an existing post. Optional 'title' and/or 'content' in JSON."""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    for post in POSTS:
        if post['id'] == post_id:
            # Only update provided fields
            if 'title' in data and data['title']:
                post['title'] = data['title']
            if 'content' in data and data['content']:
                post['content'] = data['content']
            return jsonify(post), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by its ID."""
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({
                "message": f"Post with id {post_id} has been deleted successfully."
            }), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
