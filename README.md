# �� Pipegram (Flask) - Unofficial Instagram API

![Pipegram Logo](https://i.imgur.com/kKHUeGh.png)

**Pipegram** is an **unofficial** Instagram API developed to automate common actions on Instagram accounts, with support for **multiple simultaneous sessions**. Now rewritten in Python/Flask using the [instagrapi](https://subzeroid.github.io/instagrapi/) library.

Interactive documentation is available at `/apidocs` when the service is running.

## 🚀 Technologies

- **Python 3.11+**
- **Flask 3.0** with async support
- **[instagrapi](https://subzeroid.github.io/instagrapi/)** - Modern and powerful Instagram API library
- **Docker & Docker Compose**
- **Swagger/Flasgger** for documentation
- **Pydantic** for data validation

## ✅ Features

### 📌 Authentication
- Login with username/password
- 2FA support
- Session management (save/load)
- Session import/export
- Multiple account support

### 💬 Direct Messages
- Send text messages
- Send photos (base64 or URL)
- View inbox conversations
- View thread messages
- Real-time messaging

### 📷 Posts & Stories
- Upload photos to feed
- Upload photos to stories
- Add captions and descriptions
- Media management

### 👤 Profile Management
- View user information
- Change profile picture
- Edit biography
- View user stories
- Follow/unfollow users

### 🔧 Advanced Features
- Proxy support
- Session persistence
- Error handling
- Rate limiting protection
- Comprehensive logging

## 🛠️ Installation

### Prerequisites
- Docker and Docker Compose
- Make (optional, for convenience)

### Quick Start

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Pipegram
```

2. **Configure environment variables:**
```bash
# Create .env file
echo "ADMIN_TOKEN=your_admin_token_here" > .env
```

3. **Start the API:**
```bash
# Using Makefile
make start

# Or using Docker Compose directly
docker compose up --build -d
```

4. **Access the API:**
- API: http://localhost:3000
- Documentation: http://localhost:3000/apidocs

## 📚 API Documentation

### Authentication

All protected routes require Bearer token authentication in the header:
```
Authorization: Bearer your_admin_token_here
```

### Main Endpoints

#### Authentication
- `POST /auth/login` - Login with Instagram credentials
- `POST /auth/resume` - Resume existing session
- `GET /auth/status` - Check session status
- `DELETE /auth/delete` - Delete saved session
- `POST /auth/import-session` - Import existing session

#### Direct Messages
- `POST /dm/send` - Send text message
- `POST /dm/send-photo` - Send photo message
- `GET /dm/inbox` - Get inbox conversations
- `GET /dm/thread/<threadId>` - Get thread messages

#### Posts
- `POST /post/photo` - Upload photo to feed
- `POST /post/story` - Upload photo to story

#### Profile
- `GET /profile/info/<username>` - Get user information
- `POST /profile/picture` - Change profile picture
- `PUT /profile/bio` - Edit biography
- `GET /profile/stories/<username>` - Get user stories

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ADMIN_TOKEN` | Admin authentication token | `token` |
| `PORT` | API port | `3000` |

### Docker Configuration

The API runs in a Docker container with:
- Python 3.11 slim image
- Gunicorn WSGI server
- 2 worker processes
- Session persistence via volume mount

## 🚀 Usage Examples

### 1. Login to Instagram
```bash
curl -X POST "http://localhost:3000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

### 2. Send Direct Message
```bash
curl -X POST "http://localhost:3000/dm/send" \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "toUsername": "recipient_username",
    "message": "Hello! How are you?"
  }'
```

### 3. Send Photo via DM
```bash
curl -X POST "http://localhost:3000/dm/send-photo" \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "toUsername": "recipient_username",
    "base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
  }'
```

### 4. Upload Photo to Feed
```bash
curl -X POST "http://localhost:3000/post/photo" \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA...",
    "caption": "Amazing photo!"
  }'
```

## 🔒 Security

- All sensitive routes require Bearer token authentication
- Sessions are stored locally in JSON format
- No sensitive data is logged
- Rate limiting protection against Instagram restrictions

## 🐛 Troubleshooting

### Common Issues

1. **Login fails with "checkpoint_challenge_required"**
   - Instagram requires additional verification (2FA/Captcha)
   - Complete verification manually on Instagram app/website

2. **"Session not found" error**
   - Session may have expired
   - Re-login to create new session

3. **Rate limiting errors**
   - Instagram detected automated activity
   - Wait before making more requests
   - Consider using proxy

### Logs
```bash
# View container logs
docker compose logs api-instagram

# Follow logs in real-time
docker compose logs -f api-instagram
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is an **unofficial** Instagram API. Use at your own risk and in compliance with Instagram's Terms of Service. The developers are not responsible for any account restrictions or bans.

## 🔗 Links

- [instagrapi Documentation](https://subzeroid.github.io/instagrapi/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)

---

**Made with ❤️ for the Instagram automation community**
