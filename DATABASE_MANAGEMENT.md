# Database Management - Transfers, Duties, Notifications & More 📊

## Overview

Your E-HRMS system has **9 main database tables** that manage all operations:

1. **Users** - Personnel records
2. **Stations** - Police stations
3. **Leaves** - Leave applications & approvals
4. **Transfers** - Transfer orders & workflow
5. **Duties** - Duty assignments
6. **Attendance** - Attendance tracking
7. **Grievances** - Grievance submissions
8. **Notifications** - Real-time alerts
9. **Audit Logs** - Activity tracking

---

## 📦 Transfer Management

### Database Structure (Transfer Model)

```python
Transfer Table:
- id (Primary Key)
- order_number (Unique, e.g., "TR-2025-001")
- user_id (Personnel being transferred)
- from_station_id (Current station)
- to_station_id (New station)
- transfer_type (Intra-district / Inter-district)
- order_date (When order was issued)
- effective_date (When transfer takes effect - immediate)
- status (Workflow tracking)
- issued_by_id (SP who issued order)
- relieved_by_id (OIC who relieved personnel)
- relieved_at (Timestamp)
- joining_approved_by_id (OIC at new station)
- joined_at (Timestamp)
- remarks
```

### Transfer Workflow

```
1. SP Issues Transfer Order
   ↓ (Status: Ordered)
   - Transfer record created in database
   - Personnel notified
   - Current station OIC notified
   - New station OIC notified
   - SDPO notified (if inter-district)

2. Current Station OIC Relieves Personnel
   ↓ (Status: Relieved)
   - OIC marks as "Relieved"
   - relieved_by_id = OIC user_id
   - relieved_at = Current timestamp
   - Personnel notified to join new station

3. Personnel Joins New Station
   ↓ (Status: Awaiting_Joining)
   - Personnel reports to new station
   - New OIC approves joining

4. New Station OIC Confirms Joining
   ↓ (Status: Joined)
   - joining_approved_by_id = New OIC user_id
   - joined_at = Current timestamp
   - User.current_station_id updated to new station
   - Transfer complete!
```

### Automatic Database Updates

When transfer is completed:
```python
# Update user's current station
user.current_station_id = transfer.to_station_id

# Update station counts
old_station.personnel_count -= 1
new_station.personnel_count += 1

# Create audit log
AuditLog: "transfer_completed" by SP
```

### Notifications Created

1. **Personnel**: "You have been transferred from [Station A] to [Station B]"
2. **Old OIC**: "Please relieve [Personnel Name] - Transfer Order #[Number]"
3. **New OIC**: "Incoming transfer: [Personnel Name] from [Station A]"
4. **SDPO (if inter-district)**: "Transfer order issued for [Personnel Name]"

---

## 👮 Duty Management

### Database Structure (Duty Model)

```python
Duty Table:
- id (Primary Key)
- duty_order_number (Unique, e.g., "DT-2025-001")
- event_name (e.g., "VIP Security", "Patrolling")
- location (Duty location)
- duty_date (Date of duty)
- start_time (e.g., 08:00)
- end_time (e.g., 20:00)
- duration_hours (Auto-calculated)
- assignment_type (By_Name / By_Rank / Station_Duty)
- required_rank (If By_Rank, e.g., "HC")
- num_personnel_required (e.g., 5)
- user_id (If By_Name - specific person)
- station_id (Station responsible)
- created_by_id (SP or OIC who created)
- is_present (Attendance tracking)
- actual_hours (Actual duty hours)
```

### Duty Assignment Types

#### 1. By_Name (Direct Assignment)
```
SP/OIC assigns specific personnel:
- user_id = Selected personnel
- Notification sent directly to that person
```

#### 2. By_Rank (Rank-based Assignment)
```
SP/OIC requests personnel of specific rank:
- required_rank = "HC" (Head Constable)
- num_personnel_required = 3
- station_id = Responsible station
- OIC of that station notified
- OIC assigns 3 Head Constables from their station
```

#### 3. Station_Duty (Station-wide)
```
Regular station duty:
- station_id = Station
- All station personnel notified
- OIC manages roster
```

### Duty Notifications

**For By_Name Assignment:**
```
To Personnel: "You are assigned to [Event Name] on [Date] at [Location]"
To OIC: "Duty order created for [Personnel Name]"
```

**For By_Rank Assignment:**
```
To OIC: "Provide [Number] personnel of rank [Rank] for [Event Name]"
To SP: "Duty order created - waiting for OIC assignment"
```

### Automatic Database Updates

```python
# Calculate duration automatically
duty.duration_hours = (end_time - start_time).hours

# Mark attendance
duty.is_present = True/False

# Track actual hours
duty.actual_hours = recorded_hours

# Create audit log
AuditLog: "duty_created" by SP/OIC
```

