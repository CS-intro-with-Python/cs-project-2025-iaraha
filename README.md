# Raha2008

A modern web application for sharing media files with user authentication, social interactions, and administrative control.

---

## Features
* **User Management**: Registration and secure authentication.
* **Media Upload**: Support for images, videos, and documents.
* **Discovery Feed**: Browse all posts with high-quality previews.
* **Social Interactions**: Like/unlike posts and a full comment system.
* **Content Management**: User profile management and post deletion.
* **Admin Dashboard**: Exclusive privileges to moderate and delete any post.

---

## Technology Stack
* **Backend**: Flask (Python)
* **Database**: SQLite with SQLAlchemy ORM
* **Authentication**: Flask-Login
* **Frontend**: HTML5, Bootstrap 5
* **DevOps**: Docker, GitHub Actions (CI/CD)

---

## Installation & Setup

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone <git@github.com:CS-intro-with-Python/cs-project-2025-iaraha.git>
   cd cs-project-2025-laraha
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   cd app
   python app.py
   ```
   *Access at: http://localhost:8080*

### Docker Setup
1. **Build the image:**
   ```bash
   docker build -t media-app .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8080:8080 media-app
   ```

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/` | Main page with all posts |
| GET/POST | `/register` | User registration |
| GET/POST | `/login` | User authentication |
| GET | `/logout` | User logout |
| GET/POST | `/upload` | Media file upload |
| GET | `/post/<int:post_id>` | View specific post |
| POST | `/post/<int:post_id>` | Handle interactions (like, comment, delete) |

> **Admin Access:** The first registered user automatically becomes the administrator.  
> **Default credentials (for testing):** Username: `admin` | Password: `admin123`

---

## Project Structure
```text
cs-project-2025-laraha/
├── .github/workflows/    # CI/CD configurations
├── app/
│   ├── templates/         # HTML templates (JinJa2)
│   ├── uploads/           # Storage for uploaded media
│   ├── app.py            # Main entry point
│   ├── models.py         # Database schema
│   └── routes.py         # App logic and routing
├── Dockerfile            # Container configuration
├── requirements.txt      # Project dependencies
└── README.md            # Documentation
```

---

##  Configuration & Formats
* **Port**: 8080
* **Database**: SQLite (media.db)
* **Upload Folder**: uploads/

**Supported File Formats:**
*  **Images**: JPG, JPEG, PNG, GIF
*  **Video**: MP4, AVI, MOV
*  **Documents**: PDF, TXT, DOC, DOCX