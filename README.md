# Portfolio API

API RESTful para gestión de portfolio profesional construida con FastAPI, siguiendo la misma arquitectura del proyecto C#/.NET original.

## 🚀 Características

- ✅ **Autenticación JWT** con OAuth2
- ✅ **9 Entidades** del portfolio (Companies, Technologies, Projects, etc.)
- ✅ **49 Endpoints** REST totalmente funcionales
- ✅ **Arquitectura limpia** con patrón Repository
- ✅ **Entidades auto-generadoras** de queries SQL
- ✅ **Documentación automática** con Swagger/OpenAPI
- ✅ **Base de datos MySQL** en producción

## 📋 Estructura del Proyecto

```
api_project_clean/
├── main.py                      # Aplicación FastAPI principal
├── auth.py                      # Controlador de autenticación
├── portfolio_controller.py      # Controlador genérico del portfolio
├── schemas.py                   # Esquemas Pydantic con queries SQL
├── start.py                     # Script para iniciar servidor
├── requirements.txt             # Dependencias Python
├── .env                         # Variables de entorno
├── database/
│   ├── schema.sql              # Schema SQL completo
│   ├── init_db.py              # Script de inicialización
│   ├── client.py               # Conexión y servicio MySQL
│   ├── entities/
│   │   ├── base_entity.py      # Clase base abstracta
│   │   ├── mysql_entity.py     # Implementación MySQL
│   │   └── api_db_entities.py  # Entidades de auth
│   └── utils/
│       ├── password.py         # Utilidades de hash
│       └── utils.py            # Utilidades JWT
└── routers/
    ├── auth.py                 # Endpoints de autenticación
    ├── companies.py            # CRUD Companies
    ├── technologies.py         # CRUD Technologies
    ├── experiences.py          # CRUD Professional Experiences
    ├── projects.py             # CRUD Projects
    ├── project_tasks.py        # CRUD Project Tasks
    ├── responsibilities.py     # CRUD Responsibilities
    ├── technology_projects.py  # Many-to-Many Tech-Projects
    ├── company_experiences.py  # Many-to-Many Company-Exp
    └── technology_experiences.py # Many-to-Many Tech-Exp
```

## 🗄️ Modelo de Datos

### Entidades Principales
1. **Companies** - Empresas del portfolio
2. **Technologies** - Tecnologías utilizadas
3. **Professional Experiences** - Experiencias laborales
4. **Projects** - Proyectos desarrollados

### Entidades Relacionadas
5. **Project Tasks** - Tareas de proyectos
6. **Responsibilities** - Responsabilidades por experiencia

### Relaciones Many-to-Many
7. **Technology-Projects** - Tecnologías por proyecto
8. **Company-Experiences** - Empresas por experiencia
9. **Technology-Experiences** - Tecnologías por experiencia

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
cd /Users/javier/Documents/Portfolio/api_project_clean
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Edita el archivo `.env` con tus credenciales:

```env
# Database
DATABASE=db_23rios9p45hz
USERNAME=db_23rios9p45hz
PASSWORD=tu_password
HOST=up-de-fra1-mysql-1.db.run-on-seenode.com
DB_PORT=11550

# JWT
SECRET_KEY=tu-clave-secreta-super-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Security
WHITELISTED_IPS=127.0.0.1

# Server
PORT=8000
ENVIRONMENT=production
```

### 4. Inicializar la base de datos
```bash
python database/init_db.py
```

Este script:
- ✅ Crea todas las tablas
- ✅ Configura foreign keys e índices
- ✅ Inserta datos de ejemplo
- ✅ Crea un usuario admin (username: `admin`, password: `Juan123!`)

### 5. Iniciar el servidor
```bash
python start.py
```

O con uvicorn directamente:
```bash
uvicorn main:app --reload --port 8000
```

## 📚 Documentación API

Una vez iniciado el servidor, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Autenticación

### Obtener Token
```bash
POST /auth/token
Content-Type: application/json

{
  "api_user": {
    "username": "admin",
    "email": "admin@example.com",
    "password": "Juan123!"
  }
}
```

