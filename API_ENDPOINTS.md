# E-HRMS API Endpoints Documentation 🌐

## Base URL
```
https://ehrm.onrender.com
```

---

## 🏠 Public Endpoints (No Login Required)

### Home & Health
| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/` | Home page | HTML page |
| GET | `/ping` | Keep-alive ping | `{"status": "ok", "message": "pong"}` |
| GET | `/health` | Health check with DB status | `{"status": "healthy", "database": "healthy"}` |

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/login` | Login page |
| POST | `/auth/login` | Login with Employee ID & Password |
| GET | `/auth/logout` | Logout current user |

---

## 🔐 Protected Endpoints (Login Required)

### Dashboard
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/dashboard/sp` | SP Dashboard | SP only |
| GET | `/dashboard/asp` | ASP Dashboard | ASP only |
| GET | `/dashboard/sdpo` | SDPO Dashboard | SDPO only |
| GET | `/dashboard/inspector` | Inspector Dashboard | Inspector only |
| GET | `/dashboard/personnel` | Personnel Dashboard | All other ranks |

---

## 👤 User Profile

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/profile/view` | View your profile | All users |
| GET | `/profile/edit` | Edit profile page | All users |
| POST | `/profile/edit` | Update profile | All users |
| POST | `/profile/upload_photo` | Upload profile photo | All users |

---

## 👥 User Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/users/` | List all users | SP, ASP, SDPO, Inspector |
| GET | `/users/add` | Add user page | SP only |
| POST | `/users/add` | Create new user | SP only |
| GET | `/users/edit/<id>` | Edit user page | SP only |
| POST | `/users/edit/<id>` | Update user | SP only |
| POST | `/users/delete/<id>` | Delete user | SP only |
| GET | `/users/view/<id>` | View user details | SP, ASP, SDPO, Inspector |

---

## 🏢 Station Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/stations/` | List all stations | All users |
| GET | `/stations/add` | Add station page | SP only |
| POST | `/stations/add` | Create new station | SP only |
| GET | `/stations/edit/<id>` | Edit station page | SP only |
| POST | `/stations/edit/<id>` | Update station | SP only |
| POST | `/stations/delete/<id>` | Delete station | SP only |
| GET | `/stations/view/<id>` | View station details | All users |

---

## 🏖️ Leave Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/leave/` | List all leaves | All users (filtered by role) |
| GET | `/leave/apply` | Leave application page | All users |
| POST | `/leave/apply` | Submit leave application | All users |
| GET | `/leave/view/<id>` | View leave details | Related users |
| POST | `/leave/approve/<id>` | Approve leave | OIC, SDPO, SP |
| POST | `/leave/reject/<id>` | Reject leave | OIC, SDPO, SP |
| POST | `/leave/cancel/<id>` | Cancel leave | Applicant only |

**Leave Approval Workflow:**
```
Personnel → OIC → SDPO → SP
         (Approve at each level)
```

---

## 🔄 Transfer Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/transfer/` | List all transfers | All users (filtered by role) |
| GET | `/transfer/create` | Create transfer page | SP only |
| POST | `/transfer/create` | Issue transfer order | SP only |
| GET | `/transfer/view/<id>` | View transfer details | Related users |
| POST | `/transfer/relieve/<id>` | Relieve personnel | Current station OIC |
| POST | `/transfer/join/<id>` | Confirm joining | New station OIC |
| POST | `/transfer/cancel/<id>` | Cancel transfer | SP only |

**Transfer Workflow:**
```
SP Issues → Current OIC Relieves → Personnel Joins → New OIC Confirms
```

---

## 👮 Duty Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/duty/` | List all duties | All users |
| GET | `/duty/create` | Create duty page | SP, Inspector |
| POST | `/duty/create` | Assign duty | SP, Inspector |
| GET | `/duty/view/<id>` | View duty details | Related users |
| POST | `/duty/mark_attendance/<id>` | Mark duty attendance | SP, Inspector |
| POST | `/duty/delete/<id>` | Delete duty | SP only |

