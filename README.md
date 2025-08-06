# Pipegram Flask API

An unofficial Instagram API implemented in Python using Flask and [instagrapi](https://github.com/subzeroid/instagrapi). This project re‑implements the functionality of the original Node.js Pipegram API in a modular and extensible manner. **Use at your own risk:** it interacts with Instagram via reverse‑engineered endpoints and may break or cause account restrictions.

## Features

* **Authentication**: login with username/password, resume saved sessions, import JSON sessions and delete sessions.
* **Posts**: publish photos or videos to feed, stories or reels by providing a base64 payload or remote URL.
* **Direct Messages**: send text messages, list inbox threads and retrieve messages from a thread.
* **Profile**: fetch public profile information and update the biography or profile picture of the logged in user.
* **Stories**: list current public stories of a given username.
* **Swagger UI**: automatically generated API documentation served at `/api-docs`.

## Installation

1. Clone the repository and change into the directory:

   ```bash
   git clone https://github.com/your_user/pipegram_flask.git
   cd pipegram_flask
   ```

2. Copy the example environment file and adjust values:

   ```bash
   cp example.env .env
   # edit .env to set ADMIN_TOKEN and other secrets
   ```

3. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Run the application locally:

   ```bash
   python run.py
   ```

   The API will be available on `http://localhost:5000` and Swagger docs at `http://localhost:5000/api-docs`.

Alternatively, use Docker:

```bash
docker build -t pipegram-flask .
docker run --env-file .env -p 5000:5000 pipegram-flask
```

## Using docker-compose

The repository includes a `docker-compose.yml` that will build and run the service. It mounts the `sessions/` directory as a volume so session files persist across restarts.

```bash
docker-compose up --build
```

## Making authenticated requests

Most endpoints (except for `/auth/*`) require a valid **admin token**. Set `ADMIN_TOKEN` in your `.env` and include it in the `Authorization` header of requests as follows:

```
Authorization: Bearer <your-admin-token>
```

## Disclaimer

This project uses an unofficial Instagram API obtained via reverse engineering. Use is subject to Instagram’s terms and conditions. Accounts can be restricted or banned for automated actions. Use responsibly and respect Instagram’s policies.