---

## 🔔 Notification System

### Database Structure (Notification Model)

```python
Notification Table:
- id (Primary Key)
- user_id (Recipient)
- title (Short summary)
- message (Detailed message)
- notification_type (Category)
- related_id (ID of related entity)
- link (URL to view details)
- is_read (Boolean)
- read_at (Timestamp when read)
- created_at (Timestamp)
```

### Notification Types

| Type | Triggered When | Recipients |
|------|----------------|------------|
| **Leave** | Leave applied/approved/rejected | Applicant, OC, SDPO, SP |
| **Transfer** | Transfer order issued/completed | Personnel, OICs, SDPO |
| **Duty** | Duty assigned | Assigned personnel, OIC |
| **Attendance** | Attendance marked/absent | Personnel, OIC |
| **Grievance** | Grievance submitted/responded | Submitter, SP, HR |
| **General** | System announcements | All users |

### Automatic Notification Creation

#### Leave Application
```python
# When personnel applies for leave:
Notification 1: To Applicant
  "Your leave application for [Dates] has been submitted"

Notification 2: To OIC
  "New leave application from [Name] for [Dates] - Action Required"

# When OIC approves:
Notification 3: To Applicant
  "Your leave has been approved by OIC - Forwarded to SDPO"

Notification 4: To SDPO
  "Leave application from [Name] requires your approval"

# And so on through SP...
```

#### Transfer Order
```python
# When SP issues transfer:
Notification 1: To Personnel
  "Transfer Order: You are transferred from [A] to [B]"

Notification 2: To Current OIC
  "Please relieve [Name] - Transfer Order #[Number]"

Notification 3: To New OIC
  "Incoming transfer: [Name] will join your station"

Notification 4: To SDPO (if inter-district)
  "Transfer order issued for [Name]"
```

#### Duty Assignment
```python
# By_Name:
Notification: To Personnel
  "Duty Assignment: [Event] on [Date] at [Location]"

# By_Rank:
Notification: To OIC
  "Provide [Number] [Rank] personnel for [Event]"
```

### Notification Management

**User Interface:**
- Bell icon in navbar shows unread count
- Click to view all notifications
- Mark as read (updates is_read = True, read_at = timestamp)
- Notifications older than 30 days auto-archived

**Database Query:**
```python
# Get unread notifications
unread = Notification.query.filter_by(
    user_id=current_user.id, 
    is_read=False
).order_by(Notification.created_at.desc()).all()

# Get notification count
count = Notification.query.filter_by(
    user_id=current_user.id, 
    is_read=False
).count()
```

---

## 📋 Leave Management

### Workflow with Database Updates

```
1. Personnel Applies
   - Create Leave record (status: Pending_OC)
   - Create Notification for OIC
   - Create Audit Log

2. OIC Approves
   - Update status: Approved_OC
   - Set oc_id, oc_approved_at
   - Create Notification for SDPO
   - Create Notification for Applicant

3. SDPO Approves
   - Update status: Approved_SDPO
   - Set sdpo_id, sdpo_approved_at
   - Create Notification for SP
   - Create Notification for Applicant

4. SP Final Approval
   - Update status: Approved_SP
   - Set sp_id, sp_approved_at
   - Deduct leave balance from user
   - Set user.is_on_leave = True (if currently on leave)
   - Create Notification for Applicant
   - Create Audit Log
```

### Leave Balance Deduction

```python
# Automatic when SP approves:
if leave.leave_type == 'Earned':
    user.earned_leave_balance -= leave.num_days
elif leave.leave_type == 'Casual':
    user.casual_leave_balance -= leave.num_days
elif leave.leave_type == 'Medical':
    user.medical_leave_balance -= leave.num_days

db.session.commit()
```

---

## 📊 Attendance Management

### Database Structure

```python
Attendance Table:
- id
- user_id (Personnel)
- station_id (Station)
- date (Attendance date)
- status (Present/Absent/Leave/Holiday)
- check_in_time
- check_out_time
- hours_worked
- marked_by_id (OIC who marked)
- remarks
```

### Automatic Processing

```python
# Daily attendance marking by OIC
for user in station.personnel:
    attendance = Attendance(
        user_id=user.id,
        station_id=station.id,
        date=today,
        status='Present',  # or 'Absent'
        marked_by_id=oic.id
    )
    
    # If absent, create notification
    if status == 'Absent':
        notify_attendance_alert(user, station)
```

---

## 😟 Grievance Management

### Database Structure

```python
Grievance Table:
- id
- user_id (Submitter)
- subject
- description
- category (Leave/Transfer/Duty/Workplace/Other)
- status (Submitted/Under_Review/Resolved/Closed)
- priority (Low/Normal/High/Urgent)
- response
- responded_by_id (HR/SP)
- responded_at
```

