# Leave Type Gender-Specific Rules - Implementation Summary

## ✅ Gender-Based Validation Rules Implemented

### 1. **Maternity Leave** - Female Only ♀️
**Rule**: Only female employees can apply for maternity leave.

**Validation Implemented**:
- **Backend**: `routes/leave.py` - Line ~220
  ```python
  if user_doc.get('gender', '').lower() not in ['female', 'f']:
      return 'Maternity leave is only available for female employees.'
  ```
- **Frontend**: `templates/leave/apply.html`
  - Option hidden for non-female users via JavaScript
  - Option label includes "(Female Only)"
  - Disabled and hidden from dropdown for male users

**Additional Rules**:
- **Pregnancy**: Max 180 days, less than 2 surviving children required
- **Miscarriage/Abortion**: Max 45 days lifetime total

---

### 2. **Paternity Leave** - Male Only ♂️
**Rule**: Only male employees can apply for paternity leave.

**Validation Implemented**:
- **Backend**: `routes/leave.py` - Line ~232
  ```python
  if user_doc.get('gender', '').lower() not in ['male', 'm']:
      return 'Paternity leave is only available for male employees.'
  ```
- **Frontend**: `templates/leave/apply.html`
  - Option hidden for non-male users via JavaScript
  - Option label includes "(Male Only)"
  - Disabled and hidden from dropdown for female users

**Additional Rules**:
- Max 15 days
- Less than 2 surviving children required
- Must be applied within 15 days before to 6 months after delivery date

---

### 3. **Adoption Leave** - Conditional Gender Rules 👶
**Rule**: 
- **Female employees**: Can apply freely
- **Male employees**: ONLY if commissioning mother is **dead** OR has **abandoned the child**

**Validation Implemented**:
- **Backend**: `routes/leave.py` - Line ~249
  ```python
  gender = user_doc.get('gender', '').lower()
  if gender in ['male', 'm']:
      mother_status = form_data.get('mother_status', '')
      if mother_status not in ['dead', 'abandoned']:
          return 'Adoption leave for male employees is only available if the commissioning mother is dead or has abandoned the child.'
  elif gender not in ['female', 'f']:
      return 'Adoption leave is available for female employees or male employees if mother is dead/abandoned.'
  ```

- **Frontend**: `templates/leave/apply.html`
  - **New Field Added**: "Status of Commissioning Mother" dropdown
    - Options: "Dead" or "Abandoned the Child"
    - Only shown for male employees
    - Required field for male applicants
  - JavaScript validation checks mother_status for male employees
  - Shown to all genders but with conditional required field

**Additional Rules**:
- Max 135 days
- Less than 2 surviving children required
- Child must be below 1 year old (0-11 months)

---

### 4. **Child Care Leave** - Female Only ♀️
**Rule**: Only female employees can apply for child care leave.

**Validation Implemented**:
- **Backend**: `routes/leave.py` - Line ~265
  ```python
  if user_doc.get('gender', '').lower() not in ['female', 'f']:
      return 'Child Care leave is only available for female employees.'
  ```
- **Frontend**: `templates/leave/apply.html`
  - Option hidden for non-female users via JavaScript
  - Option label includes "(Female Only)"
  - Disabled and hidden from dropdown for male users

**Additional Rules**:
- 730 days total for entire service (lifetime limit)
- Child must be below 18 years
- Reasons: Rearing, Examination, Sickness, Other

---

### 5. **Other Leave Types** - Gender Neutral
- ✅ **Earned Leave** - Available to all
- ✅ **Casual Leave** - Available to all
- ✅ **Medical Leave** - Available to all
- ✅ **Half Pay Leave** - Available to all
- ✅ **Extraordinary Leave** - Available to all
- ✅ **Leave Not Due** - Available to all

---

## 🔧 Technical Implementation Details

### Frontend (JavaScript) - `templates/leave/apply.html`

#### Gender-Based Filtering Function:
```javascript
const userGender = '{{ current_user.gender | lower }}';

function filterLeaveTypesByGender() {
    const leaveTypeSelect = document.getElementById('leave_type');
    const options = leaveTypeSelect.options;
    
    for (let i = 0; i < options.length; i++) {
        const option = options[i];
        
        // Maternity Leave - Female only
        if (option.value === 'Maternity' && !['female', 'f'].includes(userGender)) {
            option.style.display = 'none';
            option.disabled = true;
        }
        
        // Paternity Leave - Male only
        if (option.value === 'Paternity' && !['male', 'm'].includes(userGender)) {
            option.style.display = 'none';
            option.disabled = true;
        }
        
        // Child Care Leave - Female only
        if (option.value === 'Child Care' && !['female', 'f'].includes(userGender)) {
            option.style.display = 'none';
            option.disabled = true;
        }
    }
}
```

#### Dynamic Field Display for Adoption Leave:
```javascript
if (leaveType === 'Adoption') {
    document.getElementById('adoption_fields').style.display = 'block';
    // Show mother status field only for male employees
    if (['male', 'm'].includes(userGender)) {
        document.getElementById('mother_status_field').style.display = 'block';
        document.getElementById('mother_status').required = true;
    } else {
        document.getElementById('mother_status_field').style.display = 'none';
        document.getElementById('mother_status').required = false;
    }
}
```

#### Client-Side Validation for Adoption Mother Status:
```javascript
if (leaveType === 'Adoption') {
    // Check mother status for male employees
    if (['male', 'm'].includes(userGender)) {
        const motherStatus = document.getElementById('mother_status').value;
        if (!motherStatus) {
            alert('Please specify the status of the commissioning mother (required for male employees)');
            return false;
        }
    }
    // ... other validations
}
```

