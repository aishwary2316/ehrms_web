# Leave Management System - Complete Features

## Overview
Comprehensive leave management system with 9 leave types, validation rules, document uploads, and advanced workflows.

---

## 1. Leave Types (9 Total)

### 1.1 Earned Leave
- **Balance**: 30 days per year
- **LTC Option**: With/Without LTC
- **Validation**: Requires sufficient balance
- **Deduction**: Yes

### 1.2 Casual Leave
- **Balance**: 15 days per year
- **Purpose**: Short-term personal needs
- **Validation**: Requires sufficient balance
- **Deduction**: Yes

### 1.3 Medical Leave
- **Balance**: 12 days per year
- **Purpose**: Medical reasons
- **Validation**: Requires sufficient balance
- **Deduction**: Yes

### 1.4 Half Pay Leave
- **Balance**: 20 days
- **Purpose**: Extended leave with half pay
- **Validation**: Requires sufficient balance
- **Deduction**: Yes

### 1.5 Extraordinary Leave
- **Balance**: Not debited
- **Purpose**: Special circumstances
- **Validation**: None (no balance check)
- **Deduction**: No

### 1.6 Maternity Leave
- **Types**: 
  - Pregnancy: 135-180 days
  - Miscarriage: 45 days (lifetime total)
- **Validation**:
  - Less than 2 surviving children
  - Duration limits enforced
  - Medical certificate required
- **Deduction**: No (separate tracking)

### 1.7 Paternity Leave
- **Duration**: Maximum 15 days
- **Validation**:
  - Less than 2 surviving children
  - Within 15 days before to 6 months after delivery date
- **Deduction**: No

### 1.8 Adoption Leave
- **Duration**: Maximum 135 days
- **Validation**:
  - Less than 2 surviving children
  - Child age must be less than 12 months
- **Deduction**: No

### 1.9 Child Care Leave
- **Balance**: 730 days (lifetime total)
- **Purpose**: 
  - Rearing children
  - Education/examination needs
  - Child sickness
  - Other care reasons
- **Validation**: Child age must be less than 18 years
- **Deduction**: No (tracked separately)

### 1.10 Leave Not Due
- **Purpose**: Applied when no balance left
- **Validation**: None
- **Deduction**: No

---

## 2. Leave Application Features

### 2.1 Conditional Fields
Form dynamically shows/hides fields based on leave type selection:

- **Earned Leave**: LTC option (With/Without LTC)
- **Maternity Leave**: 
  - Type (Pregnancy/Miscarriage)
  - Number of surviving children
- **Paternity Leave**:
  - Number of surviving children
  - Delivery date (with validation window)
- **Adoption Leave**:
  - Number of surviving children
  - Adoption date
  - Child age in months
- **Child Care Leave**:
  - Child age in years
  - Care reason (dropdown)

### 2.2 Document Upload
- **Medical Certificate**: Single file upload
- **Other Documents**: Multiple file uploads
- **Document Title**: Optional title for documents
- **Supported Formats**: PDF, JPG, JPEG, PNG
- **Storage**: `static/uploads/leave_documents/`
- **Filename**: Secure with timestamp

### 2.3 Prefix/Suffix Dates
- **Purpose**: Exclude Sundays/Holidays from leave count
- **Input**: Comma-separated dates (DD-MM-YYYY)
- **Example**: "05-12-2024, 12-12-2024, 25-12-2024"
- **Effect**: These dates not counted in num_days

### 2.4 Suspension Check
- **Frontend**: Alert displayed if user is suspended
- **Backend**: Application blocked with error message
- **User Field**: `is_suspended` (Boolean)

### 2.5 Validation Rules
**Client-Side (JavaScript)**:
- Leave type selection required
- Date validation (end > start)
- Child count validation for family leaves
- Delivery date window for paternity
- Child age limits
- Duration limits

**Server-Side (Python)**:
- `validate_leave_application()`: Comprehensive validation
- `check_leave_balance()`: Balance checking
- Suspension check
- Date validations

---

## 3. Approval Workflow

### 3.1 Multi-Level Approval
1. **Officer in Charge (OC)**: First level
2. **SDPO**: Second level
3. **Superintendent of Police (SP)**: Final approval

### 3.2 Recommended Days
- Each approval level can modify recommended days
- Senior officers see all previous recommendations
- Fields tracked:
  - `original_num_days`: User's original request
  - `oc_recommended_days`: OC's recommendation
  - `sdpo_recommended_days`: SDPO's recommendation
  - `sp_recommended_days`: SP's final decision

