# Default Login Credentials 🔐

After deployment, your E-HRMS system will have the following default users created automatically:

## 📋 All Default Users

| Rank | Employee ID | Password | Email | Designation |
|------|------------|----------|-------|-------------|
| **SP** | `SP001` | `sp123` | sp@police.gov.in | Superintendent of Police |
| **ASP** | `ASP001` | `asp123` | asp@police.gov.in | Additional Superintendent of Police |
| **SDPO** | `SDPO001` | `sdpo123` | sdpo@police.gov.in | Sub-Divisional Police Officer |
| **Inspector** | `INS001` | `ins123` | inspector@police.gov.in | Station Officer In-Charge |
| **SI** | `SI001` | `si123` | si@police.gov.in | Sub-Inspector |
| **ASI** | `ASI001` | `asi123` | asi@police.gov.in | Assistant Sub-Inspector |
| **HC** | `HC001` | `hc123` | hc@police.gov.in | Head Constable |
| **C** | `C001` | `c123` | constable@police.gov.in | Constable |

## 🎯 Quick Login Guide

### For Admin/Management (SP)
```
Employee ID: SP001
Password: sp123
```

### For Testing Different Ranks
Each rank has a default user with pattern:
- **Employee ID**: `[RANK]001` (e.g., ASP001, SDPO001, INS001)
- **Password**: `[rank]123` (e.g., asp123, sdpo123, ins123)

## ⚠️ Security Warning

**IMPORTANT**: These are default credentials for initial setup only!

### After First Deployment:

1. ✅ Login with SP001 / sp123
2. ✅ Change SP001 password immediately
3. ✅ Go to Users menu and update all default passwords
4. ✅ Delete any unused default accounts
5. ✅ Create real user accounts with proper credentials

## 🔒 How to Change Password

1. Login with default credentials
2. Click on your **Profile** (top-right corner)
3. Click **"Edit Profile"**
4. Enter new password
5. Click **"Save Changes"**

## 👥 User Management

### As SP (Admin), you can:
- Add new users with custom credentials
- Edit existing user passwords
- Deactivate/activate users
- Assign users to stations
- Manage user roles and permissions

### To Add New Users:
1. Login as SP001
2. Go to **Users** menu
3. Click **"Add New User"**
4. Fill in details with secure password
5. Click **"Submit"**

## 🎭 Testing Different User Roles

Use the default accounts to test role-based features:

### SP (SP001) - Can:
- Approve all leaves (final approval)
- View all reports
- Manage all users and stations
- Issue transfer orders
- View system-wide statistics

### ASP (ASP001) - Can:
- View reports for assigned areas
- Monitor personnel
- Review leave applications
- Approve certain requests

### SDPO (SDPO001) - Can:
- Approve leaves for subdivision
- Manage subdivision personnel
- View subdivision reports
- Forward leaves to SP

### Inspector (INS001) - Can:
- Manage station as OIC
- Forward leaves to SDPO
- Mark attendance
- Assign duties
- Manage station personnel

### Lower Ranks (SI, ASI, HC, C) - Can:
- Apply for leaves
- View own profile
- Check attendance
- View duty roster
- Submit grievances

## 📱 Login URL

```
https://your-app-name.onrender.com/auth/login
```

## 🔄 Password Reset (If Needed)

If you forget a password, you can reset it:

### Option 1: As Admin (SP)
1. Login as SP
2. Go to Users
3. Edit the user
4. Set new password

### Option 2: Database Reset
Run this in Render Shell or locally:
```python
python init_render_db.py
```
Type `yes` to recreate all default users (⚠️ This will reset the database!)

## 📊 User Hierarchy

```
SP (Superintendent of Police)
└── ASP (Additional SP)
    └── SDPO (Sub-Divisional Police Officer)
        └── Inspector (Station OIC)
            └── SI (Sub-Inspector)
                └── ASI (Assistant Sub-Inspector)
                    └── HC (Head Constable)
                        └── C (Constable)
```

## ✅ Best Practices

1. **Change all default passwords** immediately after deployment
2. **Delete unused default accounts** after creating real users
3. **Use strong passwords** (min 8 characters, mix of letters/numbers/symbols)
4. **Don't share credentials** between multiple people
5. **Regular password updates** every 3-6 months
6. **Monitor login activity** through the system logs
7. **Deactivate accounts** for personnel who leave or transfer out

## 🆘 Troubleshooting

### Can't Login?
- Check if you're using correct Employee ID (not email)
- Password is case-sensitive
- Make sure account is active
- Clear browser cache and try again

### Forgot Password?
- Contact SP/Admin to reset
- Or reinitialize database (⚠️ data loss)

### Account Locked/Inactive?
- Only SP can reactivate accounts
- Login as SP001 and go to Users → Edit

---

**Remember**: Change these default passwords immediately after deployment! 🔒