**Duty Assignment Types:**
- **By_Name**: Assign specific personnel
- **By_Rank**: Request personnel of specific rank
- **Station_Duty**: Station-wide duty

---

## 📅 Attendance Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/attendance/` | View attendance | All users |
| GET | `/attendance/mark` | Mark attendance page | Inspector |
| POST | `/attendance/mark` | Submit attendance | Inspector |
| GET | `/attendance/report` | Attendance report | Inspector, SDPO, SP |

---

## 💰 Payslip Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/payslip/` | List your payslips | All users |
| GET | `/payslip/upload` | Upload payslip page | SP only |
| POST | `/payslip/upload` | Upload payslip PDF | SP only |
| GET | `/payslip/view/<id>` | View/Download payslip | Owner or SP |
| POST | `/payslip/delete/<id>` | Delete payslip | SP only |

---

## 😟 Grievance Management

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/grievance/` | List grievances | All users (filtered by role) |
| GET | `/grievance/submit` | Submit grievance page | All users |
| POST | `/grievance/submit` | Create grievance | All users |
| GET | `/grievance/view/<id>` | View grievance details | Submitter or SP |
| POST | `/grievance/respond/<id>` | Respond to grievance | SP only |
| POST | `/grievance/update_status/<id>` | Update status | SP only |

**Grievance Categories:**
- Leave
- Transfer
- Duty
- Workplace
- Other

---

## 📊 Reports

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/reports/` | Reports dashboard | SP, SDPO, Inspector |
| GET | `/reports/personnel` | Personnel report | SP, SDPO, Inspector |
| GET | `/reports/stations` | Stations report | SP, SDPO |
| GET | `/reports/transfer` | Transfer report | SP, SDPO |
| GET | `/reports/leave` | Leave report | SP, SDPO, Inspector |
| GET | `/reports/attendance` | Attendance report | SP, SDPO, Inspector |
| GET | `/reports/duty` | Duty report | SP, SDPO, Inspector |

**Export Options:**
- View in browser (HTML)
- Download as PDF
- Download as Excel

---

## 🔔 Notifications

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/notifications/` | View all notifications | All users |
| POST | `/notifications/mark_read/<id>` | Mark as read | All users |
| POST | `/notifications/mark_all_read` | Mark all as read | All users |
| GET | `/notifications/unread_count` | Get unread count | All users |

**Notification Types:**
- Leave (application, approval, rejection)
- Transfer (order issued, relieved, joined)
- Duty (assignment, reminder)
- Attendance (absent alert)
- Grievance (submission, response)
- General (system announcements)

---

## 🧪 Testing Endpoints

### Test Login
```bash
curl -X POST https://ehrm.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"employee_id": "SP001", "password": "sp123"}'
```

### Test Health
```bash
curl https://ehrm.onrender.com/health
```

### Test Ping
```bash
curl https://ehrm.onrender.com/ping
```

---

## 📋 Quick Test Guide

### 1. Open in Browser
```
https://ehrm.onrender.com
```

### 2. Login with Default Credentials
```
Employee ID: SP001
Password: sp123
```

### 3. Test Key Features
- ✅ Dashboard: `https://ehrm.onrender.com/dashboard/sp`
- ✅ Add Station: `https://ehrm.onrender.com/stations/add`
- ✅ Add User: `https://ehrm.onrender.com/users/add`
- ✅ Apply Leave: `https://ehrm.onrender.com/leave/apply`
- ✅ Create Transfer: `https://ehrm.onrender.com/transfer/create`
- ✅ Assign Duty: `https://ehrm.onrender.com/duty/create`
- ✅ View Notifications: `https://ehrm.onrender.com/notifications/`

---

## 🔑 Default User Logins

