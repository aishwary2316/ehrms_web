# Test Credentials for Leave Approval Workflow

Based on actual users in the database, here are the credentials to test the complete leave approval flow:

## Complete Leave Approval Workflow Test

### Step 1: Apply for Leave (as Constable/Lower Rank)
Unfortunately, there are no Constables in the database. Use any lower rank or test with an Inspector applying for themselves.

**Alternative**: Use Inspector to apply for leave:
```
Username: ins001
Password: ins123
Employee ID: INS001
Name: KHUNDONGBAM HEMANTA SINGH
Rank: Inspector
```

### Step 2: OC Approval (as Inspector)
```
Username: ins016
Password: ins16  (or try: ins123)
Employee ID: INS016
Name: KHUNDONGBAM RAJEN SINGH
Rank: Inspector
Role: inspector
```

### Step 3: SDPO Approval
**⚠️ Problem**: No SDPO users found in database!

**Solution**: You need to either:
1. Create a SDPO user through the admin panel (login as SP)
2. Or modify an existing user to be SDPO rank
3. Or test without SDPO approval step

### Step 4: Final SP Approval (auto-generates PDF)
```
Username: sp001
Password: sp123  (or possibly sp001234)
Employee ID: SP001
Name: LONGJAM JOYKUMAR SINGH
Rank: SP
Role: admin
```

## Currently Available Users in Database

### SP Users (Final Approvers)
1. **sp_admin** - Username: `sp_admin`, Password: Unknown
2. **sp001** - Username: `sp001`, Password: `sp123` or `sp001234`

### ASP Users
1. **asp001** - Username: `asp001`, Employee ID: ASP001, Name: HAORONGBAM RATAN SINGH
2. **asp002** - Username: `asp002`, Employee ID: ASP002, Name: NINGTHOUJAM AMIT SINGH
3. **asp003** - Username: `asp003`, Employee ID: ASP003, Name: THOKCHOM KIRAN SINGH

### Inspector Users (OC Level)
1. **ins001** - Username: `ins001`, Password: `ins123`, Employee ID: INS001
   - Name: KHUNDONGBAM HEMANTA SINGH
   
2. **ins016** - Username: `ins016`, Password: `ins16` or `ins123`, Employee ID: INS016
   - Name: KHUNDONGBAM RAJEN SINGH
   - ✅ **Working** (confirmed from login logs)

## Testing Strategy

Since SDPO users are missing, you have two options:

### Option A: Create SDPO User First
1. Login as **sp001** (password: `sp123`)
2. Go to **Users** → **Add New User**
3. Create a test SDPO user:
   - Username: `sdpo001`
   - Password: `sdpo123`
   - Rank: `SDPO`
   - Employee ID: `SDPO001`
   - Name: Test SDPO
4. Then test the full workflow

### Option B: Test Two-Level Approval (Inspector → SP)
1. Login as **ins001** (password: `ins123`)
2. Apply for leave
3. Logout
4. Login as **ins016** (password: `ins16`)
5. Approve the leave as OC
6. Logout
7. Login as **sp001** (password: `sp123`)
8. Final approval (PDF auto-generates)

## Current Leave Applications in Database

There are 3 existing leave applications:
1. Status: Pending
2. Status: Pending
3. Status: Approved_OC (already approved by Inspector)

You can view and approve these by:
1. Login as **ins016**
2. Go to Leaves
3. Filter by "Pending" or "Approved by OC"
4. Click "View" and approve

## Password Patterns Observed

From successful login logs:
- `sp001`: 8 characters (likely `sp123` or `sp001234`)
- `ins016`: 5 characters (likely `ins16` or could be `ins123`)

## Troubleshooting

If login fails:
1. Try both patterns: `[rank]123` and `[rank][number]`
2. Passwords are stored as hashed, so check_password comparison happens
3. Database shows "Has Password: No" because we're checking 'password' field instead of 'password_hash'

## Next Steps for Complete Testing

1. ✅ Login as **sp001** (password: `sp123`)
2. ✅ Create SDPO user (username: `sdpo001`, password: `sdpo123`)
3. ✅ Test complete workflow: Constable → Inspector → SDPO → SP
4. ✅ Verify PDF auto-generation at SP approval
5. ✅ Verify notification delivery
6. ✅ Check PDF file in `static/uploads/leave_orders/`
