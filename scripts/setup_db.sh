#!/bin/bash

set -e

# Function: Check for required tools
check_tools() {
    for tool in psql createdb pg_isready; do
        if ! command -v "$tool" &> /dev/null; then
            echo "❌ Required tool '$tool' is not installed."
            echo "💡 Please install PostgreSQL client tools."
            return 1
        fi
    done
}

# Function: Load environment variables
load_env() {
    if [ -f .env ]; then
        echo "✅ Loading environment variables from .env"
        set -a
        source .env
        set +a
    else
        echo "❌ .env file not found!"
        echo "💡 Please copy .env.example to .env and configure it."
        return 1
    fi
}

# Function: Set defaults
set_defaults() {
    DBNAME=${DBNAME:-django_app}
    DBUSER=${DBUSER:-postgres}
    DBHOST=${DBHOST:-localhost}
    DBPORT=${DBPORT:-5432}
    echo "📋 Database Configuration:"
    echo "   Host: $DBHOST:$DBPORT"
    echo "   Database: $DBNAME"
    echo "   User: $DBUSER"
    if [ -z "$DBPASSWORD" ]; then
        echo "⚠️  DBPASSWORD is not set in .env (may be required for remote DBs)"
    fi
}

# Function: Check PostgreSQL status
check_postgres() {
    if ! pg_isready -h "$DBHOST" -p "$DBPORT" > /dev/null 2>&1; then
        echo "❌ PostgreSQL is not running on $DBHOST:$DBPORT"
        echo "💡 Please start PostgreSQL first:"
        echo "   macOS: brew services start postgresql"
        echo "   Ubuntu: sudo systemctl start postgresql"
        echo "   Windows: net start postgresql-x64-[version]"
        return 1
    fi
    echo "✅ PostgreSQL is running"
}

# Function: Create database if needed
create_database() {
    DB_EXISTS=$(PGPASSWORD="$DBPASSWORD" psql -h "$DBHOST" -p "$DBPORT" -U "$DBUSER" -lqt | cut -d \| -f 1 | grep -w "$DBNAME" | wc -l)
    if [ "$DB_EXISTS" -eq "0" ]; then
        echo "🔨 Creating database '$DBNAME'..."
        if PGPASSWORD="$DBPASSWORD" createdb -h "$DBHOST" -p "$DBPORT" -U "$DBUSER" "$DBNAME"; then
            echo "✅ Database '$DBNAME' created successfully!"
        else
            echo "❌ Failed to create database '$DBNAME'"
            echo "💡 Please check your credentials and permissions."
            return 1
        fi
    else
        echo "✅ Database '$DBNAME' already exists"
    fi
}

# Function: Test database connection
test_connection() {
    echo "🔍 Testing database connection..."
    if PGPASSWORD="$DBPASSWORD" psql -h "$DBHOST" -p "$DBPORT" -U "$DBUSER" -d "$DBNAME" -c "SELECT 1;" > /dev/null 2>&1; then
        echo "✅ Database connection successful!"
    else
        echo "❌ Failed to connect to database"
        echo "💡 Please check your database credentials in .env file"
        return 1
    fi
}

echo "PostgreSQL Database Setup"
echo "========================="

check_tools || exit 1
load_env || exit 1
set_defaults
check_postgres || exit 1
create_database || exit 1
test_connection || exit 1

echo ""
echo "🎉 Database setup completed successfully!"
echo "📋 Next steps:"
echo "  1. Edit your .env file with correct settings if needed"
echo "  2. Run migrations: python manage.py migrate"
echo "  3. Start development server: python manage.py runserver"
echo "  4. For Celery: celery -A conf worker --loglevel=info"
echo "  5. Visit http://127.0.0.1:8000 to see your app!"
echo "📖 Documentation: Check README.md for more details"
echo ""