### Respuesta
```json
{
  "success": true,
  "message": "User authenticated successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 📍 Endpoints Principales

### Companies
```bash
POST   /companies/                  # Crear empresa
GET    /companies/                  # Listar empresas
GET    /companies/{company_id}      # Obtener empresa
PUT    /companies/{company_id}      # Actualizar empresa
DELETE /companies/{company_id}      # Eliminar empresa
```

### Technologies
```bash
POST   /technologies/               # Crear tecnología
GET    /technologies/               # Listar tecnologías
GET    /technologies/{tech_id}      # Obtener tecnología
PUT    /technologies/{tech_id}      # Actualizar tecnología
DELETE /technologies/{tech_id}      # Eliminar tecnología
```

### Professional Experiences
```bash
POST   /experiences/                # Crear experiencia
GET    /experiences/                # Listar experiencias
GET    /experiences/{exp_id}        # Obtener experiencia
PUT    /experiences/{exp_id}        # Actualizar experiencia
DELETE /experiences/{exp_id}        # Eliminar experiencia
```

### Projects
```bash
POST   /projects/                   # Crear proyecto
GET    /projects/                   # Listar proyectos
GET    /projects/{project_id}       # Obtener proyecto
PUT    /projects/{project_id}       # Actualizar proyecto
DELETE /projects/{project_id}       # Eliminar proyecto
```

*(Y 5 grupos más de endpoints para las demás entidades)*

## 🎯 Ejemplos de Uso

### Crear una empresa
```bash
curl -X POST "http://localhost:8000/companies/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TechCorp",
    "logo_path": "/logos/techcorp.png"
  }'
```

### Crear un proyecto
```bash
curl -X POST "http://localhost:8000/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Portfolio API",
    "description": "RESTful API for portfolio management",
    "github_uri": "https://github.com/user/portfolio-api"
  }'
```

### Asociar tecnología a proyecto
```bash
curl -X POST "http://localhost:8000/technology-projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "technology_id": 1,
    "project_id": 1
  }'
```

### Listar proyectos con paginación
```bash
curl "http://localhost:8000/projects/?skip=0&limit=10"
```

## 🏗️ Arquitectura

### Patrón de Diseño

Este proyecto sigue el **patrón Repository** con capas bien definidas:

```
┌─────────────────────────────────────┐
│         FastAPI Routers             │  ← Capa de Presentación
│  (companies.py, projects.py, etc.)  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     PortfolioController             │  ← Capa de Aplicación
│   (Orquesta la lógica de negocio)  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│        MySQLService                 │  ← Capa de Servicio
│   (Lógica de negocio genérica)     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      MySQLConnection                │  ← Capa de Datos
│  (Ejecución de queries genéricas)  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     BaseEntity/MySQLEntity          │  ← Entidades
│  (Auto-generación de queries SQL)  │
└─────────────────────────────────────┘
```

### Ventajas de esta Arquitectura

1. **DB Agnostic**: `BaseEntity` es abstracta, puedes crear `MongoEntity`, `PostgresEntity`, etc.
2. **DRY**: No repites código SQL, las entidades lo generan automáticamente
3. **Type Safe**: Pydantic valida todos los datos
4. **Testable**: Cada capa se puede testear independientemente
5. **Escalable**: Fácil agregar nuevas entidades

## 🔧 Stack Tecnológico

- **Framework**: FastAPI 0.109.0
- **Base de datos**: MySQL 8.0
- **ORM**: Raw SQL (con patrón Repository)
- **Validación**: Pydantic 2.x
- **Autenticación**: JWT (python-jose + bcrypt)
- **Servidor**: Uvicorn
- **Documentación**: OpenAPI/Swagger

## 📦 Dependencias Principales

```txt
fastapi>=0.109.0
uvicorn>=0.27.0
pydantic>=2.0.0
pymysql>=1.1.0
python-jose>=3.3.0
bcrypt>=4.0.1
python-decouple>=3.8
```

## 🚧 Próximas Mejoras

- [ ] Agregar autenticación a endpoints del portfolio
- [ ] Implementar middleware de autorización por roles
- [ ] Agregar tests unitarios y de integración
- [ ] Implementar caché con Redis
- [ ] Agregar paginación con cursors
- [ ] Implementar rate limiting
- [ ] Agregar logging estructurado
- [ ] Crear Docker Compose para desarrollo local

## 📝 Licencia

Este proyecto es parte de un portfolio personal.

## 👤 Autor

Javier - [GitHub](https://github.com/MonkeyDDeveloper)

---

**¿Necesitas ayuda?** Abre un issue en GitHub o consulta la documentación en `/docs`
