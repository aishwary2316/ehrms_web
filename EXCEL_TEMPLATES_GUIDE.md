# Excel Templates for Police Station Data Entry 📊

## Overview

These Excel templates are designed for data entry at Police Station (PS) level by Inspector/OIC. They can be filled offline and then uploaded to the E-HRMS system.

---

## 📋 Available Templates

### 1. **Personnel_Data_Template.xlsx**
For adding multiple personnel records at once

### 2. **Attendance_Template.xlsx**
For marking daily attendance of station personnel

### 3. **Duty_Roster_Template.xlsx**
For planning and assigning duties

### 4. **Leave_Applications_Template.xlsx**
For bulk leave application tracking

### 5. **Station_Assets_Template.xlsx**
For tracking station equipment and assets

---

## 1️⃣ Personnel Data Template

### Columns:

| Column | Description | Example | Required | Format |
|--------|-------------|---------|----------|--------|
| Employee_ID | Unique employee identifier | HC001 | Yes | Text |
| Name | Full name of personnel | Rajesh Kumar | Yes | Text |
| Email | Official email | rajesh.kumar@police.gov.in | Yes | Email |
| Phone | Mobile number | 9876543210 | Yes | 10 digits |
| Rank | Personnel rank | HC | Yes | C/HC/ASI/SI/Inspector |
| Date_of_Birth | Birth date | 15-01-1985 | Yes | DD-MM-YYYY |
| Date_of_Joining | Joining date | 10-05-2010 | Yes | DD-MM-YYYY |
| Current_Station | Station code | PS-001 | Yes | Text |
| Earned_Leave | Earned leave balance | 30 | No | Number (0-30) |
| Casual_Leave | Casual leave balance | 15 | No | Number (0-15) |
| Medical_Leave | Medical leave balance | 12 | No | Number (0-12) |
| Is_Active | Active status | Yes | Yes | Yes/No |

### Sample Data:
```
Employee_ID | Name           | Email                      | Phone      | Rank | DOB        | DOJ        | Station | EL | CL | ML | Active
HC001       | Rajesh Kumar   | rajesh@police.gov.in      | 9876543210 | HC   | 15-01-1985 | 10-05-2010 | PS-001  | 30 | 15 | 12 | Yes
ASI001      | Priya Sharma   | priya@police.gov.in       | 9876543211 | ASI  | 20-03-1987 | 15-06-2012 | PS-001  | 28 | 14 | 12 | Yes
C001        | Amit Singh     | amit@police.gov.in        | 9876543212 | C    | 10-07-1990 | 01-01-2015 | PS-001  | 25 | 15 | 10 | Yes
```

### Instructions:
1. Fill all required fields (marked Yes)
2. Employee_ID must be unique across the system
3. Email must be unique
4. Rank must be one of: C, HC, ASI, SI, Inspector
5. Dates in DD-MM-YYYY format
6. Leave balances: Earned (0-30), Casual (0-15), Medical (0-12)
7. Active: Yes or No

### Upload Process:
1. Login as Inspector/OIC
2. Go to Users → Import from Excel
3. Upload file
4. Review data preview
5. Confirm import

---

## 2️⃣ Attendance Template

### Columns:

| Column | Description | Example | Required |
|--------|-------------|---------|----------|
| Date | Attendance date | 01-11-2025 | Yes |
| Employee_ID | Personnel ID | HC001 | Yes |
| Status | Attendance status | Present | Yes |
| Check_In | Check-in time | 08:00 | No |
| Check_Out | Check-out time | 17:00 | No |
| Hours_Worked | Total hours | 9 | No |
| Remarks | Any notes | Late arrival | No |

### Valid Status Values:
- **Present** - Personnel present at duty
- **Absent** - Personnel absent
- **Leave** - On approved leave
- **Holiday** - Weekly off/public holiday
- **Training** - On training duty
- **Deputation** - On deputation

### Sample Data:
```
Date       | Employee_ID | Status  | Check_In | Check_Out | Hours | Remarks
01-11-2025 | HC001       | Present | 08:00    | 17:00     | 9     | -
01-11-2025 | ASI001      | Present | 08:15    | 17:00     | 8.75  | Late 15 min
01-11-2025 | C001        | Leave   | -        | -         | 0     | Casual Leave
02-11-2025 | HC001       | Present | 08:00    | 20:00     | 12    | Overtime
02-11-2025 | ASI001      | Present | 08:00    | 17:00     | 9     | -
02-11-2025 | C001        | Leave   | -        | -         | 0     | Casual Leave
```

### Instructions:
1. One row per person per date
2. Date format: DD-MM-YYYY
3. Time format: HH:MM (24-hour)
4. Status must match valid values
5. For Leave/Holiday, leave time fields empty
6. Hours_Worked auto-calculated or manual entry

### Upload Process:
1. Login as Inspector
2. Go to Attendance → Import from Excel
3. Select month and upload file
4. System validates data
5. Confirm to save

---

