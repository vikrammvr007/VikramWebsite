# Portfolio Website - Vikramaraj M

A modern, responsive portfolio website built with Flask and Supabase, featuring a premium dark theme with admin panel for content management.

![Portfolio Preview](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.3-red)
![Supabase](https://img.shields.io/badge/Database-Supabase-green)

## 🚀 Live Demo

- **Portfolio**: [Your Live URL Here]
- **Admin Panel**: [Your Live URL]/login

## ✨ Features

- **Modern Design**: Premium dark theme with smooth animations
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Admin Panel**: Complete CRUD operations for portfolio content
- **Resume Generator**: Automatic PDF resume generation
- **Dark/Light Mode**: Theme toggle functionality
- **Loading Screen**: Elegant loading animation
- **Typewriter Effect**: Dynamic text animation
- **Scroll Progress**: Visual progress indicator

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern animations
- **PDF Generation**: ReportLab
- **Authentication**: Supabase Auth

## 📁 Project Structure

```
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── supabase_schema.sql   # Database schema
├── models/               # Database operations
├── routes/               # URL routing (public & admin)
├── templates/            # HTML templates
├── static/               # CSS, JS, images
└── utils/                # Resume generator
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Supabase account

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vikrammvr007/VikramWebsite.git
   cd VikramWebsite
   ```

2. **Create virtual environment**
   ```bash
   python -m venv portfolio_env
   source portfolio_env/bin/activate  # On Windows: portfolio_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   
   Create a `.env` file:
   ```env
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   SECRET_KEY=your_secret_key_for_flask_sessions
   ADMIN_EMAIL=your_admin_email
   ```

5. **Database Setup**
   
   Run the SQL schema in your Supabase SQL editor:
   ```bash
   # Execute supabase_schema.sql in Supabase Dashboard
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

Visit `http://localhost:5000` to view the portfolio!

## 🔐 Admin Access

- **URL**: `/login`
- **Features**: Manage profile, skills, projects, experience, education, certifications

## 📱 Responsive Design

The website is fully responsive and optimized for:
- Desktop (1920px+)
- Laptop (1024px - 1919px)
- Tablet (768px - 1023px)
- Mobile (320px - 767px)

## 🎨 Design Features

- **Premium Dark Theme** with light mode toggle
- **Smooth Animations** using CSS transitions and AOS library
- **Gradient Effects** and glass morphism design
- **Interactive Elements** with hover effects
- **Loading Screen** with progress animation
- **Scroll Progress Bar** for better UX

## 📄 Resume Generation

Automatic PDF resume generation with:
- Professional Times New Roman formatting
- Single-page optimized layout
- Dynamic content from database
- Download functionality

## 🚀 Deployment

### Render Deployment

1. Connect GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy with automatic builds

### Environment Variables for Production

```env
SUPABASE_URL=your_production_supabase_url
SUPABASE_KEY=your_production_supabase_key
SECRET_KEY=your_production_secret_key
ADMIN_EMAIL=your_admin_email
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Vikramaraj M**
- GitHub: [@vikrammvr007](https://github.com/vikrammvr007)
- Email: vhbrosis@gmail.com
- LinkedIn: [Your LinkedIn Profile]

## 🙏 Acknowledgments

- Flask community for the excellent framework
- Supabase for the backend-as-a-service platform
- Bootstrap for responsive components
- Font Awesome for icons

---

⭐ **Star this repository if you found it helpful!**