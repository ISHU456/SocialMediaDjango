# 🚀 Deployment Guide - Bharat Connect Social Media App

## Deploying to Render

### Prerequisites
- GitHub account with your project pushed
- Render account (free at render.com)

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Ensure these files are in your repository:**
   - `requirements.txt`
   - `build.sh`
   - `runtime.txt`
   - `manage.py`
   - All your Django apps

### Step 2: Deploy on Render

1. **Go to [render.com](https://render.com)** and sign up/login

2. **Click "New +" → "Web Service"**

3. **Connect your GitHub repository**

4. **Configure the service:**
   - **Name**: `bharat-connect` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn socialmedia_project.wsgi:application`
   - **Plan**: `Free`

5. **Add Environment Variables:**
   - `SECRET_KEY`: Generate a new secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com`

6. **Click "Create Web Service"**

### Step 3: Set Up Database

1. **In your Render dashboard, click "New +" → "PostgreSQL"**
2. **Choose Free plan**
3. **Copy the database URL**
4. **Go back to your web service**
5. **Add environment variable:**
   - `DATABASE_URL`: Paste the PostgreSQL URL

### Step 4: Configure Static Files

1. **In your web service settings, add:**
   - `PYTHON_VERSION`: `3.12.0`

2. **Your static files will be served automatically by WhiteNoise**

### Step 5: Deploy

1. **Render will automatically deploy your app**
2. **Wait for the build to complete**
3. **Your app will be available at: `https://your-app-name.onrender.com`**

### Step 6: Create Superuser

1. **Go to your app URL + `/admin`**
2. **Create a superuser account**
3. **Start using your social media app!**

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `your-app.onrender.com` |
| `DATABASE_URL` | Database connection | `postgresql://...` |

## Troubleshooting

### Common Issues:

1. **Build fails**: Check your `requirements.txt` and `build.sh`
2. **Static files not loading**: Ensure WhiteNoise is configured
3. **Database connection**: Verify `DATABASE_URL` is set correctly
4. **500 errors**: Check Render logs for specific error messages

### Useful Commands:

```bash
# Generate new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Check logs on Render
# Go to your service → Logs tab
```

## Features After Deployment

✅ **User Registration & Authentication**  
✅ **Post Creation with Images/Videos**  
✅ **Like, Comment, Share Posts**  
✅ **User Profiles & Following**  
✅ **Real-time Chat**  
✅ **Hashtag System**  
✅ **Search Functionality**  
✅ **Responsive Design**  

## Support

If you encounter issues:
1. Check Render logs
2. Verify environment variables
3. Ensure all files are committed to GitHub
4. Check Django settings for production readiness

Your Bharat Connect social media app is now live! 🎉 