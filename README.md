# Biblioteca Online – Sistema Full Stack con Django, Redis, MongoDB y Neo4j

## Descripción breve del proyecto
Biblioteca Online será una plataforma para consultar un catálogo digital de libros, gestionar reseñas de la comunidad y ofrecer recomendaciones personalizadas. Sobre una base Django/DRF iremos añadiendo procesos asíncronos (Celery), caché con Redis y persistencia especializada en MongoDB y Neo4j para conocimiento de grafos. También se prevé exponer APIs públicas y herramientas internas para el personal bibliotecario.

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
- La salida de `./run_tests.py` (modo `-vv`) permite identificar de inmediato qué trabajo se ha roto al ver el nombre del archivo y del test.

## Historial de trabajos realizados
- **Trabajo1**: creación del repositorio base con entorno virtual, instalación offline de las dependencias mínimas (Django 5.2.8 y Pytest 9.0.1), generación del proyecto `biblioteca_config`, carpeta de tests global `tests/`, script `run_tests.py` y este archivo de contexto inicial.
- **Trabajo2**: alta de la app principal `library`, definición de la ruta de inicio/health (`/`), estandarización de la convención `test_trabajoXX_*` y ampliación de la suite con los tests de Trabajo2.

## Estado actual
- La app principal se llama `library` y expone un endpoint de salud en la ruta `/`.
- Las suites `tests/test_trabajo01_smoke.py` y `tests/test_trabajo02_library_app.py` se ejecutan con `./run_tests.py` y reportan cada test con nombres verbosos.
- `README.md` incluye la convención de nombres de tests, el historial actualizado y el estado operativo tras Trabajo2.
