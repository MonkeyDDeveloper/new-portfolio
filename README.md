# Projects and Blogs API

REST API with FastAPI that includes OAuth2 authentication (client_credentials) and IP whitelist.

## Features

- **OAuth2 Authentication** with `client_id` and `client_secret`
- **IP Whitelist**: Specific IPs can access without authentication
- **Full CRUD** for Projects and Blogs
- **Advanced search and filters**
- **Automatic documentation** with Swagger/OpenAPI
- **Ready to deploy on Seenode**

## Project Structure

```
api_project/
├── main.py              # Entry point
├── config.py            # Configuration
├── database.py          # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication system
├── routers/
│   ├── __init__.py
│   ├── auth.py          # Auth endpoints
│   ├── projects.py      # Projects endpoints
│   └── blogs.py         # Blogs endpoints
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Local Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your configurations

# Run
uvicorn main:app --reload
```

## Deployment on Seenode

### 1. Prepare the repository

```bash
# Initialize git (if you haven't already)
git init
git add .
git commit -m "Initial commit"

# Push to GitHub/GitLab
git remote add origin <your-repository>
git push -u origin main
```

### 2. Configure on Seenode

1. Go to [Seenode Dashboard](https://seenode.com)
2. Create a new **Web Service**
3. Connect your GitHub/GitLab repository
4. Configure:
   - **Port**: `8000` (or the one you configure in .env)
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`

### 3. Environment Variables on Seenode

In the Seenode dashboard, add these environment variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRET_KEY` | `<generate-a-secure-key>` | Key for JWT |
| `DATABASE_URL` | `postgresql://...` | Your database URL |
| `WHITELISTED_IPS` | `<comma-separated-ips>` | IPs without authentication |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration |
| `ENVIRONMENT` | `production` | Environment |

> Tip: Generate a secret key with: `openssl rand -hex 32`

### 4. Database

For production, it's recommended to use PostgreSQL. You can create a database on Seenode or use an external service.

```
DATABASE_URL=postgresql://username:password@host:5432/database_name
```

## API Usage

### 1. Create the first client (only once)

```bash
curl -X POST https://your-app.seenode.com/auth/clients/seed \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "my-app",
    "client_secret": "my-secure-secret-minimum-10-characters",
    "name": "My Application"
  }'
```

### 2. Get access token

```bash
curl -X POST https://your-app.seenode.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "my-app",
    "client_secret": "my-secure-secret-minimum-10-characters"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. Use the API with token

```bash
# Create project
curl -X POST https://your-app.seenode.com/projects \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Project",
    "description": "Project description",
    "status": "active",
    "tags": "python,fastapi"
  }'

# List projects
curl https://your-app.seenode.com/projects \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1..."

# Search projects
curl "https://your-app.seenode.com/projects/search?title=My&status=active" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1..."
```

### 4. Access from whitelisted IP (without token)

If your IP is in `WHITELISTED_IPS`, you can access directly:

```bash
curl https://your-app.seenode.com/projects
```

## Endpoints

### Authentication (`/auth`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/token` | Get access token |
| POST | `/auth/clients/seed` | Create first client (no auth) |
| POST | `/auth/clients` | Create client (requires token) |
| GET | `/auth/me` | Current access info |
| DELETE | `/auth/clients/{id}` | Deactivate client |

### Projects (`/projects`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects` | List projects |
| GET | `/projects/search` | Search with filters |
| GET | `/projects/{id}` | Get project |
| POST | `/projects` | Create project |
| PUT | `/projects/{id}` | Update project |
| DELETE | `/projects/{id}` | Delete project |

### Blogs (`/blogs`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/blogs` | List blogs |
| GET | `/blogs/search` | Search with filters |
| GET | `/blogs/{id}` | Get blog |
| POST | `/blogs` | Create blog |
| PUT | `/blogs/{id}` | Update blog |
| DELETE | `/blogs/{id}` | Delete blog |
| PATCH | `/blogs/{id}/publish` | Publish/Unpublish |

## Interactive Documentation

- **Swagger UI**: `https://your-app.seenode.com/docs`
- **ReDoc**: `https://your-app.seenode.com/redoc`

## Security

- `client_secret` values are stored hashed with bcrypt
- JWT tokens have configurable expiration
- IP whitelist allows controlled access without token
- Sensitive endpoints (create/delete clients) always require token

## License

MIT
