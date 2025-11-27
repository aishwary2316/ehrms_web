# E-HRMS Deployment Guide

## 🚀 Production Deployment Checklist

### Prerequisites
- Python 3.8 or higher
- Web server (Apache/Nginx)
- SSL Certificate
- Production database (SQLite/PostgreSQL/MySQL)

### 1. Environment Setup

```bash
# Create production environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create `.env` file in project root:

```env
# Production Settings
FLASK_ENV=production
SECRET_KEY=your-very-long-secure-random-key-here
DATABASE_URI=sqlite:///ehrms_production.db

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# File Upload
MAX_CONTENT_LENGTH=5242880
UPLOAD_FOLDER=uploads

# Email (if configured)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-app-password
```

### 3. Database Initialization

```bash
# Initialize production database
python init_db_fresh.py

# Verify database
python check_db.py
```

### 4. Security Hardening

1. **Change default passwords** for all users
2. **Enable HTTPS** - Configure SSL certificate
3. **Set strong SECRET_KEY** - Generate random key
4. **Configure firewall** - Allow only necessary ports
5. **Enable rate limiting** - Prevent brute force attacks
6. **Regular backups** - Schedule database backups
7. **Update dependencies** - Keep all packages up to date

### 5. Production Server Setup

#### Option A: Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

#### Option B: Using uWSGI

```bash
# Install uWSGI
pip install uwsgi

# Create uwsgi.ini
cat > uwsgi.ini << EOF
[uwsgi]
module = app:create_app()
callable = app
master = true
processes = 4
socket = ehrms.sock
chmod-socket = 660
vacuum = true
die-on-term = true
EOF

# Run
uwsgi --ini uwsgi.ini
```

### 6. Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL Configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /path/to/EHRMS_NEW/static;
        expires 30d;
    }
    
    location /uploads {
        alias /path/to/EHRMS_NEW/uploads;
        expires 7d;
    }
}
```

### 7. Systemd Service (Linux)

Create `/etc/systemd/system/ehrms.service`:

```ini
[Unit]
Description=E-HRMS Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/EHRMS_NEW
Environment="PATH=/path/to/EHRMS_NEW/venv/bin"
ExecStart=/path/to/EHRMS_NEW/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ehrms
sudo systemctl start ehrms
sudo systemctl status ehrms
```

### 8. Maintenance

#### Daily Tasks
- Monitor application logs
- Check disk space
- Review security alerts

#### Weekly Tasks
- Database backup
- Review user activity logs
- Check for system updates

#### Monthly Tasks
- Security audit
- Performance optimization
- Update dependencies

### 9. Backup Strategy

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/ehrms"
mkdir -p $BACKUP_DIR

# Backup database
cp ehrms_production.db $BACKUP_DIR/ehrms_$DATE.db

# Backup uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz uploads/

# Keep only last 30 days
find $BACKUP_DIR -name "ehrms_*.db" -mtime +30 -delete
find $BACKUP_DIR -name "uploads_*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
EOF

chmod +x backup.sh

# Add to crontab (daily at 2 AM)
0 2 * * * /path/to/backup.sh
```

### 10. Monitoring

#### Application Logs
```bash
# View application logs
tail -f /var/log/ehrms/app.log

# Search for errors
grep ERROR /var/log/ehrms/app.log
```

#### Performance Monitoring
- CPU usage
- Memory usage
- Disk I/O
- Network traffic
- Response times

### 11. Troubleshooting

#### Common Issues

**Database Locked**
```bash
# Check for stale connections
lsof ehrms_production.db
```

**Permission Denied**
```bash
# Fix file permissions
chown -R www-data:www-data /path/to/EHRMS_NEW
chmod -R 755 /path/to/EHRMS_NEW
```

**502 Bad Gateway**
```bash
# Check if application is running
systemctl status ehrms

# Check logs
journalctl -u ehrms -f
```

### 12. Security Best Practices

✅ Use HTTPS only
✅ Enable CSRF protection
✅ Implement rate limiting
✅ Regular security audits
✅ Keep dependencies updated
✅ Use strong passwords
✅ Enable two-factor authentication (future)
✅ Regular backups
✅ Monitor logs for suspicious activity
✅ Use environment variables for secrets

### 13. Performance Optimization

- Enable database query caching
- Use Redis for session storage
- Implement CDN for static files
- Enable gzip compression
- Optimize database indexes
- Monitor and optimize slow queries

### 14. Support & Maintenance

For issues and updates, contact the system administrator.

**System Requirements:**
- CPU: 2+ cores
- RAM: 4GB minimum (8GB recommended)
- Storage: 20GB minimum
- Network: Stable internet connection

**Tested On:**
- Ubuntu 20.04/22.04 LTS
- Windows Server 2019/2022
- Python 3.8/3.9/3.10/3.11

---

## 📞 Emergency Contacts

**Technical Support:** [Your Contact]
**System Administrator:** [Admin Contact]
**Database Administrator:** [DBA Contact]

---

**Last Updated:** October 2025
**Version:** 1.0.0
