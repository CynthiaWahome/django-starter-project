import logging
import os
import shlex
import subprocess
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def run_command(cmd, description):
    """Run command with proper error handling."""
    logger.info(f"{description}...")
    try:
        result = subprocess.run(shlex.split(cmd), check=True, capture_output=True, text=True)  # noqa: S603
        logger.info(f"{description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"{description} failed: {e.stderr}")
        return None

def check_requirements():
    """Check if required tools are installed."""
    logger.info("Checking requirements...")
    try:
        subprocess.run(["/usr/bin/uv", "--version"], check=True, capture_output=True)
        logger.info("UV is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("UV is not installed. Installing...")
        os.system("curl -LsSf https://astral.sh/uv/install.sh | sh")  # noqa: S605, S607
        logger.info("UV installed! Please restart your terminal and run this script again.")
        sys.exit(0)
    logger.info(f"Python {sys.version.split()[0]} is compatible")

def setup_environment():
    """Setup development environment."""
    logger.info("Setting up development environment...")
    if not Path(".env").exists():
        if Path(".env.example").exists():
            run_command("cp .env.example .env", "Creating .env file")
            logger.info("Please edit .env file with your settings")
        else:
            create_default_env()
    else:
        logger.info(".env file already exists")

def create_default_env():
    """Create a basic .env file."""
    env_content = """# Django Core
SECRET_KEY=django-insecure-change-this-in-production-$(date +%s)
DEBUG=True
ENV=dev

# Database (using SQLite for development)
DB_URL=sqlite:///db.sqlite3
# In your .env file
DB_URL=postgres://username:@localhost:5432/dbname

# Cache & Tasks
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Security
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Monitoring
USE_SENTRY=False
"""
    with open(".env", "w") as f:
        f.write(env_content)
    logger.info("Created default .env file")

def setup_database():
    """Setup and migrate database."""
    logger.info("Setting up database...")
    if not run_command("uv run python manage.py check", "Checking Django configuration"):
        logger.error("Django configuration has issues")
        return False
    run_command("uv run python manage.py makemigrations", "Creating migrations")
    if not run_command("uv run python manage.py migrate", "Running migrations"):
        logger.warning("Database migration had issues, but continuing...")
    if not run_command("uv run python manage.py collectstatic --noinput", "Collecting static files"):
        logger.warning("Static file collection had issues, but continuing...")
    return True

def main():
    """Main setup function."""
    logger.info("Modern Django Starter Project Setup")
    logger.info("=" * 50)
    check_requirements()
    setup_environment()
    logger.info("Installing dependencies...")
    if not run_command("uv sync", "Installing dependencies"):
        logger.error("Failed to install dependencies")
        sys.exit(1)
    run_command("uv run pre-commit install", "Setting up pre-commit hooks")
    setup_database()
    logger.info("Setup completed successfully!")
    logger.info("Next steps:")
    logger.info("  1. Edit .env file if needed")
    logger.info("  2. Start development server: uv run python manage.py runserver")
    logger.info("  3. Visit http://127.0.0.1:8000")
    logger.info("Test your setup:")
    logger.info("  • Run tests: uv run pytest")
    logger.info("  • Check code quality: uv run ruff check .")
    logger.info("  • Type check: uv run mypy .")

if __name__ == "__main__":
    main()
