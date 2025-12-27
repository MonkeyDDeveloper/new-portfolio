# API de Proyectos y Blogs

API REST con FastAPI que incluye autenticación OAuth2 (client_credentials) y whitelist de IPs.

## Características

- **Autenticación OAuth2** con `client_id` y `client_secret`
- **Whitelist de IPs**: IPs específicas pueden acceder sin autenticación
- **CRUD completo** para Proyectos y Blogs
- **Búsqueda y filtros** avanzados
- **Documentación automática** con Swagger/OpenAPI
- **Listo para desplegar en Seenode**

## Estructura del Proyecto

```
api_project/
├── main.py              # Punto de entrada
├── config.py            # Configuración
├── database.py          # Modelos SQLAlchemy
├── schemas.py           # Esquemas Pydantic
├── auth.py              # Sistema de autenticación
├── routers/
│   ├── __init__.py
│   ├── auth.py          # Endpoints de auth
│   ├── projects.py      # Endpoints de proyectos
│   └── blogs.py         # Endpoints de blogs
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Instalación Local

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Copiar y configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Ejecutar
uvicorn main:app --reload
```

## Despliegue en Seenode

### 1. Preparar el repositorio

```bash
# Inicializar git (si no lo has hecho)
git init
git add .
git commit -m "Initial commit"

# Subir a GitHub/GitLab
git remote add origin <tu-repositorio>
git push -u origin main
```

### 2. Configurar en Seenode

1. Ve al [Dashboard de Seenode](https://seenode.com)
2. Crea un nuevo **Web Service**
3. Conecta tu repositorio de GitHub/GitLab
4. Configura:
   - **Port**: `8000` (o el que configures en .env)
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`

### 3. Variables de Entorno en Seenode

En el dashboard de Seenode, agrega estas variables de entorno:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `SECRET_KEY` | `<genera-una-clave-segura>` | Clave para JWT |
| `DATABASE_URL` | `postgresql://...` | URL de tu base de datos |
| `WHITELISTED_IPS` | `<ips-separadas-por-coma>` | IPs sin autenticación |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Expiración del token |
| `ENVIRONMENT` | `production` | Entorno |

> 💡 **Tip**: Genera una clave secreta con: `openssl rand -hex 32`

### 4. Base de Datos

Para producción, se recomienda usar PostgreSQL. Puedes crear una base de datos en Seenode o usar un servicio externo.

```
DATABASE_URL=postgresql://usuario:password@host:5432/nombre_db
```

## Uso de la API

### 1. Crear el primer cliente (solo una vez)

```bash
curl -X POST https://tu-app.seenode.com/auth/clients/seed \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "mi-app",
    "client_secret": "mi-secreto-seguro-minimo-10-caracteres",
    "name": "Mi Aplicación"
  }'
```

### 2. Obtener token de acceso

```bash
curl -X POST https://tu-app.seenode.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "mi-app",
    "client_secret": "mi-secreto-seguro-minimo-10-caracteres"
  }'
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. Usar la API con token

```bash
# Crear proyecto
curl -X POST https://tu-app.seenode.com/projects \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi Proyecto",
    "description": "Descripción del proyecto",
    "status": "active",
    "tags": "python,fastapi"
  }'

# Listar proyectos
curl https://tu-app.seenode.com/projects \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1..."

# Buscar proyectos
curl "https://tu-app.seenode.com/projects/search?title=Mi&status=active" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1..."
```

### 4. Acceso desde IP en whitelist (sin token)

Si tu IP está en `WHITELISTED_IPS`, puedes acceder directamente:

```bash
curl https://tu-app.seenode.com/projects
```

## Endpoints

### Autenticación (`/auth`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/token` | Obtener token de acceso |
| POST | `/auth/clients/seed` | Crear primer cliente (sin auth) |
| POST | `/auth/clients` | Crear cliente (requiere token) |
| GET | `/auth/me` | Info del acceso actual |
| DELETE | `/auth/clients/{id}` | Desactivar cliente |

### Proyectos (`/projects`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/projects` | Listar proyectos |
| GET | `/projects/search` | Buscar con filtros |
| GET | `/projects/{id}` | Obtener proyecto |
| POST | `/projects` | Crear proyecto |
| PUT | `/projects/{id}` | Actualizar proyecto |
| DELETE | `/projects/{id}` | Eliminar proyecto |

### Blogs (`/blogs`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/blogs` | Listar blogs |
| GET | `/blogs/search` | Buscar con filtros |
| GET | `/blogs/{id}` | Obtener blog |
| POST | `/blogs` | Crear blog |
| PUT | `/blogs/{id}` | Actualizar blog |
| DELETE | `/blogs/{id}` | Eliminar blog |
| PATCH | `/blogs/{id}/publish` | Publicar/Despublicar |

## Documentación Interactiva

- **Swagger UI**: `https://tu-app.seenode.com/docs`
- **ReDoc**: `https://tu-app.seenode.com/redoc`

## Seguridad

- Los `client_secret` se almacenan hasheados con bcrypt
- Los tokens JWT tienen expiración configurable
- La whitelist de IPs permite acceso controlado sin token
- Endpoints sensibles (crear/eliminar clientes) siempre requieren token

## Licencia

MIT
