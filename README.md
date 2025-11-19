# Biblioteca Online – Sistema Full Stack con Django, Redis, MongoDB y Neo4j

## Descripción breve del proyecto
Biblioteca Online será una plataforma para consultar un catálogo digital de libros, gestionar reseñas de la comunidad y ofrecer
recomendaciones personalizadas. Sobre una base Django/DRF iremos añadiendo procesos asíncronos (Celery), caché con Redis y persi
stencia especializada en MongoDB y Neo4j para conocimiento de grafos. También se prevé exponer APIs públicas y herramientas inte
rnas para el personal bibliotecario.

## Stack tecnológico previsto
- Django y Django REST Framework para el backend principal.
- Celery y Redis para tareas asíncronas y colas.
- PostgreSQL como base relacional principal.
- MongoDB para reseñas enriquecidas y análisis semiestructurados.
- Neo4j para el grafo de recomendaciones.
- Docker Compose para orquestar los servicios de infraestructura.
- Pytest y herramientas de calidad (por definir) para CI.

## Convención de tests por trabajo
- Cada trabajo cuenta con al menos un archivo `tests/test_trabajoXX_<descripcion>.py`.
- Todos los tests definidos en esos archivos siguen la convención `test_trabajoXX_<caso>`.
- La salida de `./run_tests.py` (modo `-vv`) permite identificar de inmediato qué trabajo se ha roto al ver el nombre del archiv
o y del test.

## Historial de trabajos realizados
- **Trabajo1**: creación del repositorio base con entorno virtual, instalación offline de las dependencias mínimas (Django 5.2.8 y Pytest 9.0.1), generación del proyecto `biblioteca_config`, carpeta de tests global `tests/`, script `run_tests.py` y este archivo de contexto inicial.
- **Trabajo2**: alta de la app principal `library`, definición de la ruta de inicio/health (`/`), estandarización de la convención `test_trabajoXX_*` y ampliación de la suite con los tests de Trabajo2.
- **Trabajo3**: instalación de Django REST Framework, creación del endpoint JSON `/api/health/` y nuevos tests `tests/test_trabajo03_api_health.py` siguiendo la convención definida.
- **Trabajo4**: definición del modelo `Book` (campos `title`, `author`, `published_year`, `isbn` y trazabilidad), serializer propio y publicación de los endpoints `/api/books/` y `/api/books/<id>/` junto con los tests `tests/test_trabajo04_books_api.py`.
- **Trabajo5**: ampliación de la API de libros a un CRUD completo (listar, crear, actualizar y borrar), validaciones con `BookInputSerializer` y cobertura adicional en `tests/test_trabajo05_books_crud_api.py`.
- **Trabajo6**: activación del sistema de usuarios (auth de Django simplificado), asociación del campo `created_by` en `Book` y restricción de permisos en la API de libros (lectura pública, escritura solo autenticada) con los tests `tests/test_trabajo06_books_permissions_api.py`.
- **Trabajo7**: dockerización mínima del proyecto con `Dockerfile`, `docker-compose.yml` y `.env.example`, definición de los servicios web/Redis/Mongo/Neo4j/Celery y tests de configuración en `tests/test_trabajo07_docker_setup.py`.
- **Trabajo8**: integración básica con MongoDB mediante PyMongo, módulo compartido `library/mongo_client.py`, servicio de actividad (`log_activity`/`list_recent_activity`), endpoint `/api/mongo/health/` y tests de conexión/escritura en `tests/test_trabajo08_mongo_integration.py`.
- **Trabajo9**: modelado de reseñas y valoraciones en MongoDB con `library/reviews_service.py`, endpoints `/api/books/<id>/reviews/` (GET/POST) y `/api/books/<id>/rating/`, media de rating integrada en el detalle del libro y tests en `tests/test_trabajo09_reviews_mongo_api.py`.
- **Trabajo10**: integración de Neo4j mediante `library/neo4j_client.py` y `library/neo4j_service.py`, tareas Celery (`library/tasks.py`) que sincronizan reseñas hacia el grafo y calculan recomendaciones, endpoint `/api/recommendations/` y cobertura en `tests/test_trabajo10_neo4j_celery_recommendations.py` junto con el recorrido de demo E2E.

## Estado actual
- La app principal `library` expone una vista HTML mínima en `/` y las APIs JSON `/api/health/` y `/api/mongo/health/`.
- El dominio incluye el modelo `Book` en `library/models.py` respaldado por un repositorio en memoria para los tests mientras se prepara la persistencia real.
- La API de libros expone listado, detalle, creación (`POST`), actualización (`PUT`/`PATCH`) y borrado (`DELETE`) con control de permisos: lectura pública y operaciones de escritura reservadas a usuarios autenticados; cada libro persiste su `created_by`.
- Existe un servicio de actividad que escribe en la colección `activity_logs` de Mongo a través de PyMongo y puede consultarse con `list_recent_activity`.
- MongoDB también almacena reseñas y valoraciones por libro en la colección `book_reviews` (configurable). El servicio `reviews_service` ofrece inserción, listado y cálculo de medias reutilizado por la API.
- Los archivos `tests/test_trabajo01_smoke.py`, `tests/test_trabajo02_library_app.py`, `tests/test_trabajo03_api_health.py`, `tests/test_trabajo04_books_api.py`, `tests/test_trabajo05_books_crud_api.py`, `tests/test_trabajo06_books_permissions_api.py`, `tests/test_trabajo07_docker_setup.py`, `tests/test_trabajo08_mongo_integration.py`, `tests/test_trabajo09_reviews_mongo_api.py` y `tests/test_trabajo10_neo4j_celery_recommendations.py` pasan en verde mediante `./run_tests.py` en modo `-vv`, dejando cubiertos los Trabajos 01–10.
- Existe un `Dockerfile` funcional y la orquestación `docker-compose.yml` que levantan web, Redis, MongoDB, Neo4j y procesos de Celery basados en las variables documentadas en `.env.example`; las nuevas tareas sincronizan reseñas hacia el grafo y alimentan el endpoint de recomendaciones.
- El grafo en memoria de Neo4j se mantiene sincronizado a través de `library/neo4j_service.py` y las tareas `task_sync_book_reviews_to_neo4j`/`task_sync_user_recommendations`, mientras que MongoDB sigue almacenando actividad y reseñas.