### 3.3 Approval Status Tracking
- `status`: Overall status
- `oc_status`: OC approval status
- `sdpo_status`: SDPO approval status
- `sp_status`: SP approval status
- Each level stores: approver ID, remarks, approval timestamp

---

## 4. Leave Balance Management

### 4.1 Balance Fields (User Model)
```python
earned_leave_balance = 30
casual_leave_balance = 15
medical_leave_balance = 12
half_pay_leave_balance = 20
child_care_leave_balance = 730
maternity_leave_used = 0
maternity_miscarriage_leave_used = 0
```

### 4.2 Deduction Logic
**Debited Types**:
- Earned Leave
- Casual Leave
- Medical Leave
- Half Pay Leave

**Non-Debited Types**:
- Maternity Leave (tracked separately)
- Paternity Leave
- Adoption Leave
- Child Care Leave (tracked separately)
- Extraordinary Leave
- Leave Not Due

### 4.3 Balance Restoration
Balance restored in cases of:
- Leave withdrawal
- Early return from leave
- Recall to duty
- Leave rejection

---

## 5. Advanced Features

### 5.1 Commutation of Leave
**Route**: `/leave/commutation/request/<leave_id>`

**Purpose**: Convert leave type retrospectively (after completion)

**Workflow**:
1. User requests commutation (POST with new leave type)
2. SP approves/rejects commutation
3. Original balance restored
4. New leave type balance deducted
5. Leave record updated with `commuted: True`

**Valid Conversions**: To Earned, Casual, Medical, Half Pay Leave

**Database**: `leave_commutations` collection

### 5.2 Recall to Duty
**Route**: `/leave/recall/create`

**Purpose**: SP recalls personnel from approved leave

**Workflow**:
1. SP selects personnel currently on leave (GET shows list)
2. SP specifies recall date and reason
3. SP uploads recall order (PDF)
4. System calculates days to restore
5. Leave balance restored
6. Leave end date updated
7. Personnel notified

**Features**:
- Only shows active leaves
- Prevents recalling already recalled personnel
- Automatic balance adjustment
- Notification to recalled personnel

**Database**: `leave_recalls` collection

### 5.3 Return from Leave Early
**Route**: `/leave/return_early/<leave_id>`

**Purpose**: User requests to return before original end date

**Workflow**:
1. User submits new end date and reason (POST)
2. Request created with multi-level approval flow
3. OC → SDPO → SP approval
4. On SP approval:
   - Leave end date updated
   - Balance restored for unused days
   - Leave record updated with `early_return: True`

**Validation**:
- New end date must be earlier than original
- New end date must be after start date
- Leave must be fully approved

**Database**: `leave_early_returns` collection

### 5.4 Leave Modification
**Route**: `/leave/modify/<leave_id>`

**Purpose**: User modifies leave dates before full approval

**Workflow**:
1. User submits new dates and reason
2. System validates dates
3. Modification history stored
4. Leave updated with new dates
5. Approval status reset to Pending
6. Re-approval required from all levels

**Restrictions**:
- Cannot modify fully approved leave (SP status = Approved)
- Use early return instead for approved leaves

**Database**: `leave_modifications` collection

### 5.5 Withdraw Leave Application
**Route**: `/leave/withdraw/<leave_id>`

**Purpose**: User withdraws leave application

**Workflow**:
1. User provides withdrawal reason
2. If already approved, balance restored
3. Leave status set to 'Withdrawn'
4. Timestamp recorded

**Restrictions**:
- Cannot withdraw leave that has already started (if SP approved)
- Can withdraw pending applications anytime

**Balance Restoration**: Automatic for Earned/Casual/Medical/Half Pay

### 5.6 Report Overstay
**Route**: `/leave/overstay/report/<leave_id>`

**Purpose**: OC reports when personnel doesn't return on time

**Workflow**:
1. OC specifies actual return date
2. System calculates overstay days
3. **Conversion Logic**:
   - First 10 days → Half Pay Leave (deducted from balance)
   - Remaining days → Extraordinary Leave (not deducted)
4. Overstay record created
5. Leave record updated with conversion details
6. SDPO and SP notified

**Notifications**: Automatic to senior officers

**Database**: `leave_overstays` collection

### 5.7 Report Absence Without Leave
**Route**: `/leave/absence/report`

**Purpose**: OC reports absence without prior leave application

**Workflow**:
1. OC specifies user, dates, and reason
2. Absence record created
3. **Retrospective Leave Created**:
   - Type: Extraordinary Leave
   - Status: Approved by OC, Pending SDPO/SP
   - Flag: `retrospective: True`, `disciplinary_flag: True`
4. Senior officers notified for disciplinary action

