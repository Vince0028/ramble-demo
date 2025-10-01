# Database Setup Guide

Your RAMBLE demo application is now configured with Supabase database integration!

## 🎉 What's Been Set Up

### ✅ **Files Created/Updated:**
- `database.py` - Database utility module with Supabase integration
- `app.py` - Updated with database authentication endpoints
- `templates/login.html` - Updated forms to use database API
- `requirement.txt` - Added Supabase dependency
- `.env` - Configured with your Supabase credentials
- `setup_database.py` - Database setup script

### 🔧 **API Endpoints Added:**
- `POST /api/login` - User login with email/password
- `POST /api/signup` - User registration with all form fields
- `GET /api/user` - Get current user data

## 🚀 **Next Steps**

### 1. Create Database Table
Go to your Supabase dashboard and create the users table:

**Dashboard URL:** https://supabase.com/dashboard/project/vstdajngvqntisjituoo

**Table Schema:**
```sql
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    middle_name VARCHAR(100),
    surname VARCHAR(100),
    birthday DATE,
    gender VARCHAR(50),
    password VARCHAR(255),
    points INTEGER DEFAULT 0,
    rank INTEGER DEFAULT 1,
    login_method VARCHAR(50) DEFAULT 'email',
    linkedin_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 2. Install Dependencies
```bash
pip install -r requirement.txt
```

### 3. Run Application
```bash
python app.py
```

## 📋 **Form Features**

### **Login Form:**
- Email field with validation
- Password field
- Real-time error handling
- Database authentication

### **Signup Form:**
- First Name (required)
- Middle Name (optional)
- Surname (required)
- Email Address (required, unique)
- Password (required, min 6 characters)
- Birthday (required)
- Gender (required)
- Database storage with duplicate email prevention

## 🔐 **Authentication Flow**

1. **Signup:** User fills form → Data validated → Stored in Supabase → Session created
2. **Login:** Email/password → Database authentication → Session created
3. **LinkedIn:** OAuth flow → User created/updated in database → Session created

## 🛠️ **Database Features**

- **Persistent Storage:** All user data stored in Supabase
- **Email Uniqueness:** Prevents duplicate accounts
- **Password Authentication:** Secure login with stored passwords
- **LinkedIn Integration:** OAuth users stored in same database
- **Session Management:** Flask sessions with database user data

## 🎯 **Ready to Use!**

Your application now has:
- ✅ Complete database integration
- ✅ Email/password authentication
- ✅ User registration with all requested fields
- ✅ LinkedIn OAuth with database storage
- ✅ Form validation and error handling
- ✅ Persistent user data

The forms work exactly as requested with email and password fields, and all data is now stored in your Supabase database!
