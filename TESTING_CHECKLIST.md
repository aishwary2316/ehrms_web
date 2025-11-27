# E-HRMS Testing Checklist

## ✅ Testing Guide for All Features

### Setup & Installation
- [ ] Run `setup.bat` or `setup.ps1` successfully
- [ ] Database created (`ehrms.db` exists)
- [ ] Sample data loaded
- [ ] Application starts with `run.bat` or `run.ps1`
- [ ] Access http://localhost:5000 successfully

---

## 1. Authentication & Authorization Testing

### Login Tests
- [ ] Login as SP (SP001 / password123)
- [ ] Login as ASP (ASP001 / password123)
- [ ] Login as SDPO (SDPO001 / password123)
- [ ] Login as Inspector (INS001 / password123)
- [ ] Login as SI (SI0001 / password123)
- [ ] Login as Constable (C0001 / password123)
- [ ] Invalid credentials show error
- [ ] Logout works correctly
- [ ] Remember me checkbox works

### Authorization Tests
- [ ] SP can access all modules
- [ ] Inspector cannot access SP-only pages
- [ ] Personnel cannot access OC functions
- [ ] Proper error message on unauthorized access

---

## 2. Dashboard Testing

### SP Dashboard
- [ ] Total personnel count displayed
- [ ] On leave today count
- [ ] Absent today count
- [ ] Pending leave approvals shown
- [ ] Pending transfers shown
- [ ] Station-wise summary table
- [ ] Recent transfers list
- [ ] Quick action buttons work

### Inspector Dashboard
- [ ] Station personnel count
- [ ] Pending leave approvals for station
- [ ] Present/absent today stats
- [ ] Station personnel list
- [ ] Quick actions (mark attendance, create duty, review leaves)

### Personnel Dashboard
- [ ] Leave balance displayed (Earned, Casual, Medical)
- [ ] Recent leave applications shown
- [ ] Upcoming duties displayed
- [ ] Posting history shown
- [ ] Pending transfer alert (if any)
- [ ] Quick actions (apply leave, submit grievance, view payslips)

---

## 3. Leave Management Testing

### Apply for Leave
- [ ] Personnel can access "Apply for Leave" form
- [ ] Leave balance displayed correctly
- [ ] Date selection works
- [ ] Number of days calculated automatically
- [ ] Leave types dropdown (Earned, Casual, Medical)
- [ ] Reason text area works
- [ ] "Leaving station" checkbox works
- [ ] Submit shows success message
- [ ] Application appears in leave list

### Leave Approval Workflow
**Test as Constable (C0001):**
- [ ] Apply for 3 days casual leave
- [ ] See status as "Pending"

**Test as Inspector (INS001):**
- [ ] See pending leave in queue
- [ ] View leave details with overlapping count
- [ ] See leave balance of applicant
- [ ] Approve leave
- [ ] Status changes to "Approved_OC"
- [ ] Notification sent to SDPO

**Test as SDPO (SDPO001):**
- [ ] See leave in queue
- [ ] View complete leave details
- [ ] Approve leave
- [ ] Status changes to "Approved_SDPO"
- [ ] Notification sent to SP

**Test as SP (SP001):**
- [ ] See leave for final approval
- [ ] View all approval history
- [ ] Final approve
- [ ] Status changes to "Approved"
- [ ] Leave balance deducted
- [ ] Notification sent to applicant

### Leave Rejection
- [ ] Reject leave at any stage
- [ ] Provide rejection reason
- [ ] Status changes to "Rejected"
- [ ] Applicant notified

### Leave Calendar
- [ ] View leave calendar
- [ ] See all approved leaves
- [ ] Color-coded by status

---

## 4. Transfer Management Testing

### Create Transfer (as SP)
- [ ] Access "Create Transfer" page
- [ ] Select personnel from dropdown
- [ ] Select destination station
- [ ] Set order date
- [ ] Generate unique order number (e.g., TO/2025/0006)
- [ ] Submit successfully
- [ ] Notifications sent to:
  - Personnel being transferred
  - Current station OC
  - New station OC
  - Both SDPOs
  - SP

### Transfer Workflow
**Initial State:**
- [ ] Transfer status: "Ordered"
- [ ] Personnel still at current station

**Relieving (as current station OC):**
- [ ] OC sees pending transfer
- [ ] Click "Relieve" button
- [ ] Status changes to "Awaiting_Joining"
- [ ] Posting history updated

**Joining (as new station OC):**
- [ ] New OC sees awaiting joining transfer
- [ ] Click "Approve Joining" button
- [ ] Status changes to "Joined"
- [ ] Personnel's current station updated
- [ ] New posting history created

