# Chat Feature Setup Guide

## 🚨 "Failed to create user" Error Fix

This error occurs because the Supabase database is not configured. Follow these steps:

### Step 1: Create .env file
Create a `.env` file in the `ramble-demo` directory with:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-this

# Supabase Configuration
# Get these from your Supabase project dashboard
SUPABASE_URL=your-supabase-url-here
SUPABASE_KEY=your-supabase-anon-key-here

# LinkedIn OAuth Configuration
LINKEDIN_CLIENT_ID=862mvp7e208g5z
LINKEDIN_CLIENT_SECRET=WPL_AP1.DLvWnuIO53i8K8Gk.r22wZQ==
LINKEDIN_REDIRECT_URI=http://localhost:5000/auth/linkedin/callback
```

### Step 2: Set up Supabase Database

1. **Create a Supabase account** at https://supabase.com
2. **Create a new project**
3. **Get your credentials**:
   - Go to Settings > API
   - Copy the "Project URL" (SUPABASE_URL)
   - Copy the "anon public" key (SUPABASE_KEY)
4. **Update your .env file** with these credentials

### Step 3: Create Database Tables

Run this SQL in your Supabase SQL Editor:

```sql
-- Users table
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
    profile_picture_url TEXT,
    is_online BOOLEAN DEFAULT FALSE,
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Groups table
CREATE TABLE groups (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_by UUID REFERENCES users(id) ON DELETE CASCADE,
    is_private BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Group members table
CREATE TABLE group_members (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(group_id, user_id)
);

-- Messages table
CREATE TABLE messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    sender_id UUID REFERENCES users(id) ON DELETE CASCADE,
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    recipient_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'text',
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Group invitations table
CREATE TABLE group_invitations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    invited_by UUID REFERENCES users(id) ON DELETE CASCADE,
    invited_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    responded_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for better performance
CREATE INDEX idx_messages_group_id ON messages(group_id);
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_messages_recipient_id ON messages(recipient_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_group_members_group_id ON group_members(group_id);
CREATE INDEX idx_group_members_user_id ON group_members(user_id);
CREATE INDEX idx_group_invitations_group_id ON group_invitations(group_id);
CREATE INDEX idx_group_invitations_invited_user_id ON group_invitations(invited_user_id);
```

### Step 4: Test the Setup

1. **Start the app**: `python app.py`
2. **Try to sign up** with email or LinkedIn
3. **Check the console** for any error messages

### Step 5: Verify Database Connection

The app will log database connection status. Look for:
- ✅ "Supabase client initialized successfully" = Good
- ❌ "Database not connected" = Check your .env file

## 🎯 Chat Features Available After Setup

- ✅ Private messaging between users
- ✅ Group creation and management
- ✅ User discovery and online status
- ✅ LinkedIn profile integration
- ✅ Group invitations system
- ✅ Real-time chat interface

## 🔧 Troubleshooting

### Still getting "Failed to create user"?

1. **Check .env file exists** and has correct Supabase credentials
2. **Verify Supabase project is active** (not paused)
3. **Check database tables exist** in Supabase dashboard
4. **Look at console logs** for specific error messages
5. **Test database connection** by visiting `/api/user` endpoint

### Common Issues:

- **Missing .env file**: Create it with Supabase credentials
- **Wrong credentials**: Double-check URL and key from Supabase
- **Tables don't exist**: Run the SQL commands above
- **Network issues**: Check internet connection
- **Supabase project paused**: Reactivate in Supabase dashboard
