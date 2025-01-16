# Social Media API

## Project Overview

This project provides a RESTful API for managing social media posts, users, and comments. It is built using **FastAPI** and includes database migrations via **Alembic**. The project structure ensures modularity, scalability, and ease of maintenance.

---

## Directory Structure

### 1. `core` Directory
Contains the main entry point of the application.

- **`main.py`**: The main script to start the FastAPI application.

### 2. `api` Directory
Handles database interactions, models, and configuration.

- **`database.py`**: Manages database sessions and connections.
- **`models/model.py`**: Defines the database models for users, posts, and comments.
- **`schemas/schema.py`**: Contains data validation and serialization schemas.
- **`config.py`**: Stores configuration settings such as environment variables.

### 3. `router` Directory
Manages CRUD API endpoints for various entities.

- **`user.py`**: Handles user-related endpoints.
- **`post.py`**: Manages endpoints for creating, reading, updating, and deleting posts.
- **`comment.py`**: Handles comment-related operations.

### 4. `fetch` Directory
Contains scripts for fetching and displaying data from the database.

- **`fetch_all_user.py`**: Retrieves all users.
- **`fetch_all_post.py`**: Fetches all posts.
- **`fetch_all_comment.py`**: Retrieves all comments.
- **`fetch_post_by_user.py`**: Gets posts by a specific user.
- **`fetch_single_post_with_their_user_and_comments.py`**: Fetches a single post along with user and comments.
- **`fetch_all_post_with_their_user_and_comments.py`**: Fetches all posts along with their user and associated comments.

### 5. `exception` Directory
Handles custom exceptions used throughout the project.

- **`exceptions.py`**: Defines application-specific exceptions.

### 6. `alembic` Directory
Handles database schema migrations.

- **`versions`**: Contains migration scripts.
- **`env.py`**: Configuration for Alembic migrations.

---

## Getting Started

### Prerequisites
- Python 3.12.2
- PostgreSQL or a compatible database
- Alembic for database migrations
- Uvicorn to run the FastAPI application

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/priyanshis2024/socialmedia.git
   cd socialmedia

2. Set up a virtual environment:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate

3. Install dependencies:
   ```bash
   pip install -r requiremnents.txt

4. Configure environment variables:
   ```bash
   cp .env.template .env

Update the `.env` file with database and configuration details.

5. Apply database migrations:
   ```bash
   alembic upgrade head

6. Start the application:
   ```bash
   uvicorn core.main:app --reload
 
---

# Usage

- Access the API at `http://localhost:<port>`.
- Explore the available CRUD operations for users, posts, and comments.

## Project Structure
   ```
   .
   ├── core
   │   └── main.py
   ├── api
   │   ├── database.py
   │   ├── models
   │   │   └── model.py
   │   ├── schemas
   │   │   └── schema.py
   │   └── config.py
   ├── fetch
   │   ├── fetch_all_user.py
   │   ├── fetch_all_post.py
   │   ├── fetch_all_comment.py
   │   ├── fetch_post_by_user.py
   │   ├── fetch_single_post_with_their_user_and_comments.py
   │   └── fetch_all_post_with_their_user_and_comments.py
   ├── router
   │   ├── user.py
   │   ├── post.py
   │   └── comment.py
   ├── exception
   │   └── exceptions.py
   ├── alembic
   │   ├── versions
   │   └── env.py
   ├── .env.template
   ├── alembic.ini.template
   ├── requiremnents.txt
   ├── README.md
   └── LICENSE
```

### Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Ensure your changes include proper tests and documentation.