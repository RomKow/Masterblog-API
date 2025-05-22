# Masterblog API

**Repository:** [https://github.com/RomKow/Masterblog-API.git](https://github.com/RomKow/Masterblog-API.git)

## Description

The Masterblog API is a minimalistic CRUD application for blog posts, built with Flask. It provides endpoints to create, read, update, delete, search, and sort posts, along with interactive Swagger UI documentation.

## Features

* **GET /api/posts**: Retrieve all posts (optionally sortable by `title` or `content` in ascending or descending order). Displays the latest post first when no sort parameters are provided.
* **POST /api/posts**: Create a new post with `title` and `content`.
* **PUT /api/posts/{id}**: Update an existing post (partial updates supported).
* **DELETE /api/posts/{id}**: Delete a post by its ID.
* **GET /api/posts/search**: Search posts by `title` and/or `content` via query parameters.
* **Persistence**: All data is stored in `posts.json` to survive server restarts.
* **Swagger UI**: Interactive API documentation available at `/api/docs`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/RomKow/Masterblog-API.git
   cd Masterblog-API
   ```
2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

> **requirements.txt** should include at least:
>
> ```text
> Flask
> flask-cors
> flask-swagger-ui
> ```

## Configuration

* **`posts.json`**: The JSON file for persistent storage, located in the project root. If the file is missing, an empty list will be initialized.
* **Swagger UI**:

  * URL: `http://localhost:5002/api/docs`
  * JSON Spec: `static/masterblog.json`

## Running the Application

```bash
python backend_app.py
```

By default, the API runs at `http://localhost:5002`.

## API Endpoints

### GET /api/posts

* **Query Parameters:**

  * `sort`: `title` | `content`
  * `direction`: `asc` | `desc`
* **Description:** Returns all posts, optionally sorted. Without parameters, the list is reversed to show the latest post first.

### POST /api/posts

* **Request Body:**

  ```json
  { "title": "Your Title", "content": "Your Content" }
  ```
* **Response:** Newly created post (201 Created).

### PUT /api/posts/{id}

* **Request Body (optional):**

  ```json
  { "title": "New Title", "content": "New Content" }
  ```
* **Response:** Updated post (200 OK) or 404 if not found.

### DELETE /api/posts/{id}

* **Response:** Success message (200 OK) or 404 if not found.

### GET /api/posts/search

* **Query Parameters:**

  * `title`: string to search in post titles
  * `content`: string to search in post content
* **Response:** List of matching posts (200 OK).

## Swagger UI

Interactive API documentation:

```
http://localhost:5002/api/docs
```

## Contributing

Contributions, bug reports, and feature requests are welcome! Fork the repository, create a branch, and open a pull request.

## License

MIT License © 2025
