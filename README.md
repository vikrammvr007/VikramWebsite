# Portfolio Website

A modern, responsive portfolio website built with Flask and Supabase, featuring a premium dark theme with admin panel for content management.

## Features

- **Modern Design**: Premium dark theme with smooth animations and transitions
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Admin Panel**: Complete CRUD operations for managing portfolio content
- **Resume Generator**: Automatic PDF resume generation with professional formatting
- **Dark/Light Mode**: Toggle between dark and light themes
- **Loading Screen**: Elegant loading animation with progress bar
- **Typewriter Effect**: Dynamic text animation for hero section
- **Scroll Progress**: Visual progress indicator while scrolling

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **PDF Generation**: ReportLab
- **Authentication**: Supabase Auth

## Project Structure

```
WebSite/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── supabase_schema.sql   # Database schema
├── .env                  # Environment variables (not in git)
├── .gitignore           # Git ignore rules
├── models/
│   ├── __init__.py
│   └── supabase_client.py    # Database operations
├── routes/
│   ├── __init__.py
│   ├── public.py            # Public routes (portfolio)
│   └── admin.py             # Admin routes (management)
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Portfolio homepage
│   ├── login.html           # Admin login
│   └── admin/               # Admin panel templates
├── static/
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   ├── js/
│   │   └── main.js          # JavaScript functionality
│   └── images/
│       └── profile.jpeg     # Profile photo
└── utils/
    ├── __init__.py
    └── resume_generator.py   # PDF resume generation
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Anaconda (recommended) or pip
- Supabase account

### 1. Environment Setup

Create a new conda environment:
```bash
conda create -n portfolio_env python=3.9
conda activate portfolio_env
```

Or use the full path if conda is not in PATH:
```bash
C:\Users\MVR\anaconda3\Scripts\conda.exe create -n portfolio_env python=3.9
C:\Users\MVR\anaconda3\Scripts\activate.bat portfolio_env
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

1. Create a new project in [Supabase](https://supabase.com)
2. Copy your project URL and API key
3. Run the database schema:
   ```sql
   -- Execute the contents of supabase_schema.sql in your Supabase SQL editor
   ```

### 4. Environment Configuration

Create a `.env` file in the project root:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SECRET_KEY=your_secret_key_for_flask_sessions
```

### 5. Admin User Setup

1. Go to Supabase Dashboard > Authentication > Users
2. Create a new user with email: `vhbrosis@gmail.com`
3. Set password: `VikramMvr@2000`

### 6. Run the Application

Using conda environment:
```bash
C:\Users\MVR\anaconda3\envs\portfolio_env\python.exe app.py
```

Or if conda is in PATH:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Public Portfolio
- Visit `http://localhost:5000` to view the portfolio
- Navigate through different sections: About, Skills, Projects, Experience, etc.
- Download resume PDF using the download button

### Admin Panel
1. Go to `http://localhost:5000/login`
2. Login with admin credentials
3. Access the dashboard to manage:
   - Personal profile information
   - Skills and skill categories
   - Projects and project categories
   - Work experience
   - Education records
   - Certifications

## Database Schema

The application uses the following main tables:
- `persons` - Personal information
- `skills` & `skill_categories` - Technical skills
- `projects` & `project_categories` - Portfolio projects
- `work_experience` - Professional experience
- `education` - Educational background
- `certifications` - Professional certifications
- `soft_skills` - Soft skills and attributes

## Deployment

### Local Testing
1. Test all functionality locally
2. Ensure database is properly seeded
3. Verify admin panel operations

### GitHub Repository
1. Push code to GitHub repository
2. Ensure `.env` file is in `.gitignore`
3. Update README with deployment instructions

### Production Deployment (Render)
1. Connect GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy and test production environment

## Admin Credentials

- **Email**: vhbrosis@gmail.com
- **Password**: VikramMvr@2000

## Support

For issues or questions, please check the database connection and ensure all environment variables are properly configured.