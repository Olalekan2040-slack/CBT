@echo off
REM N-TECH CBT Docker Setup Script for Windows

echo 🚀 Setting up N-TECH CBT System with Docker...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ✅ Please edit .env file with your configuration before continuing.
    echo Press any key when ready...
    pause >nul
)

REM Build and start services
echo 🔨 Building Docker containers...
docker-compose build

echo 🗄️ Starting database and Redis...
docker-compose up -d db redis

echo ⏳ Waiting for database to be ready...
timeout /t 10 /nobreak >nul

echo 📊 Running database migrations...
docker-compose run --rm web python manage.py migrate

echo 👤 Creating superuser (optional)...
set /p createuser="Would you like to create a superuser? (y/n): "
if /i "%createuser%"=="y" (
    docker-compose run --rm web python manage.py createsuperuser
)

echo 📂 Collecting static files...
docker-compose run --rm web python manage.py collectstatic --noinput

echo 🚀 Starting all services...
docker-compose up -d

echo.
echo ✅ N-TECH CBT System is now running!
echo.
echo 🌐 Access the application at: http://localhost:8000
echo 🔧 Admin panel: http://localhost:8000/admin/
echo 📊 View logs: docker-compose logs -f
echo 🛑 Stop services: docker-compose down
echo.
echo 🎉 Happy coding with N-TECH CBT!
pause