### Workflow

```
1. Personnel Submits Grievance
   - Create Grievance record
   - Notify SP/HR
   - Status: Submitted

2. SP/HR Reviews
   - Update status: Under_Review
   - Notify submitter

3. SP/HR Responds
   - Add response text
   - Set responded_by_id, responded_at
   - Status: Resolved
   - Notify submitter
```

---

## 📝 Audit Log System

### Tracks All Important Actions

```python
Every action creates audit log:
- User login/logout
- Leave application/approval/rejection
- Transfer order issued/completed
- Duty assignment created
- Attendance marked
- User created/edited/deleted
- Station created/edited
- Password changed
- Settings updated
```

### Database Structure

```python
AuditLog Table:
- id
- user_id (Who performed action)
- action (What was done)
- entity_type (Leave/Transfer/User etc.)
- entity_id (ID of affected entity)
- details (JSON with additional info)
- ip_address (User's IP)
- timestamp
```

### Example Entries

```
[2025-10-29 10:30:15] SP001 | approve_leave | Leave #45 | "Approved leave for HC001"
[2025-10-29 11:20:30] SP001 | issue_transfer | Transfer #23 | "Transferred INS001 from PS-A to PS-B"
[2025-10-29 14:45:00] INS001 | mark_attendance | Attendance | "Marked 15 personnel present"
[2025-10-29 16:00:12] HC001 | login | - | "Successful login from 192.168.1.10"
```

---

## 🔄 Database Auto-Management Features

### 1. Automatic Timestamps
All records have:
- `created_at` - Auto-set on creation
- `updated_at` - Auto-updated on any change

### 2. Cascade Deletes
Relationships configured with cascade:
- Delete user → Archive their leaves, transfers, duties
- Delete station → Update personnel to null station

### 3. Data Integrity
Database constraints:
- Unique constraints (order numbers, employee IDs)
- Foreign keys (maintain relationships)
- Check constraints (valid statuses, dates)

### 4. Indexing for Performance
Indexed columns:
- user_id, station_id (fast lookups)
- status (filter by status)
- date columns (date range queries)
- is_read (unread notifications)

---

## 🎯 Real-Time Database Updates

### When Actions Occur:

**Leave Approved:**
```python
1. Update Leave.status = 'Approved_SP'
2. Update User.earned_leave_balance -= days
3. Create Notification (applicant)
4. Create Notification (OIC)
5. Create AuditLog entry
6. Commit all changes atomically
```

**Transfer Completed:**
```python
1. Update Transfer.status = 'Joined'
2. Update User.current_station_id = new_station
3. Update old_station.personnel_count -= 1
4. Update new_station.personnel_count += 1
5. Create Notifications (all parties)
6. Create AuditLog entry
7. Commit all changes atomically
```

**Duty Assigned:**
```python
1. Create Duty record
2. If By_Name: Create Notification (personnel)
3. If By_Rank: Create Notification (OIC)
4. Create AuditLog entry
5. Commit all changes atomically
```

---

## 🗄️ Database Initialization

### On First Deployment

```python
auto_init_db.py runs automatically:

1. Create all tables (if don't exist)
2. Create 8 default users (one per rank)
3. Ready to add:
   - Stations
   - Real users
   - Then they can create:
     - Leaves
     - Transfers
     - Duties
     - Grievances
```

### Database Location

- **Development (Local)**: SQLite file `ehrms.db`
- **Production (Render)**: PostgreSQL database
  - Host: `dpg-d413m02li9vc73c3tjb0-a`
  - Database: `ehrms_db`
  - Automatic backups by Render

---

## 📈 Database Growth & Maintenance

### Expected Growth

```
Users: ~500-1000 records (personnel)
Stations: ~50-100 records (police stations)
Leaves: ~10,000/year (20 leaves/user/year)
Transfers: ~500/year (10% transfer rate)
Duties: ~5,000/year (special duties)
Notifications: ~50,000/year (auto-archived)
Audit Logs: ~100,000/year (all actions)
```

### Auto-Cleanup (Recommended to implement)

```python
# Archive old notifications (older than 90 days)
# Archive old audit logs (older than 1 year)
# Keep all leaves, transfers, duties (historical records)
```

---

## ✅ Summary

Your database is **automatically managed** for:

✅ **Transfers** - Complete workflow with status tracking
✅ **Duties** - Assignment types and attendance tracking  
✅ **Notifications** - Auto-created for all actions
✅ **Leaves** - Multi-level approval with balance deduction
✅ **Attendance** - Daily marking and alerts
✅ **Grievances** - Submission and response tracking
✅ **Audit Logs** - Complete action history

**Everything is automatic!** Just use the web interface - the database handles all the complex tracking, notifications, and updates behind the scenes. 🎉
