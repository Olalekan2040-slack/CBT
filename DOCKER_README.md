# 🐳 N-TECH CBT Docker Deployment Guide

This guide will help you deploy the N-TECH CBT system using Docker containers for easy development and production deployment.

## 📋 Prerequisites

### Required Software:
- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Docker Compose** (usually included with Docker Desktop)
- **Git** (to clone the repository)

### System Requirements:
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 2GB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux

## 🚀 Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/Olalekan2040-slack/CBT.git
cd CBT

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment
Edit the `.env` file with your settings:
```env
DEBUG=0
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
DATABASE_URL=postgresql://postgres:postgres123@db:5432/ntech_cbt
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Start the Application

#### For Windows:
```cmd
setup-docker.bat
```

#### For Linux/Mac:
```bash
chmod +x setup-docker.sh
./setup-docker.sh
```

#### Manual Setup:
```bash
# Build containers
docker-compose build

# Start database
docker-compose up -d db redis

# Run migrations
docker-compose run --rm web python manage.py migrate

# Create superuser
docker-compose run --rm web python manage.py createsuperuser

# Start all services
docker-compose up -d
```

## 🌐 Access the Application

- **Main Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/ (if implemented)

## 🛠️ Docker Services

### Services Overview:
- **web**: Django application server
- **db**: PostgreSQL database
- **redis**: Redis cache and message broker
- **celery**: Background task worker
- **nginx**: Reverse proxy (production)

### Service Ports:
- **Web Application**: 8000
- **PostgreSQL**: 5432
- **Redis**: 6379
- **Nginx**: 80

## 📊 Management Commands

### View Logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
```

### Execute Commands:
```bash
# Django management commands
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Access Django shell
docker-compose exec web python manage.py shell

# Access database
docker-compose exec db psql -U postgres -d ntech_cbt
```

### Container Management:
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart specific service
docker-compose restart web

# Rebuild containers
docker-compose build --no-cache
```

## 🔧 Development Workflow

### Making Code Changes:
1. Edit your code locally
2. Changes are automatically reflected (volume mounted)
3. For dependency changes, rebuild: `docker-compose build web`

### Database Operations:
```bash
# Create new migration
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Reset database (CAREFUL!)
docker-compose down -v
docker-compose up -d db
docker-compose exec web python manage.py migrate
```

### Testing:
```bash
# Run tests
docker-compose exec web python manage.py test

# Run specific test
docker-compose exec web python manage.py test exams.tests.test_models
```

## 🚢 Production Deployment

### Environment Configuration:
```env
DEBUG=0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@db:5432/ntech_cbt
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
SECURE_SSL_REDIRECT=True
```

### Production Setup:
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Or with custom environment
docker-compose --env-file .env.prod up -d
```

### SSL/HTTPS Setup:
1. Obtain SSL certificates (Let's Encrypt recommended)
2. Update nginx configuration
3. Set `SECURE_SSL_REDIRECT=True` in environment

## 🛡️ Security Considerations

### Production Security:
- Change default passwords
- Use strong SECRET_KEY
- Enable HTTPS
- Configure firewall rules
- Regular security updates
- Database backups

### Environment Variables:
Never commit sensitive data to version control:
- Use `.env` files (not tracked)
- Use environment variables in production
- Rotate secrets regularly

## 📦 Backup and Restore

### Database Backup:
```bash
# Create backup
docker-compose exec db pg_dump -U postgres ntech_cbt > backup.sql

# Restore backup
docker-compose exec -T db psql -U postgres ntech_cbt < backup.sql
```

### Volume Backup:
```bash
# Backup volumes
docker run --rm -v cbt_postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres_backup.tar.gz /data
```

## 🐛 Troubleshooting

### Common Issues:

#### Port Already in Use:
```bash
# Check what's using the port
netstat -tulpn | grep :8000

# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use port 8001 instead
```

#### Database Connection Issues:
```bash
# Check database status
docker-compose logs db

# Restart database
docker-compose restart db
```

#### Permission Issues:
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Fix Docker permissions
sudo usermod -aG docker $USER
```

### Performance Optimization:
```bash
# Clean unused Docker resources
docker system prune -a

# Monitor resource usage
docker stats

# Increase memory limits
# Edit docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 1G
```

## 📈 Monitoring

### Health Checks:
```bash
# Check service health
docker-compose ps

# View resource usage
docker stats

# Monitor logs in real-time
docker-compose logs -f --tail=100
```

### Database Monitoring:
```bash
# Connect to database
docker-compose exec db psql -U postgres -d ntech_cbt

# Check database size
SELECT pg_size_pretty(pg_database_size('ntech_cbt'));

# Monitor connections
SELECT count(*) FROM pg_stat_activity;
```

## 🚀 Next Steps

After successful deployment:

1. **Configure Email**: Set up SMTP for production emails
2. **Set up Monitoring**: Consider Sentry for error tracking
3. **Database Optimization**: Configure PostgreSQL for production
4. **Caching**: Implement Redis caching strategies
5. **CDN**: Set up static file CDN for better performance
6. **Code Editor**: Ready for the integrated code editor feature!

## 🆘 Support

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify configuration: Review `.env` file
3. Check Docker status: `docker-compose ps`
4. Restart services: `docker-compose restart`

The N-TECH CBT system is now containerized and ready for scalable deployment! 🎉