## 3️⃣ Duty Roster Template

### Columns:

| Column | Description | Example | Required |
|--------|-------------|---------|----------|
| Duty_Date | Date of duty | 05-11-2025 | Yes |
| Employee_ID | Personnel assigned | HC001 | Yes |
| Duty_Type | Type of duty | Patrolling | Yes |
| Location | Duty location | Market Area | Yes |
| Start_Time | Duty start | 08:00 | Yes |
| End_Time | Duty end | 20:00 | Yes |
| Shift | Shift type | Day | No |
| Remarks | Additional notes | VIP movement | No |

### Valid Duty Types:
- **Patrolling** - Regular patrol duty
- **Bandobast** - Security arrangement
- **Investigation** - Investigation duty
- **Court** - Court duty
- **Traffic** - Traffic management
- **VIP_Security** - VIP protection
- **Station_Duty** - Station house duty
- **PCR** - PCR van duty

### Valid Shifts:
- **Day** - Day shift (08:00-20:00)
- **Night** - Night shift (20:00-08:00)
- **General** - General shift (fixed hours)

### Sample Data:
```
Date       | Employee_ID | Duty_Type    | Location      | Start | End   | Shift | Remarks
05-11-2025 | HC001       | Patrolling   | Market Area   | 08:00 | 20:00 | Day   | -
05-11-2025 | ASI001      | Investigation| PS Office     | 09:00 | 17:00 | Day   | Case 45/2025
05-11-2025 | C001        | Station_Duty | PS Office     | 20:00 | 08:00 | Night | -
06-11-2025 | HC001       | VIP_Security | Circuit House | 06:00 | 22:00 | Day   | CM visit
06-11-2025 | ASI001      | Court        | District Court| 10:00 | 16:00 | Day   | Case hearing
```

### Instructions:
1. Plan duties in advance (weekly/monthly)
2. Avoid overlapping duties for same person
3. Ensure adequate personnel for each shift
4. Balance workload among personnel
5. Time format: HH:MM (24-hour)

### Upload Process:
1. Login as Inspector
2. Go to Duty → Import Roster
3. Upload file
4. System checks for conflicts
5. Personnel receive notifications

---

## 4️⃣ Leave Applications Template

### Columns:

| Column | Description | Example | Required |
|--------|-------------|---------|----------|
| Employee_ID | Applicant ID | HC001 | Yes |
| Leave_Type | Type of leave | Casual | Yes |
| Start_Date | Leave start | 10-11-2025 | Yes |
| End_Date | Leave end | 12-11-2025 | Yes |
| Num_Days | Number of days | 3 | Yes |
| Reason | Leave reason | Family function | Yes |
| Contact_Number | Contact during leave | 9876543210 | No |
| Address | Address during leave | Village Xyz | No |
| Status | Current status | Pending | No |

### Valid Leave Types:
- **Earned** - Earned leave (30 days/year)
- **Casual** - Casual leave (15 days/year)
- **Medical** - Medical leave (12 days/year)
- **Maternity** - Maternity leave
- **Paternity** - Paternity leave

### Valid Status Values:
- **Pending** - Not yet submitted
- **Submitted** - Awaiting OIC approval
- **Approved_OC** - OIC approved
- **Approved_SDPO** - SDPO approved
- **Approved_SP** - Final approval
- **Rejected** - Rejected at any level

### Sample Data:
```
Employee_ID | Leave_Type | Start_Date | End_Date   | Days | Reason          | Contact    | Status
HC001       | Casual     | 10-11-2025 | 12-11-2025 | 3    | Family function | 9876543210 | Pending
ASI001      | Earned     | 15-11-2025 | 25-11-2025 | 11   | Annual vacation | 9876543211 | Pending
C001        | Medical    | 08-11-2025 | 09-11-2025 | 2    | Fever          | 9876543212 | Pending
```

### Instructions:
1. Check leave balance before applying
2. End_Date must be >= Start_Date
3. Num_Days = End_Date - Start_Date + 1
4. Provide valid reason
5. Contact number for emergencies
6. Status "Pending" for new applications

### Upload Process:
1. Login as Inspector
2. Go to Leave → Import Applications
3. Upload file
4. Applications submitted for approval
5. Applicants receive notifications

---

## 5️⃣ Station Assets Template

### Columns:

| Column | Description | Example | Required |
|--------|-------------|---------|----------|
| Asset_Type | Type of asset | Vehicle | Yes |
| Asset_Name | Name/Model | Mahindra Bolero | Yes |
| Asset_Code | Unique code | VEH-001 | Yes |
| Purchase_Date | Date acquired | 15-01-2020 | No |
| Status | Current status | Working | Yes |
| Assigned_To | Employee ID | HC001 | No |
| Location | Current location | PS Parking | Yes |
| Condition | Physical condition | Good | No |
| Last_Service | Last maintenance | 01-10-2025 | No |
| Next_Service | Next maintenance due | 01-01-2026 | No |
| Remarks | Additional notes | Regular servicing | No |