### Transfer Dashboard
- [ ] SP sees all transfers
- [ ] Filter by status works
- [ ] Transfer order details viewable
- [ ] Can see from/to stations
- [ ] Order number searchable

---

## 5. Duty Management Testing

### Create Duty by Name (as SP/OC)
- [ ] Access "Create Duty" page
- [ ] Enter event name
- [ ] Select location
- [ ] Select duty date
- [ ] Set start and end time
- [ ] Duration calculated automatically
- [ ] Select assignment type: "By Name"
- [ ] Select specific personnel
- [ ] Submit successfully
- [ ] Personnel notified

### Create Duty by Rank (as SP)
- [ ] Create duty with assignment type "By Rank"
- [ ] Select required rank (e.g., HC)
- [ ] Set number of personnel required
- [ ] OC notified to select personnel
- [ ] OC can assign specific personnel later

### Create Station Duty (as OC)
- [ ] OC creates station-level duty
- [ ] Automatically assigned to OC's station
- [ ] SP and SDPO notified

### Mark Duty Attendance
- [ ] View duty details
- [ ] Mark as present/absent
- [ ] Record actual hours worked
- [ ] Add remarks

### Duty Reports
- [ ] View all duties
- [ ] Filter by date
- [ ] Filter by station
- [ ] Sort by various columns
- [ ] See duty statistics

---

## 6. Attendance Management Testing

### Mark Attendance (as OC/Inspector)
- [ ] Access "Mark Attendance" page
- [ ] Select station
- [ ] Select date
- [ ] See list of all personnel
- [ ] Mark each as: Present/Absent/Late/On Leave
- [ ] Personnel on approved leave auto-highlighted
- [ ] Submit attendance
- [ ] Success message shown

### Attendance Notifications
- [ ] When personnel marked Absent
- [ ] SDPO receives notification
- [ ] SP receives notification
- [ ] Absence count shown in alert

### Attendance Reports
- [ ] View attendance for date range
- [ ] Filter by station
- [ ] Filter by rank
- [ ] Filter by status
- [ ] Export/print functionality
- [ ] See station-wise summary

### On Leave View
- [ ] Click "On Leave" link
- [ ] See all personnel on leave today
- [ ] Shows leave type and dates
- [ ] Clickable to view leave details

---

## 7. Station Management Testing

### View Stations
- [ ] See all stations listed
- [ ] Each station shows:
  - Code and name
  - SDPO assigned
  - Sanctioned strength
  - Current strength
  - Color-coded strength indicator
  - On leave count
  - Phone number

### Station Details
- [ ] Click station name
- [ ] See complete station information
- [ ] Personnel listed by rank
- [ ] Current strength vs sanctioned
- [ ] Can navigate to mark attendance

### Add/Edit Station (as SP)
- [ ] Add new station
- [ ] Set sanctioned strength for each rank
- [ ] Assign SDPO
- [ ] Edit existing station
- [ ] Update contact details

---

## 8. Personnel Management Testing

### View Personnel
- [ ] See all personnel listed
- [ ] Filter by rank
- [ ] Filter by station
- [ ] Filter by status (active/inactive)
- [ ] Search by name/employee ID
- [ ] Sort by columns
- [ ] Pagination works

### Personnel Details
- [ ] View individual personnel page
- [ ] See complete profile:
  - Employee ID, name, rank
  - Current station
  - Date of joining
  - Leave balances
  - Contact information
- [ ] See posting history
- [ ] Active/inactive status

### Add Personnel (as SP)
- [ ] Add new personnel
- [ ] Set rank
- [ ] Assign to station
- [ ] Set initial password
- [ ] Set leave balances
- [ ] Personnel can login

### Deactivate/Activate Personnel (as SP)
- [ ] Deactivate personnel
- [ ] Cannot login when inactive
- [ ] Reactivate personnel
- [ ] Can login again

---

## 9. Payslip Management Testing

### Upload Payslips (as SP)
- [ ] Access payslip upload page
- [ ] Select personnel
- [ ] Select month and year
- [ ] Upload PDF file
- [ ] Submit successfully
- [ ] File stored securely

### View Payslips (as Personnel)
- [ ] Personnel see their own payslips only
- [ ] Listed by month/year
- [ ] Download payslip works
- [ ] Cannot see others' payslips

---

## 10. Grievance System Testing

### Submit Grievance (as Personnel)
- [ ] Access "Submit Grievance" page
- [ ] Enter subject
- [ ] Enter detailed description
- [ ] Select category (Leave/Transfer/Duty/Workplace/Other)
- [ ] Submit successfully
- [ ] SP notified immediately
- [ ] Status: "Submitted"

### Respond to Grievance (as SP)
- [ ] SP sees all grievances
- [ ] Filter by status
- [ ] View grievance details
- [ ] Add response
- [ ] Change status to "Resolved"
- [ ] Personnel notified of response

