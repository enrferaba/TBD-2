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

## Historial de trabajos realizados
- **Trabajo1**: creación del repositorio base con entorno virtual, instalación offline de las dependencias mínimas (Django 5.2.8 y Pytest 9.0.1), generación del proyecto `biblioteca_config`, carpeta de tests global `tests/`, script `run_tests.py` y este archivo de contexto inicial.

## Estado actual
- El proyecto Django arranca en local (`python manage.py runserver` se probó en modo desarrollo).
- La suite de humo (`tests/test_smoke_project.py`) se ejecuta mediante `./run_tests.py` y pasa correctamente.
- `README.md` documenta el objetivo general, el stack previsto y deja constancia del trabajo realizado en esta fase inicial.