### Backend (Python) - `routes/leave.py`

#### Validation Function Enhancements:
- ✅ Gender check added to `validate_leave_application()` function
- ✅ Checks `user_doc.get('gender', '').lower()` for case-insensitive matching
- ✅ Supports both full names ('female', 'male') and abbreviations ('f', 'm')
- ✅ Returns clear error messages for gender violations
- ✅ Mother status validation for male adoption leave applicants

#### Data Storage:
- ✅ `mother_status` field added to leave document
- ✅ Stored when `leave_type == 'Adoption'`
- ✅ Values: 'dead' or 'abandoned'

---

## 🎯 User Experience Features

### Visual Indicators:
1. **Dropdown Options**: 
   - Labels include gender restrictions (e.g., "Maternity Leave (Female Only)")
   - Tooltips on hover show eligibility criteria
   
2. **Help Text**:
   - "Note: Some leave types are gender-specific based on government rules"

3. **Dynamic Form**:
   - Only relevant leave types shown in dropdown
   - Ineligible options hidden and disabled
   - Conditional fields appear based on selection

### Error Messages:
- Clear, user-friendly error messages
- Specific to the violation (gender, child count, duration, etc.)
- Displayed both client-side (JavaScript alerts) and server-side (Flask flash messages)

### Validation Layers:
1. **Client-Side**: JavaScript prevents submission with invalid data
2. **Server-Side**: Python validates all rules before saving
3. **Database**: Gender stored in user record, leave type stored in leave document

---

## 📋 Complete Validation Matrix

| Leave Type | Gender | Max Duration | Child Count | Special Conditions |
|------------|--------|--------------|-------------|-------------------|
| Earned Leave | All | Varies | N/A | With/Without LTC |
| Casual Leave | All | 15 days/year | N/A | None |
| Medical Leave | All | 12 days/year | N/A | Medical certificate may be needed |
| Half Pay Leave | All | 20 days | N/A | Half salary |
| Extraordinary Leave | All | No limit | N/A | Not debited from balance |
| **Maternity Leave** | **Female Only** | **180 days** | **< 2** | Pregnancy: 135-180 days<br>Miscarriage: 45 days lifetime |
| **Paternity Leave** | **Male Only** | **15 days** | **< 2** | Within 15 days before to 6 months after delivery |
| **Adoption Leave** | **Female OR Male*** | **135 days** | **< 2** | ***Male only if mother dead/abandoned**<br>Child < 1 year old |
| **Child Care Leave** | **Female Only** | **730 days lifetime** | N/A | Child < 18 years<br>Rearing/Exam/Sickness |
| Leave Not Due | All | No limit | N/A | When no balance left |

---

## 🧪 Testing Checklist

### Test Cases for Gender Validation:

#### Female User:
- [x] Can see: Maternity Leave
- [x] Can see: Child Care Leave
- [x] Can see: Adoption Leave (no mother status required)
- [x] Cannot see: Paternity Leave (hidden)
- [x] Can apply for Maternity with valid conditions
- [x] Can apply for Child Care with valid child age
- [x] Can apply for Adoption without mother status

#### Male User:
- [x] Can see: Paternity Leave
- [x] Can see: Adoption Leave (mother status REQUIRED)
- [x] Cannot see: Maternity Leave (hidden)
- [x] Cannot see: Child Care Leave (hidden)
- [x] Can apply for Paternity with valid conditions
- [x] Can apply for Adoption ONLY if mother status = 'dead' or 'abandoned'
- [x] Adoption form shows "Status of Commissioning Mother" dropdown
- [x] Adoption validation fails if mother status not selected

#### Validation Tests:
- [x] Backend rejects Maternity for male users
- [x] Backend rejects Paternity for female users
- [x] Backend rejects Child Care for male users
- [x] Backend rejects Adoption for male without valid mother status
- [x] Frontend hides ineligible options
- [x] Frontend makes mother status required for male adoption applicants
- [x] Client-side validation alerts user before submission
- [x] Server-side validation catches any bypass attempts

---

## 📝 Database Schema Updates

### User Collection:
```javascript
{
    _id: ObjectId,
    name: String,
    gender: String,  // Values: 'Male', 'Female', 'M', 'F' (case-insensitive)
    // ... other fields
}
```

### Leaves Collection:
```javascript
{
    _id: ObjectId,
    user_id: String,
    leave_type: String,
    gender: String,  // Copied from user for audit
    
    // Adoption Leave specific (NEW FIELD):
    mother_status: String,  // Values: 'dead', 'abandoned' (only for male adoption leave)
    
    // Other fields...
}
```

---

## 🔒 Security Considerations

### Protection Against Manipulation:
1. **Client-Side**: Options hidden via CSS and disabled attribute
2. **Server-Side**: Full validation on backend regardless of frontend
3. **Database**: User gender fetched from database, not from form
4. **Audit Trail**: Gender stored in leave record for historical accuracy

### Bypass Prevention:
- Even if user manipulates HTML/JavaScript, backend validation will catch violations
- Gender fetched from authenticated user's database record
- Form data not trusted for gender determination
- All rules enforced on server before database insert

---

## ✅ Implementation Complete

All gender-specific leave rules have been fully implemented with:
- ✅ Backend validation in `routes/leave.py`
- ✅ Frontend filtering in `templates/leave/apply.html`
- ✅ JavaScript validation and dynamic forms
- ✅ Clear user feedback and error messages
- ✅ Database field for mother status (adoption)
- ✅ Security against manipulation attempts
- ✅ User-friendly interface with helpful labels

**Status**: Production Ready! 🚀
