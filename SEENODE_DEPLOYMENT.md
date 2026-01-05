# Guía de Despliegue en Seenode

Este documento contiene las instrucciones para desplegar la API de Portfolio en Seenode.

## Variables de Entorno Requeridas

Debes configurar las siguientes variables de entorno en el dashboard de Seenode:

### 1. Configuración General
```
ENVIRONMENT=production
PORT=8000
```

### 2. Base de Datos MySQL
```
ADMIN_PASSWORD=Juan123!
DATABASE=db_23rios9p45hz
USERNAME=db_23rios9p45hz
PASSWORD=5tKnFc16K7ZKJwcxS7HTW05h
HOST=up-de-fra1-mysql-1.db.run-on-seenode.com
DB_PORT=11550
```

### 3. JWT (Autenticación)
```
SECRET_KEY=Juan123!
ALGORITHM=HS256
```

### 4. Whitelist de IPs y Origins
```
WHITELISTED_IPS=127.0.0.1
```

**Nota:**
- **IPs:** Si necesitas agregar múltiples IPs, sepáralas con comas:
  ```
  WHITELISTED_IPS=127.0.0.1,192.168.1.100,10.0.0.50
  ```
- **Origins:** Para permitir acceso desde dominios específicos sin token (por ejemplo, tu frontend), agrégalos aquí:
  ```
  WHITELISTED_ORIGINS=https://tu-frontend.seenode.com,https://otro-dominio.com
  ```
- Si configuras `WHITELISTED_ORIGINS` con tu dominio de frontend, las peticiones desde ese dominio **NO necesitarán token de autenticación**

## Pasos para Configurar en Seenode

1. **Accede al dashboard de Seenode** y selecciona tu proyecto

2. **Ve a la sección de Variables de Entorno** (Environment Variables)

3. **Agrega cada variable** listada arriba con su respectivo valor

4. **Configura el puerto** en el dashboard de Seenode para que coincida con `PORT=8000`

5. **Comando de inicio:** Asegúrate de que Seenode ejecute:
   ```bash
   python start.py
   ```
   O alternativamente:
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Verificación del Despliegue

Después de desplegar, verifica que la API esté funcionando:

1. **Health Check:**
   ```
   GET https://tu-dominio.seenode.com/health
   ```
   Debería retornar: `{"status": "healthy"}`

2. **Documentación:**
   ```
   GET https://tu-dominio.seenode.com/docs
   ```
   Debería mostrar la documentación interactiva de Swagger

3. **Autenticación:**
   ```
   POST https://tu-dominio.seenode.com/auth
   ```
   Con las credenciales correctas debería retornar un token JWT

## Notas Importantes

- **No subas el archivo `.env` al repositorio** - las variables se configuran directamente en Seenode
- El archivo `.env.example` está en el repositorio como referencia
- La aplicación detecta automáticamente el modo producción mediante la variable `ENVIRONMENT`
- En producción, el auto-reload está deshabilitado para mejor rendimiento
- Asegúrate de que las IPs de Seenode estén en la whitelist si es necesario

## Solución de Problemas

### Error: "Application start failed"
- Verifica que todas las variables de entorno estén configuradas
- Revisa los logs de Seenode para más detalles
- Asegúrate de que el puerto configurado sea el correcto

### Error: "Database connection failed"
- Verifica las credenciales de la base de datos
- Confirma que el host y puerto sean correctos
- Asegúrate de que Seenode permita conexiones a tu base de datos MySQL

### Error: "Invalid token" en todas las peticiones
- Verifica que `SECRET_KEY` y `ALGORITHM` estén configurados
- Asegúrate de que la IP del cliente esté en `WHITELISTED_IPS` si aplica
- Verifica que estés enviando el token en el header `Authorization: Bearer <token>`