### Valid Asset Types:
- **Vehicle** - Cars, bikes, PCR vans
- **Weapon** - Firearms, lathis
- **Communication** - Radios, phones
- **Computer** - PCs, laptops, printers
- **Furniture** - Tables, chairs
- **Equipment** - Other equipment

### Valid Status:
- **Working** - In working condition
- **Under_Repair** - Being repaired
- **Out_of_Order** - Not working
- **Disposed** - Disposed off

### Valid Condition:
- **Excellent** - Like new
- **Good** - Normal wear
- **Fair** - Needs attention
- **Poor** - Needs repair

### Sample Data:
```
Type    | Name           | Code    | Purchase   | Status  | Assigned | Location   | Condition | Last_Service | Next_Service | Remarks
Vehicle | Bolero         | VEH-001 | 15-01-2020 | Working | HC001    | PS Parking | Good      | 01-10-2025   | 01-01-2026   | PCR van
Weapon  | Service Rifle  | WPN-001 | 10-05-2015 | Working | ASI001   | Armory     | Good      | 15-09-2025   | 15-03-2026   | -
Computer| Desktop PC     | CMP-001 | 20-08-2021 | Working | -        | PS Office  | Excellent | -            | -            | Intel i5
```

### Instructions:
1. Maintain accurate asset register
2. Update status regularly
3. Track maintenance schedules
4. Record assignments clearly
5. Date format: DD-MM-YYYY

---

## 📥 How to Download Templates

### Option 1: Create in Excel
1. Open Microsoft Excel
2. Create new workbook
3. Copy column headers from above
4. Save as `.xlsx` format

### Option 2: From System (Future Feature)
1. Login to E-HRMS
2. Go to respective section
3. Click "Download Template"
4. Fill and upload

---

## 📤 Upload Process

### General Steps:
1. **Prepare Data**
   - Fill template completely
   - Validate all required fields
   - Check data formats
   - Remove empty rows

2. **Login to System**
   - Login as Inspector/OIC
   - Navigate to respective module

3. **Upload File**
   - Click "Import from Excel"
   - Select file
   - Upload

4. **Review Preview**
   - System shows data preview
   - Check for errors
   - Correct if needed

5. **Confirm Import**
   - Click "Confirm Import"
   - Data saved to database
   - Notifications sent (if applicable)

---

## ✅ Data Validation Rules

### Common Rules:
- ✅ Required fields cannot be empty
- ✅ Dates must be in DD-MM-YYYY format
- ✅ Employee_ID must exist in system
- ✅ Email must be valid format
- ✅ Phone must be 10 digits
- ✅ No duplicate records
- ✅ Status values must match predefined list

### Personnel Data:
- ✅ Employee_ID must be unique
- ✅ Email must be unique
- ✅ Rank must be valid
- ✅ Leave balance within limits

### Attendance:
- ✅ Date not in future
- ✅ Employee_ID must exist
- ✅ Status must be valid
- ✅ Check_Out > Check_In

### Duty Roster:
- ✅ No overlapping duties
- ✅ Duty_Date can be in future
- ✅ End_Time > Start_Time
- ✅ Valid duty type

### Leave Applications:
- ✅ End_Date >= Start_Date
- ✅ Sufficient leave balance
- ✅ No overlapping leaves
- ✅ Valid leave type

---

## 🎯 Best Practices

### 1. Data Entry
- ✅ Use consistent formatting
- ✅ Avoid special characters in names
- ✅ Use UPPERCASE for codes
- ✅ Double-check employee IDs
- ✅ Validate before upload

### 2. File Management
- ✅ Name files with date: `Attendance_Nov2025.xlsx`
- ✅ Keep backup copies
- ✅ Archive old files
- ✅ Use version numbers if multiple revisions

### 3. Regular Updates
- ✅ Upload attendance daily
- ✅ Update duty roster weekly
- ✅ Review personnel data monthly
- ✅ Track assets quarterly

### 4. Error Handling
- ✅ Fix errors shown in preview
- ✅ Don't force-upload invalid data
- ✅ Contact admin if persistent errors
- ✅ Keep log of uploads

---

## 🚨 Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Employee_ID not found" | ID doesn't exist in system | Create user first or check spelling |
| "Invalid date format" | Wrong date format | Use DD-MM-YYYY format |
| "Duplicate entry" | Record already exists | Check for duplicates, update instead |
| "Invalid status value" | Status not in list | Use exact status values from list |
| "Insufficient leave balance" | Not enough leaves | Check leave balance first |
| "Overlapping duty" | Duty conflict | Check existing duties for that person |

---

## 📞 Support

For template issues or upload problems:
- Contact: System Administrator (SP)
- Email: sp@police.gov.in
- Phone: Extension 100

---

## 🔄 Template Updates

Templates are version-controlled. Check for updates:
- **Version**: 1.0
- **Last Updated**: November 2025
- **Next Review**: February 2026

---

**Important**: Always download the latest template version before data entry!
