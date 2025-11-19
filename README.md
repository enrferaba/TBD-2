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
- **Trabajo1**: creación del repositorio base con entorno virtual, instalación offline de las dependencias mínimas (Django 5.2.8
y Pytest 9.0.1), generación del proyecto `biblioteca_config`, carpeta de tests global `tests/`, script `run_tests.py` y este ar
chivo de contexto inicial.
- **Trabajo2**: alta de la app principal `library`, definición de la ruta de inicio/health (`/`), estandarización de la convenci
ón `test_trabajoXX_*` y ampliación de la suite con los tests de Trabajo2.
- **Trabajo3**: instalación de Django REST Framework, creación del endpoint JSON `/api/health/` y nuevos tests `tests/test_traba
jo03_api_health.py` siguiendo la convención definida.
- **Trabajo4**: definición del modelo `Book` (con campos `title`, `author`, `published_year`, `isbn` y trazabilidad), exponer un serializer propio
para la API y publicar los endpoints `/api/books/` y `/api/books/<id>/` junto con la batería de tests `tests/test_trabajo04_books_api.py`.

## Estado actual
- La app principal se llama `library`, expone una ruta HTML mínima en `/` y una API JSON en `/api/health/`.
- El dominio incluye el modelo `Book` en `library/models.py` respaldado por un repositorio en memoria para los tests mientras se mantiene la compatibilidad con la infraestructura offline.
- Los endpoints REST `/api/books/` (listado) y `/api/books/<id>/` (detalle) devuelven JSON serializado mediante `BookSerializer`.
- Las suites `tests/test_trabajo01_smoke.py`, `tests/test_trabajo02_library_app.py`, `tests/test_trabajo03_api_health.py` y `tests/test_trabajo04_books_api.py` se ejecutan en verde con `./run_tests.py` (modo `-vv`).

## API actual
- `GET /api/health/` → responde con JSON indicando `{ "service": "Biblioteca Online", "status": "ok", "version": "trabajo4" }`.
- `GET /api/books/` → devuelve una lista de libros con campos `id`, `title`, `author`, `published_year` e `isbn` (lista vacía si no hay registros).
- `GET /api/books/<id>/` → devuelve el detalle de un libro (mismos campos que el listado) o un JSON `{ "detail": "Libro no encontrado" }` con estado 404.