### Grievance Tracking
- [ ] Personnel can see their grievances
- [ ] See response when given
- [ ] Status tracking works
- [ ] Priority levels displayed

---

## 11. Reporting System Testing

### Attendance Reports
- [ ] Access "Reports" → "Attendance Report"
- [ ] Set date range (last 14 days default)
- [ ] Select station (or all)
- [ ] See detailed attendance records
- [ ] Station-wise summary shown
- [ ] Present/Absent/Late/On Leave counts
- [ ] Print-friendly format

### Leave Reports
- [ ] Generate leave report
- [ ] Set date range
- [ ] Filter by station
- [ ] See all approved leaves
- [ ] Summary by station and type
- [ ] Total days calculation

### Duty Reports
- [ ] Generate duty report
- [ ] Filter by date and station
- [ ] See all duties
- [ ] Duty hours summary
- [ ] Actual vs planned hours

### Station Summary Report
- [ ] View comprehensive station report
- [ ] For each station:
  - Current strength by rank
  - Sanctioned vs actual
  - On leave today
  - Present/absent today
- [ ] Sortable and filterable

---

## 12. Notification System Testing

### Notification Badge
- [ ] Bell icon shows unread count
- [ ] Red badge when unread notifications
- [ ] Click to view notifications
- [ ] Badge updates automatically

### Notification List
- [ ] See all notifications
- [ ] Unread highlighted
- [ ] Filter: Show read/unread
- [ ] Click notification to view details
- [ ] Mark as read functionality
- [ ] Mark all as read button

### Notification Types
- [ ] Leave approval/rejection
- [ ] Transfer order issued
- [ ] Duty assignment
- [ ] Absence alert
- [ ] Grievance response
- [ ] Each links to relevant page

---

## 13. Security & Error Handling

### Security Tests
- [ ] Cannot access page without login
- [ ] Redirects to login page
- [ ] Cannot access unauthorized pages
- [ ] Proper 403 error shown
- [ ] Passwords hashed (not visible in database)
- [ ] Session expires after logout

### Error Pages
- [ ] 404 page for non-existent URLs
- [ ] 403 page for unauthorized access
- [ ] 500 page for server errors
- [ ] All have "Go to Dashboard" button

### Audit Logging
- [ ] Login actions logged
- [ ] Leave approvals logged
- [ ] Transfers logged
- [ ] All include: user, action, timestamp, IP address

---

## 14. UI/UX Testing

### Theme & Design
- [ ] Logo displayed correctly
- [ ] Color scheme matches logo (blue/gold)
- [ ] Consistent styling across pages
- [ ] Buttons have hover effects
- [ ] Forms are well-organized
- [ ] Tables are readable

### Responsive Design
- [ ] Desktop view (1920x1080)
- [ ] Laptop view (1366x768)
- [ ] Tablet view (768x1024)
- [ ] Mobile view (375x667)
- [ ] Navigation menu adapts
- [ ] Tables scroll horizontally on mobile

### Flash Messages
- [ ] Success messages (green)
- [ ] Error messages (red)
- [ ] Info messages (blue)
- [ ] Warning messages (yellow)
- [ ] Auto-dismiss after 5 seconds
- [ ] Closable manually

### Forms
- [ ] Required fields marked with *
- [ ] Validation on submit
- [ ] Clear error messages
- [ ] Date pickers work
- [ ] Dropdowns populate correctly
- [ ] Cancel buttons work

---

## 15. Performance Testing

### Page Load Times
- [ ] Homepage loads < 2 seconds
- [ ] Dashboard loads < 3 seconds
- [ ] Reports with 100+ records load < 5 seconds

### Database Queries
- [ ] Pagination works for large datasets
- [ ] Filters apply quickly
- [ ] Search is responsive
- [ ] No noticeable lag

---

## 16. Data Integrity Testing

### Leave Balance
- [ ] Correct initial balance
- [ ] Deducted after approval
- [ ] Cannot exceed balance
- [ ] Accurate calculation

### Transfer Updates
- [ ] Station changed after joining
- [ ] Posting history created
- [ ] Old posting closed properly

### Attendance Records
- [ ] One record per person per day
- [ ] No duplicates
- [ ] Proper date tracking

---

## Test Results Summary

**Total Tests**: ~200+  
**Passed**: _____  
**Failed**: _____  
**Blocked**: _____  

### Critical Issues Found:
1. 
2. 
3. 

### Minor Issues Found:
1. 
2. 
3. 

### Recommendations:
1. 
2. 
3. 

---

## Notes

**Testing Date**: __________________  
**Tested By**: __________________  
**Version**: 1.0  
**Environment**: Development  

---

**E-HRMS - Imphal West District Police**
