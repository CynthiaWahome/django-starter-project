# 🚀 Modern Django Starter Project

> Quite the opionionated Django starter template

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Django 5.2](https://img.shields.io/badge/django-5.2-green.svg)](https://docs.djangoproject.com/en/5.2/)
[![UV](https://img.shields.io/badge/dependency_manager-uv-purple.svg)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/badge/linter-ruff-red.svg)](https://github.com/astral-sh/ruff)
[![MyPy](https://img.shields.io/badge/type_checker-mypy-blue.svg)](https://mypy.readthedocs.io/)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-brightgreen.svg)](https://docs.github.com/en/github/administering-a-repository/keeping-your-dependencies-updated-automatically)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

This template assumes you want:

- ⚡ **Speed over flexibility** (UV instead of Poetry/pip)
- 🧹 **Fewer tools that do more** (Ruff instead of Black + Flake8 + isort)
- 🔍 **Type safety** (because `Any` is not a type)
- 🤖 **Automation** (Dependabot keeping you current)
- 🎨 **Consistency** (standardized everything)

If you disagree with these choices, this template will make you _very_ unhappy. Consider yourself warned! 😈

## 🎖 Tool Choices

| Category               | Choice                                                                                                                     | Why This & Not That                                                                                |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Dependency Manager** | [UV](https://github.com/astral-sh/uv)                                                                                      | 10x faster than Poetry. Life's too short for slow installs.                                        |
| **Code Formatter**     | [Ruff](https://github.com/astral-sh/ruff)                                                                                  | Replaces Black + Flake8 + isort + 12 other tools. One tool to rule them all.                       |
| **Type Checker**       | [MyPy](https://mypy.readthedocs.io/)                                                                                       | Because `def process_data(data):` tells us nothing about what happens when you pass it a sandwich. |
| **Database**           | [PostgreSQL](https://www.postgresql.org/)                                                                                  | SQLite is for prototypes. This is for production.                                                  |
| **Task Queue**         | [Celery](http://www.celeryproject.org/) + [Redis](https://redis.io/)                                                       | Send emails without blocking the UI. Revolutionary!                                                |
| **Testing**            | [PyTest](https://docs.pytest.org/) + [Hypothesis](https://hypothesis.readthedocs.io/)                                      | Property-based testing finds bugs you didn't know you had.                                         |
| **Security Scanner**   | [Bandit](https://bandit.readthedocs.io/)                                                                                   | Catches security issues before your CISO does.                                                     |
| **Dependency Updates** | [Dependabot](https://docs.github.com/en/github/administering-a-repository/keeping-your-dependencies-updated-automatically) | Auto-updates dependencies so you don't have to remember.                                           |
| **Web Server**         | [Caddy](https://caddyserver.com/)                                                                                          | Automatic HTTPS. It's 2025, people!                                                                |
| **Containerization**   | [Docker](https://www.docker.com/)                                                                                          | "Works on my machine" → "Works on every machine"                                                   |
| **Static Assets**      | [Webpack](https://webpack.js.org/)                                                                                         | Because `<script src="jquery-1.4.2-final-FINAL-v2.js">` is not a build system.                     |

## 📋 Prerequisites (The Boring But Necessary Stuff)

**Required (or your project will explode):**

- Python 3.12+ (3.11 if you enjoy living dangerously)
- PostgreSQL 12+ (because you're not a savage)
- Redis 6+ (for caching and background tasks)
- UV package manager (the future is here)

**Optional (for the full experience):**

- Node.js 18+ (for asset compilation)
- Docker (for "works on everyone's machine")

## 🚀 Getting Started

### Method 1: Use This Template (Recommended for Humans)

**Click "Use this template"**

Instead of running `django-admin startproject` to start your new project, clone this repo in a directory of your choosing

```bash
git clone https://github.com/CynthiaWahome/django-starter-project.git django-starter
cd django-starter
```

### Method 2 :**One command to rule them all:**

```bash
python scripts/setup_project.py
```

This magical script will:

- Install UV (if you forgot)
- Install all dependencies
- Setup pre-commit hooks (no more "oops" commits)
- Create and migrate database
- Collect static files
- Make you coffee ☕ (just kidding, but everything else is real)

At this point you may start a clean git repo by removing the `.git` directory and then running `git init`.

```bash
cp .env.example .env
```

### 4) Run the project

You have two choices, either you turn every service on your own or you use docker-compose

#### A) Use Docker Compose

```bash
docker-compose up --build
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) and you'll see your site up and running 🧘‍♀️

#### B) Run by yourself

Make sure you have `redis-server` running and finally on 3 separate consoles run:

**server**

```bash
uv run python manage.py runserver
```

**worker**

```bash
uv run celery -A conf worker --loglevel=info
```

**webpack**

```bash
cd assets
npm install
npm run dev
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) and you'll see your site up and running 🧘‍♀️

## 📁 Project Structure (Organized Like Your Life Should Be)

```
django-starter-project/
├── 📁 apps/                   # Your Django applications
│   ├── 📁 common/             # Shared utilities
│   ├── 📁 misc/               # Miscellaneous utilities
│   └── 📁 users/              # User management
├── 📁 assets/                 # Frontend assets (SCSS, JS, images)
├── 📁 conf/                   # Django project configuration
│   ├── settings.py           # The main settings file
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI entrypoint
│   └── celery.py             # Celery configuration
├── 📁 scripts/                # Utility and setup scripts
│   ├── 📄 entrypoint-django.sh # Docker entrypoint script for Django
│   ├── 📄 entrypoint-celery.sh # Docker entrypoint script for Celery
│   ├── setup_db.sh           # Database setup script
│   └── setup_project.py      # Project setup automation
├── 📁 templates/              # Django templates
├── 📁 tests/                  # Test suite
│   ├── conftest.py           # Pytest configuration
│   ├── test_int.py           # Integration tests
│   └── test_responses.py     # Response tests
├── 📄 .env.example           # Environment variable template
├── 📄 .gitignore             # Git ignore rules
├── 📄 .pre-commit-config.yaml # Pre-commit hook definitions
├── 📄 Caddyfile              # Caddy web server configuration
├── 📄 docker-compose.yml     # Docker Compose orchestration
├── 📄 Dockerfile             # Main container definition
├── 📄 manage.py               # Django's command-line utility
├── 📄 pyproject.toml         # Project metadata and dependencies (PEP 621)
└── 📄 README.md              # This file
```

## 🎯 API Standards (Because Consistency Is Beautiful)

All API endpoints follow a standardized response format:

### Success Response

```json
{
  "success": true,
  "message": "Data retrieved successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "created_at": "2025-01-01T00:00:00Z"
    }
  },
  "error": null,
  "metadata": {}
}
```

### Error Response

```json
{
  "success": false,
  "message": "Validation failed",
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "details": {
      "email": ["This field is required."],
      "password": ["Password must be at least 8 characters."]
    }
  },
  "metadata": {}
}
```

### Paginated Response

```json
{
  "success": true,
  "message": "Users retrieved successfully",
  "data": [
    { "id": 1, "name": "Alice" },
    { "id": 2, "name": "Bob" }
  ],
  "error": null,
  "metadata": {
    "pagination": {
      "total_items": 42,
      "total_pages": 5,
      "current_page": 1,
      "per_page": 10,
      "has_next": true,
      "has_previous": false
    }
  }
}
```

## ♻️ Zed Editor Settings

This project includes optimized Zed configuration in `.zed/settings.json`:

```json
{
  "format_on_save": "on",
  "formatter": "ruff",
  "linter": "ruff",
  "tab_size": 4,

  "languages": {
    "Python": {
      "format_on_save": "on",
      "formatter": {
        "external": {
          "command": "uv",
          "arguments": ["run", "ruff", "format", "-"]
        }
      }
    }
  }
}
```

## 🔒 Security Features (Because Hackers Don't Sleep)

- **Django 5.2** with latest security patches
- **CSP headers** configured
- **HTTPS redirect** in production
- **Secure cookie settings**
- **SQL injection protection** via ORM
- **XSS protection** with template escaping
- **CSRF protection** enabled
- **Security middleware** stack
- **Bandit security scanner** in CI/CD

## 🎉 What's Next? (Your Journey Begins)

After setup, you're ready to:

1. **Create your first app**: `uv run python manage.py startapp your_app`
2. **Move it to apps directory**: `mv your_app apps/`
3. **Add to INSTALLED_APPS**: Update `conf/settings/base.py`
4. **Create models**: Define your data structure
5. **Write tests first**: TDD for the win
6. **Build APIs**: Use the standardized response format
7. **Deploy with confidence**: Follow the deployment checklist

## 🙏 Credits & Inspiration

This template stands on the shoulders of giants:

- **Original foundation**: [fceruti/django-starter-project](https://github.com/fceruti/django-starter-project) - The OG Django starter
- **Enterprise inspiration**: [wemake-services/wemake-django-template](https://github.com/wemake-services/wemake-django-template) - Serious business template
- **Documentation style**: [FastAPI](https://fastapi.tiangolo.com/) - Made docs fun again
- **Modern tooling**: [Astral](https://astral.sh/) - UV and Ruff creators
- **Dependabot**: GitHub's automated dependency updates

## 📄 License

MIT License - Use it, abuse it, make money with it. Just don't blame me when your startup becomes a unicorn and you forget to invite me to the IPO party.
