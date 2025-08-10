#!/bin/bash

# N-TECH CBT Docker Setup Script
echo "🚀 Setting up N-TECH CBT System with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Please edit .env file with your configuration before continuing."
    echo "Press Enter when ready..."
    read
fi

# Build and start services
echo "🔨 Building Docker containers..."
docker-compose build

echo "🗄️ Starting database and Redis..."
docker-compose up -d db redis

echo "⏳ Waiting for database to be ready..."
sleep 10

echo "📊 Running database migrations..."
docker-compose run --rm web python manage.py migrate

echo "👤 Creating superuser (optional)..."
echo "Would you like to create a superuser? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    docker-compose run --rm web python manage.py createsuperuser
fi

echo "📂 Collecting static files..."
docker-compose run --rm web python manage.py collectstatic --noinput

echo "🚀 Starting all services..."
docker-compose up -d

echo ""
echo "✅ N-TECH CBT System is now running!"
echo ""
echo "🌐 Access the application at: http://localhost:8000"
echo "🔧 Admin panel: http://localhost:8000/admin/"
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop services: docker-compose down"
echo ""
echo "🎉 Happy coding with N-TECH CBT!"
