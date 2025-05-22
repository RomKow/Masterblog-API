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
    """
    Return all posts, optionally sorted.
    Query params:
      - sort: 'title' or 'content'
      - direction: 'asc' or 'desc'
    """
    sort_field = request.args.get('sort', type=str)
    direction = request.args.get('direction', type=str)

    posts = POSTS.copy()

    if sort_field:
        # Validate sort field
        if sort_field not in ('title', 'content'):
            return jsonify({
                "error": f"Invalid sort field '{sort_field}'. "
                         "Must be 'title' or 'content'."
            }), 400

        # Validate direction
        if direction and direction not in ('asc', 'desc'):
            return jsonify({
                "error": f"Invalid direction '{direction}'. "
                         "Must be 'asc' or 'desc'."
            }), 400

        reverse = (direction == 'desc')
        # Case-insensitive sort by the given field
        posts = sorted(
            posts,
            key=lambda post: post[sort_field].lower(),
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
        return jsonify({
            "error": f"Missing fields: {', '.join(missing)}"
        }), 400

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
            if 'title' in data and data['title']:
                post['title'] = data['title']
            if 'content' in data and data['content']:
                post['content'] = data['content']
            return jsonify(post), 200

    return jsonify({
        "error": f"Post with id {post_id} not found."
    }), 404


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by its ID."""
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({
                "message": f"Post with id {post_id} has been deleted successfully."
            }), 200

    return jsonify({
        "error": f"Post with id {post_id} not found."
    }), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search posts by title and/or content.
    Query params:
      - title: substring to search in title
      - content: substring to search in content
    """
    title_q = request.args.get('title', type=str)
    content_q = request.args.get('content', type=str)

    if not title_q and not content_q:
        return jsonify([]), 200

    title_q = title_q.lower() if title_q else None
    content_q = content_q.lower() if content_q else None

    results = [
        post for post in POSTS
        if (title_q and title_q in post['title'].lower())
        or (content_q and content_q in post['content'].lower())
    ]

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
