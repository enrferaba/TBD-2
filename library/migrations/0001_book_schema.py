"""Documented placeholder migration for the in-memory Book model."""

MIGRATION_STAMP = {
    "name": "0001_book_schema",
    "dependencies": [],
    "operations": [
        {
            "operation": "CreateModel",
            "model": "Book",
            "fields": [
                ("title", "CharField"),
                ("author", "CharField"),
                ("published_year", "IntegerField"),
                ("isbn", "CharField"),
                ("created_at", "DateTimeField"),
                ("updated_at", "DateTimeField"),
            ],
        }
    ],
}
