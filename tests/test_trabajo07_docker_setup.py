from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def read_file(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")

def test_trabajo07_existe_dockerfile_en_raiz():
    assert (PROJECT_ROOT / "Dockerfile").exists()

def test_trabajo07_existe_docker_compose_en_raiz():
    assert (PROJECT_ROOT / "docker-compose.yml").exists()

def test_trabajo07_existe_env_example():
    assert (PROJECT_ROOT / ".env.example").exists()

def test_trabajo07_docker_compose_contiene_servicios_basicos():
    compose = read_file("docker-compose.yml")
    for service in ["web:", "redis:", "mongo:", "neo4j:", "celery_worker:"]:
        assert service in compose
    assert "celery_beat:" in compose

def test_trabajo07_docker_compose_define_volumenes_para_mongo_y_neo4j():
    compose = read_file("docker-compose.yml")
    assert "mongo_data" in compose
    assert "neo4j_data" in compose
    assert "neo4j_logs" in compose

def test_trabajo07_docker_compose_define_puertos_para_web_y_neo4j():
    compose = read_file("docker-compose.yml")
    assert '"8000:8000"' in compose
    assert '"7474:7474"' in compose
    assert '"7687:7687"' in compose

def test_trabajo07_env_example_contiene_claves_basicas():
    env_example = read_file(".env.example")
    for key in [
        "DJANGO_SECRET_KEY",
        "DJANGO_DEBUG",
        "REDIS_URL",
        "MONGO_URI",
        "MONGO_DB_NAME",
        "MONGO_ACTIVITY_COLLECTION",
        "NEO4J_URI",
        "NEO4J_USER",
        "NEO4J_PASSWORD",
    ]:
        assert key in env_example