| Rank | Employee ID | Password | Dashboard URL |
|------|------------|----------|---------------|
| SP | SP001 | sp123 | `/dashboard/sp` |
| ASP | ASP001 | asp123 | `/dashboard/asp` |
| SDPO | SDPO001 | sdpo123 | `/dashboard/sdpo` |
| Inspector | INS001 | ins123 | `/dashboard/inspector` |
| SI | SI001 | si123 | `/dashboard/personnel` |
| ASI | ASI001 | asi123 | `/dashboard/personnel` |
| HC | HC001 | hc123 | `/dashboard/personnel` |
| C | C001 | c123 | `/dashboard/personnel` |

---

## 🚦 HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 302 | Redirect (after form submission) |
| 400 | Bad Request (invalid data) |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 500 | Server Error |

---

## 🔒 Access Control

### SP (Superintendent of Police)
- ✅ Full access to all features
- ✅ Create/edit/delete users
- ✅ Create/edit/delete stations
- ✅ Issue transfer orders
- ✅ Final leave approvals
- ✅ View all reports
- ✅ Respond to grievances

### ASP (Additional SP)
- ✅ View users and stations
- ✅ View reports
- ❌ Cannot edit users/stations

### SDPO (Sub-Divisional Police Officer)
- ✅ Approve leaves (second level)
- ✅ View subdivision reports
- ✅ Monitor personnel
- ❌ Cannot issue transfers

### Inspector (OIC - Officer In-Charge)
- ✅ Approve leaves (first level)
- ✅ Relieve/join personnel (transfers)
- ✅ Assign duties
- ✅ Mark attendance
- ✅ View station reports
- ❌ Cannot create users/stations

### Personnel (SI, ASI, HC, C)
- ✅ Apply for leaves
- ✅ View own profile
- ✅ Submit grievances
- ✅ View assigned duties
- ❌ Limited access

---

## 🎯 Common Use Cases

### 1. Apply for Leave
```
Login → /leave/apply → Fill form → Submit
→ OIC approves → SDPO approves → SP approves
→ Leave balance deducted automatically
```

### 2. Transfer Personnel
```
Login as SP → /transfer/create → Select personnel & stations
→ Transfer order issued → Notifications sent
→ Current OIC relieves → Personnel joins → New OIC confirms
```

### 3. Assign Duty
```
Login as SP/Inspector → /duty/create → Select type
→ By_Name: Assign specific person
→ By_Rank: Request rank from OIC
→ Notifications sent automatically
```

### 4. Mark Attendance
```
Login as Inspector → /attendance/mark → Select date
→ Mark present/absent → Submit
→ Absent alerts sent automatically
```

---

## 📱 Mobile Access

All endpoints are mobile-responsive! Access from:
- 📱 Mobile browser
- 💻 Desktop browser
- 🖥️ Tablet

---

## 🔄 Keep-Alive

To prevent free tier sleep, setup monitoring at:
```
UptimeRobot.com → Monitor: https://ehrm.onrender.com/ping
Interval: Every 5 minutes
```

---

## ⚠️ Important Notes

1. **Change default passwords** after first login
2. **Add stations** before assigning personnel
3. **Assign SDPO** to each station's district
4. **Assign Inspector (OIC)** to each station
5. **Leave approval** requires all 3 levels (OIC → SDPO → SP)
6. **Transfer workflow** requires relieve + join confirmation

---

## 🆘 Troubleshooting

### Cannot Access Endpoint?
- Check if you're logged in
- Verify you have required permissions
- Check URL spelling

### 403 Forbidden?
- You don't have permission for this action
- Login with appropriate rank (e.g., SP for user management)

### 404 Not Found?
- Check URL is correct
- Verify the ID exists
- Check if item was deleted

### 500 Server Error?
- Check Render logs
- Database connection issue?
- Contact admin

---

**Your E-HRMS is live at https://ehrm.onrender.com! 🎉**

Test all endpoints and change default passwords immediately!
