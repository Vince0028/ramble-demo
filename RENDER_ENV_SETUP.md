# Render Environment Variables Setup Guide

## 🎯 **How to Set Environment Variables in Render**

### **Step 1: Access Your Render Service**

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on your **ramble-demo** service
3. Go to the **Environment** tab

### **Step 2: Add Required Environment Variables**

Add these environment variables one by one in the Render dashboard:

#### **Required Variables:**

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `SECRET_KEY` | `ramble-demo-secret-key-2024-production` | Flask secret key for sessions |
| `SUPABASE_URL` | `your-supabase-url-here` | Your Supabase project URL |
| `SUPABASE_KEY` | `your-supabase-anon-key-here` | Your Supabase anon key |
| `LINKEDIN_CLIENT_ID` | `862mvp7e208g5z` | LinkedIn OAuth client ID |
| `LINKEDIN_CLIENT_SECRET` | `WPL_AP1.DLvWnuIO53i8K8Gk.r22wZQ==` | LinkedIn OAuth client secret |
| `LINKEDIN_REDIRECT_URI` | `https://ramble-demo-1.onrender.com/auth/linkedin/callback` | LinkedIn redirect URI |

### **Step 3: Get Supabase Credentials**

If you don't have Supabase set up yet:

1. **Create account** at [supabase.com](https://supabase.com)
2. **Create new project**
3. **Go to Settings > API**
4. **Copy the values:**
   - **Project URL** → Use as `SUPABASE_URL`
   - **anon public** key → Use as `SUPABASE_KEY`

### **Step 4: Create Database Tables**

In your Supabase SQL Editor, run this SQL:

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

-- Create indexes
CREATE INDEX idx_messages_group_id ON messages(group_id);
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_messages_recipient_id ON messages(recipient_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_group_members_group_id ON group_members(group_id);
CREATE INDEX idx_group_members_user_id ON group_members(user_id);
CREATE INDEX idx_group_invitations_group_id ON group_invitations(group_id);
CREATE INDEX idx_group_invitations_invited_user_id ON group_invitations(invited_user_id);
```

### **Step 5: Deploy and Test**

1. **Save** all environment variables in Render
2. **Redeploy** your service (or it will auto-deploy)
3. **Check logs** for any errors
4. **Test the app** by visiting your Render URL

## 🔧 **Troubleshooting**

### **Common Issues:**

#### **"Failed to create user"**
- ✅ Check `SUPABASE_URL` and `SUPABASE_KEY` are correct
- ✅ Verify database tables exist in Supabase
- ✅ Check Supabase project is not paused

#### **"Different page shows up"**
- ✅ Verify all environment variables are set
- ✅ Check Render logs for errors
- ✅ Ensure database connection is working

#### **LinkedIn OAuth not working**
- ✅ Check `LINKEDIN_REDIRECT_URI` matches your Render URL
- ✅ Verify LinkedIn app settings
- ✅ Check `LINKEDIN_CLIENT_ID` and `LINKEDIN_CLIENT_SECRET`

### **How to Check if Environment Variables are Working:**

1. **Check Render logs** - look for "Supabase client initialized successfully"
2. **Visit `/api/user`** - should return user data or authentication error
3. **Try to sign up** - should work without "Failed to create user" error

## 📋 **Environment Variables Checklist**

- [ ] `SECRET_KEY` - Set to a secure random string
- [ ] `SUPABASE_URL` - Your Supabase project URL
- [ ] `SUPABASE_KEY` - Your Supabase anon key
- [ ] `LINKEDIN_CLIENT_ID` - Your LinkedIn app client ID
- [ ] `LINKEDIN_CLIENT_SECRET` - Your LinkedIn app client secret
- [ ] `LINKEDIN_REDIRECT_URI` - Your Render app URL + `/auth/linkedin/callback`
- [ ] Database tables created in Supabase
- [ ] Service redeployed after adding variables

## 🎯 **Expected Result**

After setting up all environment variables correctly:
- ✅ App loads the same as local development
- ✅ User registration/login works
- ✅ Chat feature is accessible
- ✅ LinkedIn OAuth works
- ✅ Database operations work
- ✅ No "Failed to create user" errors
