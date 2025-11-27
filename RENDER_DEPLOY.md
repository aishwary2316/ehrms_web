# 🚀 Quick Deploy to Render - E-HRMS

## 🎯 5-Minute Deployment Guide

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Ready for deployment"
git remote add origin https://github.com/YOUR_USERNAME/ehrms.git
git push -u origin main
```

### Step 2: Create Render Account
- Go to https://render.com
- Sign up with GitHub

### Step 3: Deploy Database
1. New + → PostgreSQL
2. Name: `ehrms-db`, Region: Singapore, Plan: Free
3. **Copy Internal Database URL**

### Step 4: Deploy App
1. New + → Web Service
2. Connect GitHub repo
3. Settings:
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn app:app --bind 0.0.0.0:$PORT`
4. Add Environment Variables:
   ```
   DATABASE_URL = (paste from Step 3)
   SECRET_KEY = (generate: python -c "import secrets; print(secrets.token_hex(32))")
   FLASK_ENV = production
   ```
5. **Create Web Service**

### Step 5: Initialize Database
Go to Shell tab in Render:
```python
python << 'EOF'
from app import create_app, db
from models import User
app = create_app()
with app.app_context():
    db.create_all()
    sp = User(employee_id='SP001', name='Admin', email='admin@example.com', rank='SP')
    sp.set_password('password123')
    db.session.add(sp)
    db.session.commit()
EOF
```

### Step 6: Keep-Alive (Free Tier)
**Use UptimeRobot** (Best option):
1. Go to https://uptimerobot.com → Sign up
2. Add Monitor:
   - URL: `https://your-app.onrender.com/ping`
   - Interval: 5 minutes
3. Done! ✅

**Alternative - Cron-Job.org**:
1. Go to https://cron-job.org → Sign up
2. Add Cronjob:
   - URL: `https://your-app.onrender.com/ping`
   - Schedule: Every 14 minutes
3. Done! ✅

### Step 7: Test
- Visit: `https://your-app.onrender.com`
- Login: `SP001` / `password123`
- **Change password immediately!**

## 🎉 Done! Your app is live!

---

## 🔧 Quick Reference

### Your URLs
- **App**: `https://your-app-name.onrender.com`
- **Health**: `https://your-app-name.onrender.com/health`
- **Ping**: `https://your-app-name.onrender.com/ping`

### Free Tier Info
- ⚠️ Sleeps after 15 minutes (wakes on request in ~30s)
- ✅ Keep-alive prevents sleeping
- ✅ 750 hours/month free compute
- ✅ Free PostgreSQL (1GB, 90 days)

### Upgrade Options
- **Starter**: $7/month (no sleeping, better performance)
- **Pro**: $25/month (high availability, scaling)

### Troubleshooting
**App won't start?**
- Check Render logs
- Verify environment variables
- Check database connection

**Database errors?**
- Use Internal Database URL (not External)
- Check credentials
- Verify PostgreSQL is running

**Keep-alive not working?**
- Test: `curl https://your-app.onrender.com/ping`
- Check UptimeRobot/Cron-Job logs
- Try different service

### Update App
```bash
git add .
git commit -m "Update"
git push origin main
# Render auto-deploys!
```

---

## 📞 Need Help?

- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

**Happy Deploying! 🚀**
