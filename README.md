# FastAPI Template

A production-ready FastAPI template with PostgreSQL, Redis, and RabbitMQ, fully containerized with Docker.

## Features

- 🚀 **FastAPI** - Modern, high-performance web framework
- 🐘 **PostgreSQL** - Robust relational database with async support
- ⚡ **Redis** - In-memory caching for improved performance
- 🐰 **RabbitMQ** - Message broker for async task processing
- 🐳 **Docker** - Fully containerized for easy deployment
- 🔒 **Security** - JWT authentication ready, CORS configured
- 📝 **Pydantic** - Data validation and settings management
- 📚 **Auto-generated API docs** - Swagger UI and ReDoc

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection management
│   ├── dependencies.py   # Dependency injection utilities
│   └── routers/
│       ├── __init__.py
│       ├── health.py     # Health check endpoints
│       ├── users.py      # User CRUD endpoints
│       └── items.py      # Item CRUD endpoints with Redis caching
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/BadRabbit00/FastAPI_Template.git
   cd FastAPI_Template
   ```

2. **Copy environment file**
   ```bash
   cp .env.example .env
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - API: http://localhost:8000
   - API Docs (Swagger): http://localhost:8000/api/v1/docs
   - API Docs (ReDoc): http://localhost:8000/api/v1/redoc
   - RabbitMQ Management: http://localhost:15672 (guest/guest)

### Local Development

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start infrastructure services**
   ```bash
   docker-compose up -d db redis rabbitmq
   ```

4. **Update .env for local development**
   ```
   POSTGRES_HOST=localhost
   REDIS_HOST=localhost
   RABBITMQ_HOST=localhost
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Health
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health with service status

### Users
- `GET /api/v1/users` - List all users
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Items
- `GET /api/v1/items` - List all items
- `POST /api/v1/items` - Create a new item
- `GET /api/v1/items/{item_id}` - Get item by ID (with Redis caching)
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item

## Configuration

All configuration is managed through environment variables. See `.env.example` for available options:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | FastAPI_Template |
| `DEBUG` | Enable debug mode | False |
| `SECRET_KEY` | JWT secret key | your-super-secret-key |
| `POSTGRES_*` | PostgreSQL connection settings | See .env.example |
| `REDIS_*` | Redis connection settings | See .env.example |
| `RABBITMQ_*` | RabbitMQ connection settings | See .env.example |

## Useful Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop all services
docker-compose down

# Rebuild application container
docker-compose build app

# Reset all data (removes volumes)
docker-compose down -v

# Run tests
pytest

# Format code
black app/
isort app/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is open source and available under the MIT License.
