# GetCovered - User Management Application

## Overview

GetCovered is a full-stack web application that provides user authentication and management functionality with role-based access control. The application features Google OAuth integration, admin and client dashboards, and comprehensive user profile management.

## 🏗️ Architecture

The application follows a modern microservices architecture with:

- **Frontend**: React 18 application with routing and component-based architecture
- **Backend**: FastAPI (Python) REST API with JWT authentication
- **Database**: MySQL 8.0 with SQLAlchemy ORM
- **Authentication**: Google OAuth 2.0 integration
- **Deployment**: Docker containerization with Heroku deployment support

## 🚀 Features

### Authentication & Authorization
- Google OAuth 2.0 integration for secure sign-in
- Domain-restricted access (configurable allowed email domains)
- JWT token-based authentication
- Role-based access control (Admin/Client)
- Automatic user registration and profile creation

### User Management
- User profile creation and editing
- Admin dashboard for user management
- Client dashboard for personal profile access
- Role assignment and management
- Secure session handling

### Technical Features
- Responsive UI with Tailwind CSS
- RESTful API design
- Database migrations and schema management
- Docker containerization
- Production-ready deployment configuration

## 📁 Project Structure

```
GetCovered/
├── backend/                    # FastAPI backend application
│   ├── main.py                # Main application file with API endpoints
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend container configuration
│   ├── .env.example          # Environment variables template
│   └── create_tables.py      # Database initialization script
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── App.js            # Main application component
│   │   ├── components/       # React components
│   │   │   ├── AdminDashboard.js    # Admin interface
│   │   │   ├── ClientDashboard.js   # Client interface
│   │   │   ├── Login.js             # Authentication component
│   │   │   ├── UserProfile.js       # Profile management
│   │   │   └── EditProfile.js       # Profile editing
│   │   └── api.js           # API integration utilities
│   ├── package.json         # Frontend dependencies
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   └── Dockerfile           # Frontend container configuration
├── docker-compose.yml        # Multi-container orchestration
├── package.json             # Root package configuration
├── Procfile                 # Heroku deployment configuration
└── README.md               # Project documentation
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, high-performance Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PyMySQL**: MySQL database connector
- **Authlib**: OAuth and authentication library
- **PyJWT**: JSON Web Token implementation
- **Passlib**: Password hashing utilities
- **Uvicorn**: ASGI server implementation

### Frontend
- **React 18**: Modern JavaScript library for UI
- **React Router DOM**: Client-side routing
- **Axios**: HTTP client for API requests
- **Tailwind CSS**: Utility-first CSS framework
- **React Scripts**: Build tools and development server

### Database & Infrastructure
- **MySQL 8.0**: Relational database management system
- **Docker**: Containerization platform
- **Heroku**: Cloud platform for deployment

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ and npm 9+ (for local development)
- Python 3.10+ (for local development)
- MySQL 8.0 (for local development)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GetCovered
   ```

2. **Set up environment variables**
   ```bash
   # Backend environment
   cp backend/.env.example backend/.env
   # Edit backend/.env with your configuration

   # Frontend environment
   cp frontend/.env.example frontend/.env
   # Edit frontend/.env with your configuration
   ```

3. **Configure Google OAuth**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create OAuth 2.0 credentials
   - Add authorized redirect URI: `http://localhost:8000/auth/callback`
   - Update `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `backend/.env`

4. **Start the application**
   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Database: localhost:3306

### Local Development Setup

#### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

#### Database Setup
```sql
CREATE DATABASE getcovered_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'getcovered'@'localhost' IDENTIFIED BY 'strongpassword';
GRANT ALL PRIVILEGES ON getcovered_db.* TO 'getcovered'@'localhost';
FLUSH PRIVILEGES;
```

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)
```env
# Database Configuration
DATABASE_URL=mysql+pymysql://getcovered:strongpassword@localhost:3306/getcovered_db
MYSQL_USER=getcovered
MYSQL_PASSWORD=strongpassword
MYSQL_DATABASE=getcovered_db
DB_HOST=localhost

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Security
SECRET_KEY=your_jwt_secret_key
SESSION_SECRET_KEY=your_session_secret_key

# Application Settings
ALLOWED_EMAIL_DOMAIN=getcovered.io
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ADMIN_EMAIL=admin@getcovered.io
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

## 🔐 Authentication Flow

1. **User Login**: User clicks "Sign in with Google" on the frontend
2. **OAuth Redirect**: Frontend redirects to backend `/auth/login` endpoint
3. **Google OAuth**: Backend initiates OAuth flow with Google
4. **User Consent**: User grants permission on Google's consent screen
5. **Callback Processing**: Google redirects to backend `/auth/callback`
   - Validates user email domain against `ALLOWED_EMAIL_DOMAIN`
   - Creates user record if not exists
   - Generates JWT token
6. **Frontend Redirect**: Backend redirects to frontend with JWT token
7. **Token Storage**: Frontend stores token in localStorage
8. **Role-based Routing**: User is routed to appropriate dashboard based on role

## 🎯 API Endpoints

### Authentication
- `GET /auth/login` - Initiate Google OAuth flow
- `GET /auth/callback` - Handle OAuth callback
- `POST /auth/token` - Token refresh endpoint

### User Management
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update current user profile
- `GET /users` - List all users (admin only)
- `POST /users` - Create new user (admin only)
- `PUT /users/{user_id}` - Update user (admin only)
- `DELETE /users/{user_id}` - Delete user (admin only)

### Health Check
- `GET /` - Application health check

## 🔒 Security Features

- JWT token-based authentication
- Domain-restricted user registration
- Role-based access control
- Secure password hashing with bcrypt
- CORS protection
- Session management
- Input validation and sanitization

## 🚀 Deployment

### Heroku Deployment

The application is configured for Heroku deployment with:

- `Procfile` for process configuration
- `package.json` with Heroku build scripts
- Environment variable configuration
- Database URL handling for Heroku PostgreSQL

#### Deploy Steps:
```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set GOOGLE_CLIENT_ID=your_client_id
heroku config:set GOOGLE_CLIENT_SECRET=your_client_secret
heroku config:set SECRET_KEY=your_secret_key
heroku config:set ALLOWED_EMAIL_DOMAIN=your_domain.com

# Add database
heroku addons:create heroku-postgresql:mini

# Deploy
git push heroku main
```

### Docker Production Deployment

```bash
# Build and run in production mode
docker-compose -f docker-compose.yml up --build -d
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📈 Development Roadmap

### Immediate Improvements
- [ ] Add comprehensive test coverage
- [ ] Implement refresh token mechanism
- [ ] Add proper logging and monitoring
- [ ] Implement password reset functionality
- [ ] Add email verification

### Future Enhancements
- [ ] Multi-factor authentication (MFA)
- [ ] Advanced user permission system
- [ ] Audit logging and user activity tracking
- [ ] API rate limiting
- [ ] Real-time notifications
- [ ] Mobile application support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues

**Database Connection Issues**
- Ensure MySQL is running and accessible
- Verify database credentials in `.env` file
- Check network connectivity between containers

**Google OAuth Issues**
- Verify OAuth credentials are correctly set
- Ensure redirect URIs match in Google Cloud Console
- Check that the allowed domain is correctly configured

**Frontend Build Issues**
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version compatibility

**Backend API Issues**
- Check if all required environment variables are set
- Verify Python virtual environment is activated
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the application logs for error details

## 🙏 Acknowledgments

- FastAPI for the excellent Python web framework
- React team for the powerful frontend library
- Google for OAuth 2.0 integration
- Docker for containerization support
- All open-source contributors who made this project possible