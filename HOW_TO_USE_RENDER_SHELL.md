# How to Access Render Shell 🖥️

## Step-by-Step Guide to Find Render Shell

### 1. Go to Render Dashboard
Visit: https://dashboard.render.com/

### 2. Find Your Web Service
- You'll see a list of your services
- Click on your **E-HRMS web service** (the one you just deployed)

### 3. Locate the Shell Tab
Once you're on your service page, look at the **left sidebar**. You'll see:

```
📊 Overview
📋 Logs
🖥️ Shell          ← Click here!
⚙️ Settings
🔧 Environment
📊 Metrics
```

### 4. Click "Shell"
- Click on the **"Shell"** option in the left sidebar
- Render will open a terminal connected to your running container

### 5. Run Commands
Once the shell opens, you can run commands like:

```bash
# Initialize your database
python init_render_db.py

# Check Python version
python --version

# List files
ls -la

# Check environment variables
echo $DATABASE_URL
```

## Visual Guide

```
┌─────────────────────────────────────────────────────────┐
│  Render Dashboard                                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Your Services:                                         │
│  ┌──────────────────────────────────────────┐          │
│  │  ehrms (Web Service)                      │          │
│  │  Status: ● Live                           │ ← Click  │
│  │  https://ehrms-xxxx.onrender.com         │          │
│  └──────────────────────────────────────────┘          │
│                                                          │
└─────────────────────────────────────────────────────────┘

After clicking on your service:

┌─────────────────────────────────────────────────────────┐
│  ehrms                                     ● Live       │
├──────────────┬──────────────────────────────────────────┤
│              │                                           │
│  📊 Overview │  Service Details                         │
│  📋 Logs     │  Last deploy: 2 minutes ago             │
│  🖥️ Shell    │← Click here to open terminal             │
│  ⚙️ Settings │                                          │
│  🔧 Env      │                                          │
│  📊 Metrics  │                                          │
│              │                                           │
└──────────────┴──────────────────────────────────────────┘

Shell will open in the same page:

┌─────────────────────────────────────────────────────────┐
│  ehrms > Shell                                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  $ _                                                    │
│                                                          │
│  Type commands here...                                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Quick Commands for Shell

### Initialize Database
```bash
python init_render_db.py
```
Type `yes` when prompted to confirm.

### Check if Database is Connected
```bash
python -c "from app import app, db; app.app_context().push(); db.session.execute(db.text('SELECT 1')); print('✅ Database connected!')"
```

### List All Tables
```bash
python -c "from app import app, db; app.app_context().push(); print([table for table in db.metadata.tables.keys()])"
```

### Check Environment
```bash
env | grep DATABASE_URL
env | grep FLASK_ENV
```

## 🆓 If Shell Is Not Available on Free Tier

### ✅ Automatic Database Initialization (Already Configured!)

**Good News**: Your app is now configured to automatically initialize the database on first startup!

When you deploy to Render, the app will:
1. Check if database tables exist
2. If not, create all tables automatically
3. Create the default SP admin user (SP001 / password123)
4. Log everything in the deployment logs

**Nothing to do manually!** Just deploy and the database will be ready.

### How to Verify Initialization

After deployment, check the **Logs** tab in Render Dashboard:

```
📦 Database tables don't exist, creating them...
✅ Database tables created
👤 Creating default SP admin user...
✅ Default SP user created (SP001 / password123)
⚠️  IMPORTANT: Change this password after first login!
```

### Alternative Methods (if needed)

#### Method 1: Local Initialization (Recommended if Shell not available)

Run this on your local machine (it will connect to Render's PostgreSQL):

```powershell
python init_render_db.py
```

This connects to your Render database remotely and initializes it.

#### Method 2: Force Re-initialization

If you need to reset the database:
1. Delete the web service in Render
2. Delete the PostgreSQL database in Render
3. Create new PostgreSQL database (get new URL)
4. Update DATABASE_URL in .env and Render environment variables
5. Redeploy - database will auto-initialize

## Alternative: SSH Access (Not Available on Free Tier)

SSH access requires a paid plan. Use the automatic initialization method above instead!

## Troubleshooting

### "Shell" Tab Not Visible?
- Make sure your service has been deployed at least once
- Refresh the page
- Check if you're on the correct service page

### Shell Won't Load?
- Check if your service is running (Status: ● Live)
- If service crashed, check the "Logs" tab first
- Fix any deployment errors before using Shell

### Commands Not Working?
```bash
# Check Python path
which python

# Check current directory
pwd

# List files
ls -la
```

## 🎯 What You Need to Do

1. **Go to**: https://dashboard.render.com/
2. **Click**: Your E-HRMS web service
3. **Click**: "Shell" in the left sidebar
4. **Run**: `python init_render_db.py`
5. **Type**: `yes` to confirm
6. **Done**: Database initialized! 🎉

---

**Need More Help?**

If the shell doesn't appear or you have issues:
- Check Logs tab first (to see if app is running)
- Make sure deployment succeeded
- Verify your service is in "Live" status

The Shell is essentially a terminal that runs inside your deployed container on Render's servers!