**Purpose**: Documentation and disciplinary tracking

**Database**: `leave_absences` and `leaves` collections

---

## 6. Notifications System

### 6.1 Notification Triggers
- Leave application submitted
- Leave approved/rejected at each level
- Commutation request status
- Recall to duty issued
- Early return request status
- Overstay reported
- Absence without leave reported

### 6.2 Notification Fields
```python
{
    'user_id': 'Recipient user ID',
    'title': 'Notification title',
    'message': 'Notification message',
    'type': 'leave',
    'is_read': False,
    'created_at': datetime.now()
}
```

---

## 7. PDF Generation

### 7.1 Leave Order PDF
**Route**: `/leave/generate_pdf/<leave_id>`

**Content**:
- Government header
- Order number
- Personnel details
- Leave type (with LTC status if applicable)
- Start and end dates
- Number of days
- Station/charge during leave
- Prefix/suffix dates (if any)
- Medical certificate reference (if uploaded)
- Reason for leave
- Signatures (right-aligned):
  - OC
  - SDPO
  - Superintendent of Police

**Features**:
- Professional formatting with ReportLab
- Signature alignment: RIGHT
- Download as PDF attachment

---

## 8. Database Collections

### 8.1 Primary Collection: `leaves`
**Fields**:
- Basic: user_id, leave_type, start_date, end_date, num_days, reason
- LTC: ltc_availed
- Maternity: maternity_type, surviving_children
- Paternity: surviving_children_pat, delivery_date
- Adoption: surviving_children_adopt, adoption_date, child_age (months)
- Child Care: child_age_care (years), care_reason
- Prefix/Suffix: has_prefix_suffix, prefix_dates, suffix_dates
- Documents: medical_certificate, other_documents, document_title
- Approval: status, oc_status, sdpo_status, sp_status
- Recommended: original_num_days, oc_recommended_days, sdpo_recommended_days, sp_recommended_days
- Approvers: oc_id, sdpo_id, sp_id
- Timestamps: applied_on, oc_approved_at, sdpo_approved_at, sp_approved_at
- Flags: modified, commuted, recalled, early_return, overstayed, retrospective, disciplinary_flag

### 8.2 Supporting Collections
1. **leave_commutations**: Commutation requests
2. **leave_recalls**: Recall to duty records
3. **leave_early_returns**: Early return requests
4. **leave_modifications**: Modification history
5. **leave_overstays**: Overstay incidents
6. **leave_absences**: Absence without leave records

---

## 9. API Endpoints Summary

### Leave Application
- `GET /leave/apply` - Show leave application form
- `POST /leave/apply` - Submit leave application
- `GET /leave/index` - View all leave applications
- `GET /leave/view/<leave_id>` - View specific leave

### Approval
- `POST /leave/approve/<leave_id>` - Approve/reject leave (OC/SDPO/SP)
- `GET /leave/generate_pdf/<leave_id>` - Generate leave order PDF

### Commutation
- `POST /leave/commutation/request/<leave_id>` - Request commutation
- `POST /leave/commutation/approve/<commutation_id>` - SP approves commutation

### Recall
- `GET /leave/recall/create` - Show recall form with active leaves
- `POST /leave/recall/create` - Create recall order

### Early Return
- `POST /leave/return_early/<leave_id>` - Request early return
- `POST /leave/early_return/approve/<return_id>` - Approve early return

### Modification & Withdrawal
- `POST /leave/modify/<leave_id>` - Modify leave dates
- `POST /leave/withdraw/<leave_id>` - Withdraw application

### Reporting
- `POST /leave/overstay/report/<leave_id>` - Report overstay
- `POST /leave/absence/report` - Report absence without leave

---

## 10. Frontend Templates Required

### 10.1 Existing (Updated)
- `templates/leave/apply.html` - ✅ Complete with all 9 types

### 10.2 New Templates Needed
1. `templates/leave/recall_create.html` - Recall to duty form
2. Views need update to show:
   - Commutation request button
   - Early return request form
   - Modify dates form
   - Withdraw button
   - Overstay report form (OC only)
   - Absence report form (OC only)

---

## 11. User Roles & Permissions

### Personnel (Constable, Head Constable, ASI, SI, Inspector)
- Apply for leave
- View own leave applications
- Request commutation
- Request early return
- Modify pending leaves
- Withdraw leaves

### Officer in Charge (Inspector)
- All personnel permissions
- Approve/reject at OC level
- Modify recommended days
- Report overstay
- Report absence without leave

### SDPO
- All OC permissions
- Approve/reject at SDPO level
- Modify recommended days

