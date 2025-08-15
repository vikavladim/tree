import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

REQUIREMENTS_FILE = "requirements.txt"
VENV_DIR = "venv"
PYTHON_VERSION = "3.12"


class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'


def print_color(text, color):
    print(f"{color}{text}{Colors.NC}")


def run_command(command, shell=False, cwd=None):
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print_color(
            f"Ошибка при выполнении команды: {' '.join(command)}", Colors.RED)
        print_color(e.stderr, Colors.RED)
        sys.exit(1)


def check_python_version():
    print_color("Проверка версии Python...", Colors.YELLOW)
    if sys.version_info < (3, 12):
        print_color(f"Требуется Python {PYTHON_VERSION} или выше", Colors.RED)
        sys.exit(1)
    print_color(f"Python {platform.python_version()} обнаружен", Colors.GREEN)


def setup_venv():
    if not Path(VENV_DIR).exists():
        if platform.system() == "Linux":
            print_color("Проверка системных зависимостей для Linux...",
                        Colors.YELLOW)
            try:
                subprocess.run(["dpkg", "-s", f"python{PYTHON_VERSION}-venv"],
                               check=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                print_color(
                    f"Установка python{PYTHON_VERSION}-venv...", Colors.YELLOW)
                run_command(["sudo", "apt-get", "update"])
                run_command(["sudo", "apt-get", "install", "-y",
                            f"python{PYTHON_VERSION}-venv"])
        print_color("Создание виртуального окружения...", Colors.YELLOW)
        run_command([sys.executable, "-m", "venv", VENV_DIR])

    if platform.system() == "Windows":
        activate_script = Path(VENV_DIR) / "Scripts" / "activate.bat"
    else:
        activate_script = Path(VENV_DIR) / "bin" / "activate"

    return activate_script


def install_dependencies():
    print_color("Установка зависимостей...", Colors.YELLOW)
    pip_executable = str(Path(
        VENV_DIR) / ("Scripts" if platform.system() == "Windows" else "bin") / "pip")
    run_command([pip_executable, "install", "-r", REQUIREMENTS_FILE])


def django_manage(command):
    python_executable = str(Path(
        VENV_DIR) / ("Scripts" if platform.system() == "Windows" else "bin") / "python")
    run_command([python_executable, "manage.py"] + command)


def handle_migrations():
    print_color("Создание миграций...", Colors.YELLOW)
    shutil.copyfile('./url/urls_initial.py', './tree_menu/urls.py')
    django_manage(["makemigrations"])
    print_color("Применение миграций...", Colors.YELLOW)
    django_manage(["migrate"])
    shutil.copyfile('./url/urls.py', './tree_menu/urls.py')
    django_manage(["migrate"])
    print_color("Все миграции применены", Colors.GREEN)


def execute_sql_file(sql_file="start.sql"):
    print_color(f"Выполнение SQL-файла {sql_file}...", Colors.YELLOW)
    try:
        subprocess.run(
            [str(Path(VENV_DIR) / ("Scripts" if platform.system() == "Windows" else "bin") / "python"),
                "insert.py"],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            check=True
        )
        print_color("Суперпользователь успешно создан", Colors.GREEN)
    except subprocess.CalledProcessError:
        print_color("Ошибка при создании суперпользователя", Colors.RED)
    except KeyboardInterrupt:
        print_color("\nСоздание суперпользователя отменено", Colors.YELLOW)


def main():
    print_color("\n=== Настройка Django-проекта ===", Colors.GREEN)

    check_python_version()
    setup_venv()
    install_dependencies()

    handle_migrations()

    create_superuser = input(
        "Создать суперпользователя? (y/n): ").strip().lower()
    if create_superuser == 'y':
        try:
            subprocess.run(
                [str(Path(VENV_DIR) / ("Scripts" if platform.system() == "Windows" else "bin") / "python"),
                 "manage.py", "createsuperuser"],
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
                check=True
            )
            print_color("Суперпользователь успешно создан", Colors.GREEN)
        except subprocess.CalledProcessError:
            print_color("Ошибка при создании суперпользователя", Colors.RED)
        except KeyboardInterrupt:
            print_color("\nСоздание суперпользователя отменено", Colors.YELLOW)

    print_color("\n=== Заполнение БД тестовыми данными ===", Colors.GREEN)
    execute_sql_file()

    print_color("\nЗапуск сервера...", Colors.GREEN)
    print_color(
        "Сервер будет доступен по адресу: http://127.0.0.1:8000/", Colors.YELLOW)
    print_color(
        "Админка: http://127.0.0.1:8000/admin/", Colors.YELLOW)
    django_manage(["runserver"])


if __name__ == "__main__":
    main()
