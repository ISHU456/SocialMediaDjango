# Bharat Connect - Django Social Media App

A modern, feature-rich social media application built with Django, featuring user profiles, posts, comments, likes, sharing, and real-time notifications.

## 🚀 Features

### Core Features
- **User Authentication**: Secure registration and login with email verification
- **User Profiles**: Customizable profiles with bio, profile pictures, and cover photos
- **Posts**: Create, edit, and delete posts with text, images, and videos
- **Comments**: Add comments to posts with threaded replies
- **Likes**: Like/unlike posts and comments
- **Sharing**: Share posts with optional comments
- **Follow System**: Follow/unfollow other users
- **Notifications**: Real-time notifications for likes, comments, follows, and shares
- **Search**: Search for posts and users
- **Privacy**: Public/private post settings

### Technical Features
- **Responsive Design**: Mobile-first design with Bootstrap 5
- **AJAX Integration**: Smooth interactions without page reloads
- **File Upload**: Support for images and videos
- **Pagination**: Efficient loading of posts and comments
- **Admin Interface**: Full Django admin integration
- **Security**: CSRF protection, user authentication, and input validation

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SocialMedia
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
SocialMedia/
├── socialmedia_project/     # Main Django project
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── core/                   # Core app (base functionality)
├── posts/                  # Posts app
│   ├── models.py          # Post, Comment, Share, Notification models
│   ├── views.py           # Post-related views
│   ├── forms.py           # Post forms
│   └── urls.py            # Post URL patterns
├── profiles/               # Profiles app
│   ├── models.py          # Profile model
│   ├── views.py           # Profile-related views
│   ├── forms.py           # Profile forms
│   └── urls.py            # Profile URL patterns
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── posts/             # Post templates
│   └── profiles/          # Profile templates
├── static/                 # Static files
│   ├── css/               # CSS stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Static images
├── media/                  # User-uploaded files
│   ├── profile_pics/      # Profile pictures
│   ├── cover_photos/      # Cover photos
│   ├── post_images/       # Post images
│   └── post_videos/       # Post videos
└── manage.py              # Django management script
```

## 🎯 Usage Guide

### For Users

1. **Registration & Login**
   - Visit the homepage and click "Sign Up"
   - Fill in your details and verify your email
   - Log in with your credentials

2. **Creating Posts**
   - Click "Create a Post" on the homepage
   - Add text content, images, or videos
   - Choose public or private visibility
   - Click "Post" to publish

3. **Interacting with Posts**
   - Like posts by clicking the heart icon
   - Add comments using the comment form
   - Share posts with your own comments
   - View detailed posts by clicking "View"

4. **Managing Your Profile**
   - Click your username in the navigation
   - Select "Profile" to view your profile
   - Click "Settings" to edit your profile
   - Upload profile pictures and cover photos

5. **Following Users**
   - Visit other users' profiles
   - Click "Follow" to follow them
   - View your followers and following lists

6. **Searching**
   - Use the search bar to find posts or users
   - Visit the "Discover" page to find new users

### For Administrators

1. **Admin Access**
   - Log in with superuser credentials
   - Access http://127.0.0.1:8000/admin/

2. **Managing Content**
   - Monitor and moderate posts and comments
   - Manage user accounts and profiles
   - View system notifications

3. **User Management**
   - View all registered users
   - Monitor user activity
   - Handle user reports (if implemented)

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Database Configuration
The app uses SQLite by default. For production, configure PostgreSQL or MySQL in `settings.py`.

### Email Configuration
For production, configure SMTP settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 🚀 Deployment

### Production Setup

1. **Set DEBUG to False**
   ```python
   DEBUG = False
   ```

2. **Configure ALLOWED_HOSTS**
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

3. **Set up static files**
   ```bash
   python manage.py collectstatic
   ```

4. **Use a production database**
   - PostgreSQL recommended for production
   - Configure database settings in `settings.py`

5. **Set up a web server**
   - Use Gunicorn with Nginx
   - Configure SSL certificates

### Docker Deployment (Optional)
Create a `Dockerfile`:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "socialmedia_project.wsgi:application"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   python manage.py makemigrations --merge
   python manage.py migrate
   ```

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic
   ```

3. **Media Files Not Accessible**
   - Ensure `MEDIA_URL` and `MEDIA_ROOT` are configured
   - Check file permissions on the media directory

4. **Email Not Sending**
   - Check email configuration in settings
   - For development, use console backend

### Support
For issues and questions:
- Check the Django documentation
- Review the project's issue tracker
- Contact the development team

## 🔮 Future Enhancements

- Real-time chat functionality
- Story/status features
- Advanced privacy controls
- API endpoints for mobile apps
- Push notifications
- Analytics dashboard
- Content moderation tools
- Advanced search filters
- Group functionality
- Event creation and management

---

**Built with ❤️ using Django** 