### SP (Superintendent of Police)
- All SDPO permissions
- Final approval authority
- Approve commutations
- Recall personnel from leave
- Approve early returns (final)

---

## 12. Validation Summary

### Maternity Leave
- Pregnancy: ≤180 days, <2 children
- Miscarriage: ≤45 days lifetime total, <2 children
- Medical certificate required

### Paternity Leave
- ≤15 days
- <2 surviving children
- Within 15 days before to 6 months after delivery

### Adoption Leave
- ≤135 days
- Child age <12 months
- <2 surviving children

### Child Care Leave
- Child age <18 years
- 730 days lifetime balance
- 4 care reasons available

### General
- End date must be after start date
- Suspended users cannot apply
- Balance check for debited types
- Document upload validation

---

## 13. Implementation Status

### ✅ Completed
- All 9 leave types with validation
- Leave application form with conditional fields
- Document upload functionality
- Multi-level approval workflow
- Recommended days tracking
- Balance management
- Commutation workflow
- Recall to duty
- Early return
- Leave modification
- Leave withdrawal
- Overstay reporting
- Absence without leave reporting
- Suspension check
- PDF generation (with right-aligned signature)

### ⏳ Pending Frontend
- Recall to duty form template
- View template updates for new features
- Commutation request UI
- Early return request UI
- Modify dates UI
- Withdraw confirmation UI
- Overstay report form
- Absence report form

---

## 14. Testing Checklist

### Leave Application
- [ ] All 9 leave types can be selected
- [ ] Conditional fields show/hide correctly
- [ ] Client-side validation works
- [ ] Server-side validation catches errors
- [ ] Document upload works
- [ ] Prefix/suffix dates stored correctly
- [ ] Suspension check blocks application

### Approval Workflow
- [ ] OC can approve/reject
- [ ] SDPO can approve/reject after OC
- [ ] SP can approve/reject after SDPO
- [ ] Recommended days tracked at each level
- [ ] Notifications sent at each level

### Balance Management
- [ ] Balance deducted for debited types
- [ ] Balance not deducted for non-debited types
- [ ] Maternity leave tracked separately
- [ ] Child care balance tracked correctly
- [ ] Balance restored on withdrawal
- [ ] Balance restored on early return
- [ ] Balance restored on recall

### Advanced Features
- [ ] Commutation creates request
- [ ] SP can approve commutation
- [ ] Balance swapped correctly on commutation
- [ ] Recall updates leave and balance
- [ ] Early return restores balance
- [ ] Modification resets approval
- [ ] Withdrawal restores balance
- [ ] Overstay converts correctly (Half Pay + Extraordinary)
- [ ] Absence creates retrospective leave

### PDF Generation
- [ ] PDF generates with all fields
- [ ] Signatures right-aligned
- [ ] LTC status shown for Earned Leave
- [ ] Special fields shown for each leave type
- [ ] Document references included

---

## 15. Database Initialization

### Update Existing Users
Run this script to add new fields to existing users:

```python
from extensions import mongo

db = mongo.db

# Update all users with new leave balance fields
db.users.update_many(
    {},
    {
        '$set': {
            'half_pay_leave_balance': 20,
            'child_care_leave_balance': 730,
            'maternity_leave_used': 0,
            'maternity_miscarriage_leave_used': 0,
            'is_suspended': False
        }
    }
)

print("All users updated with new leave fields")
```

---

## 16. Security Considerations

### File Upload Security
- `secure_filename()` used for all uploads
- Timestamp added to prevent collisions
- File extension validation
- Upload directory permissions

### Authorization Checks
- Ownership checks for leave modification
- Role-based access for approval
- OC-only functions for reporting
- SP-only functions for recall and commutation

### Data Validation
- Server-side validation for all inputs
- Date validation
- Balance checks
- Child count validation
- Duration limit checks

---

## 17. Future Enhancements

### Potential Additions
1. **Charge Assignment**: Select replacement during leave approval
2. **Leave Calendar**: Visual calendar showing all leaves
3. **Leave Statistics**: Dashboard with leave analytics
4. **Bulk Operations**: Import/export leave data
5. **Leave Encashment**: Convert unused leave to payment
6. **Leave Transfer**: Transfer leave balance between types
7. **Medical Certificate Verification**: Workflow for certificate validation
8. **Auto-Approval**: Automatic approval for certain conditions
9. **Leave Forecasting**: Predict leave requirements
10. **Mobile App Integration**: Push notifications

---

## Document Version
- **Version**: 1.0
- **Last Updated**: December 2024
- **Status**: All backend routes implemented, frontend templates pending
