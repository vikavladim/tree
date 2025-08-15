from django.db import connection
import django
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tree_menu.settings')
django.setup()

sql_file = "start.sql"
try:
    with connection.cursor() as cursor:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
    print("SQL-файл успешно выполнен")
except Exception as e:
    print("Ошибка при выполнении SQL: {e}")