## API actual
- `GET /api/health/` → responde con JSON indicando `{ "service": "Biblioteca Online", "status": "ok", "version": "trabajo4" }`.
- `GET /api/books/` → lista libros con los campos `id`, `title`, `author`, `published_year`, `isbn` y `created_by` (lista vacía si no hay registros). Acceso público.
- `POST /api/books/` → crea un libro nuevo (campos obligatorios: `title`, `author`; opcionales: `published_year`, `isbn`). Requiere usuario autenticado y el `created_by` queda fijado con su `username`.
- `GET /api/books/<id>/` → devuelve el detalle de un libro o `{ "detail": "Libro no encontrado" }` si el id no existe.
- `PUT/PATCH /api/books/<id>/` → actualiza un libro existente validando los mismos campos que el POST (PUT requiere todos los obligatorios; PATCH permite parciales). Requiere usuario autenticado.
- `DELETE /api/books/<id>/` → elimina un libro existente y devuelve 204; si no existe responde 404. Requiere usuario autenticado.
- `GET /api/books/<id>/reviews/` → lista las reseñas guardadas para un libro, incluyendo `rating`, `comment`, `username` y marcas de tiempo. Acceso público.
- `POST /api/books/<id>/reviews/` → crea una reseña (requiere usuario autenticado) validando `rating` (1–5) y un comentario opcional.
- `GET /api/books/<id>/rating/` → devuelve la media (`average_rating`) y el número total de reseñas (`num_reviews`) calculados desde MongoDB.
- `GET /api/mongo/health/` → comprueba el estado de MongoDB ejecutando un `ping` y devolviendo el resultado de `server_info`; acceso público.
- `GET /api/recommendations/` → lista los libros recomendados para el usuario autenticado según el grafo sincronizado en Neo4j. Requiere autenticación; se basa en las tareas Celery que consumen las reseñas de Mongo.

## Arquitectura de servicios (Docker Compose)
- **web**: servicio Django/DRF construido a partir del `Dockerfile`, expone el puerto 8000 y consume las variables del `.env`.
- **redis**: caché y broker de Celery disponible en el puerto 6379.
- **mongo**: base documental con persistencia en el volumen `mongo_data` y puerto 27017.
- **neo4j**: grafo de recomendaciones con puertos 7474/7687 y volúmenes `neo4j_data` y `neo4j_logs`.
- **celery_worker**: procesa tareas en segundo plano usando el mismo código que web y `redis` como broker para ejecutar `task_sync_book_reviews_to_neo4j` y `task_sync_user_recommendations`.
- **celery_beat**: programador opcional de tareas periódicas que comparte imagen con web y depende de redis.
- Las variables sensibles (secret key, URIs de Redis/Mongo/Neo4j y credenciales) se documentan en `.env.example`; el servicio web toma `MONGO_URI`, `MONGO_DB_NAME`, `MONGO_ACTIVITY_COLLECTION`, `MONGO_REVIEWS_COLLECTION`, `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`, `CELERY_BROKER_URL` y `CELERY_RESULT_BACKEND`.

## Recorrido de demo sugerido
1. **Levantar la infraestructura** con `docker compose up --build` para disponer de web, Redis, MongoDB, Neo4j y procesos de Celery.
2. **Crear libros** mediante la API (`POST /api/books/`) autenticado con un usuario creado via los tests o shell.
3. **Registrar reseñas** con distintos usuarios (`POST /api/books/<id>/reviews/`). Cada reseña dispara `task_sync_book_reviews_to_neo4j` y `task_sync_user_recommendations`, por lo que el grafo queda sincronizado.
4. **Consultar el estado** del sistema en `/api/health/` y `/api/mongo/health/` para confirmar que los servicios base responden.
5. **Obtener recomendaciones** llamando a `GET /api/recommendations/` autenticado como un lector: la respuesta lista libros no valorados por el usuario pero con buenas valoraciones en Neo4j.
6. **Visualizar el grafo** abriendo Neo4j Browser (puerto 7474) para comprobar los nodos `User`, `Book` y las relaciones `RATED` generadas por las tareas.
7. **Ejecutar `./run_tests.py`** para cerrar la demo validando que toda la suite Trabajo01–Trabajo10 sigue en verde.
