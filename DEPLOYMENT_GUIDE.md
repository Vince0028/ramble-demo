# Render Deployment Guide

## 🚀 Deploying Ramble App to Render

### **Step 1: Set up Supabase Database**

Before deploying, you need to set up your Supabase database:

1. **Create Supabase account** at https://supabase.com
2. **Create a new project**
3. **Get your credentials**:
   - Go to Settings > API
   - Copy the "Project URL" (SUPABASE_URL)
   - Copy the "anon public" key (SUPABASE_KEY)
4. **Create database tables** using the SQL from `CHAT_SETUP_GUIDE.md`

### **Step 2: Update render.yaml**

Replace the placeholder values in `render.yaml`:

```yaml
envVars:
  - key: SUPABASE_URL
    value: your-actual-supabase-url-here
  - key: SUPABASE_KEY
    value: your-actual-supabase-key-here
```

### **Step 3: Deploy to Render**

1. **Push your code** to GitHub
2. **Connect Render** to your GitHub repository
3. **Use the render.yaml** configuration
4. **Set environment variables** in Render dashboard if needed

### **Step 4: Verify Deployment**

After deployment, check:

1. **Homepage loads** correctly
2. **Login/signup** works
3. **Chat feature** is accessible
4. **Database connection** is working

## 🔧 **Common Deployment Issues & Fixes**

### **Issue: Different page shows up**

**Cause**: Missing environment variables or database connection issues

**Fix**:
1. Check Supabase credentials in Render dashboard
2. Verify database tables exist
3. Check Render logs for errors

### **Issue: "Failed to create user"**

**Cause**: Database not connected

**Fix**:
1. Add SUPABASE_URL and SUPABASE_KEY to Render environment variables
2. Create database tables in Supabase
3. Check database permissions

### **Issue: Static files not loading**

**Cause**: Incorrect file paths

**Fix**:
1. Ensure all static files are in the correct directories
2. Check file permissions
3. Verify file paths in templates

### **Issue: LinkedIn OAuth not working**

**Cause**: Incorrect redirect URI

**Fix**:
1. Update LinkedIn app settings with correct redirect URI
2. Check LINKEDIN_REDIRECT_URI in environment variables

## 📋 **Environment Variables Required**

```env
SECRET_KEY=your-secret-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
LINKEDIN_REDIRECT_URI=https://your-app.onrender.com/auth/linkedin/callback
```

## 🎯 **Production vs Development Differences**

| Feature | Development | Production |
|---------|-------------|------------|
| Server | Flask dev server | Gunicorn WSGI |
| Debug | Enabled | Disabled |
| Port | 5000 | Environment variable |
| Database | Local/Development | Production Supabase |
| Static files | Local | CDN/Static hosting |

## 🚨 **Troubleshooting Steps**

1. **Check Render logs** for error messages
2. **Verify environment variables** are set correctly
3. **Test database connection** by visiting `/api/user`
4. **Check Supabase dashboard** for database status
5. **Verify file paths** and permissions

## ✅ **Success Indicators**

Your deployment is successful when:
- ✅ Homepage loads without errors
- ✅ User registration works
- ✅ Login (email and LinkedIn) works
- ✅ Chat feature is accessible
- ✅ Database operations work
- ✅ No console errors in browser
