# 📚 **Quiz Master - V2**

Welcome to **Quiz Master - V2**, a comprehensive, multi-user, role-based quiz management system designed for educational and training environments. This project acts as an exam preparation platform for multiple courses, enabling seamless quiz creation, management, and performance tracking. Built with a modern tech stack, it integrates **Flask** for the backend, **Vue.js** for the frontend, **SQLite** for the database, and **Redis** with **Celery** for caching and background task management.

---

## 📑 **Table of Contents**

1. [🚀 Overview](#-overview)  
2. [🎯 Key Features](#-key-features)  
   - [Admin Features](#admin-features)  
   - [User Features](#user-features)  
   - [Additional Functionalities](#additional-functionalities)  
3. [🛠️ Tech Stack](#️-tech-stack)  
4. [📂 Project Structure](#-project-structure)
5. [📈 Frontend Components](#-frontend-components)
6. [⚙️ Installation Guide](#️-installation-guide)  
7. [🔑 Authentication & Authorization](#-authentication--authorization)  
8. [🌐 API Endpoints](#-api-endpoints)  
9. [🗄️ Database Schema](#️-database-schema)  
10. [⏱️ Scheduled Jobs (Batch Processing)](#️-scheduled-jobs-batch-processing)  
11. [📊 Performance Optimization & Caching](#-performance-optimization--caching)  
12. [📈 Deployment Guide](#-deployment-guide)  
13. [🗃️ Data Flow Diagram](#-data-flow-diagram)  
14. [💡 Potential Future Enhancements](#-potential-future-enhancements)  
15. [📜 Contributing Guidelines](#-contributing-guidelines)  
16. [📝 License](#-license)  

---

## 🚀 **Overview**

**Quiz Master - V2** is a scalable, dynamic, and fully-featured quiz management application. It is designed for both educational institutions and corporate environments where quizzes, exams, or assessments are conducted regularly. This project implements secure login mechanisms, role-based access, advanced quiz functionalities, and performance tracking features.

There are **two types of users** in this system:
- **Administrator (Quiz Master):** Manages the entire platform, creates quizzes, subjects, chapters, handles users, and generates analytical reports.
- **User (Student):** Registers, logs in, attempts quizzes, views results, and tracks their performance over time.

The application is designed with a **modular architecture**, allowing easy maintenance and scalability.

---

## 🎯 **Key Features**

### 👑 **Admin Features**

1. **Admin Dashboard:**
   - A centralized hub for managing all aspects of the platform.
   - Quick stats on the number of users, quizzes, active sessions, etc.

2. **Subject & Chapter Management:**
   - Add, update, and delete subjects.
   - Organize chapters under each subject with descriptions.

3. **Quiz Management:**
   - Create quizzes under specific chapters.
   - Set quiz parameters such as duration, start/end dates, and remarks.

4. **Question Management:**
   - Add multiple-choice questions (MCQs) with single correct answers.
   - Edit/delete questions within quizzes.

5. **User Management:**
   - View registered users, search, and filter users based on activity.
   - Deactivate or delete users if necessary.

6. **Analytics & Reporting:**
   - Track quiz performance metrics and generate charts.
   - Export quiz results and user reports in CSV format.

7. **Batch Processing:**
   - Schedule tasks like daily reminders or monthly performance reports using Celery.

---

### 🙋‍♂️ **User Features**

1. **Secure Registration & Login:**
   - Register with email, password, and other profile details.
   - Secure JWT-based authentication for safe access.

2. **Quiz Participation:**
   - Browse available quizzes based on subjects and chapters.
   - Participate in timed quizzes with real-time progress tracking.

3. **Performance Tracking:**
   - View quiz history with scores, time taken, and correct answers.
   - Track improvements through performance analytics.

4. **Dashboard:**
   - Personalized dashboard showing recent quizzes, performance summaries, and upcoming quizzes.

5. **Report Export:**
   - Export personal quiz history as CSV files.

---

### 🚀 **Additional Functionalities**

- **Role-Based Access Control (RBAC):** Ensures secure and restricted access to sensitive resources.
- **JWT Token Authentication:** Secures API endpoints with token-based authentication.
- **Redis Caching:** Enhances performance by caching frequently accessed data.
- **Celery for Background Tasks:** Handles asynchronous jobs like email notifications, report generation, etc.
- **Responsive UI:** Fully responsive design compatible with desktops, tablets, and mobile devices.

---

## 🛠️ **Tech Stack**

### **Frontend:**
- **Vue.js:** Modern JavaScript framework for building dynamic web applications.
- **Vue Router:** For handling client-side routing.
- **Vuex:** State management library to manage global state across components.
- **Axios:** HTTP client for making API requests to the backend.
- **Bootstrap:** CSS framework for responsive layouts and styling.

### **Backend:**
- **Flask:** Lightweight Python framework for building RESTful APIs.
- **SQLite:** Embedded SQL database for data persistence.
- **Flask-JWT-Extended:** For implementing JWT-based authentication.
- **Celery:** Asynchronous task queue for background processing.
- **Redis:** In-memory data store for caching and message brokering with Celery.

### **Other Tools:**
- **Git & GitHub:** Version control and repository hosting.
- **Postman:** For API testing and development.
- **Docker (Optional):** For containerizing the application.

---

## 📂 **Project Structure**

### **Backend Directory:**

```
backend/
├── applications/
│   ├── auth_api.py               # Handles login, registration, and token generation
│   ├── config.py                 # App configuration including database and Redis
│   ├── database.py               # Database models and initialization
│   ├── model.py                  # SQLAlchemy models for quizzes, users, scores, etc.
│   ├── quizmanagement_api.py     # CRUD operations for quizzes and related entities
│   └── user_datastore.py         # User data operations
├── app.py                        # Main Flask application entry point
├── quiz_master.db                # SQLite database file
└── requirements.txt              # Python dependencies
```

### **Frontend Directory:**

```
├── frontend/
│   ├── node_modules/                    # Node.js dependencies for Vue.js
│   ├── public/                          # Static public assets (index.html, favicon)
│   └── src/                             # Source code for Vue.js application
│       ├── api/
│       │   └── api.js                   # Handles all API requests with Axios
│       ├── assets/
│       │   └── logo.png                 # Application logo and other static files
│       ├── components/                  # Reusable Vue.js components
│       │   ├── AdminDashboardComponent.vue    # Admin dashboard UI component
│       │   ├── LoginComponent.vue             # User login form component
│       │   ├── RegisterComponent.vue          # User registration form
│       │   ├── ManageSubjects.vue              # Admin component for subject management
│       │   ├── ManageChapters.vue              # Admin component for chapter management
│       │   ├── ManageQuizzes.vue               # Admin component for quiz management
│       │   ├── ManageQuestions.vue             # Admin component to manage questions
│       │   ├── StartQuizComponent.vue          # User component to start quizzes
│       │   ├── TakeQuizComponent.vue           # User component for quiz-taking interface
│       │   ├── ScoreView.vue                   # Component to view quiz scores
│       │   └── UserDashboardComponent.vue      # User dashboard UI component
│       ├── router/
│       │   └── index.js                        # Vue Router for client-side navigation
│       ├── store/
│       │   └── index.js                        # Vuex Store for state management
│       ├── views/
│       │   ├── AdminView.vue                   # View for Admin panel
│       │   ├── HomeView.vue                    # Landing page view
│       │   └── UserView.vue                    # View for user dashboard
│       ├── App.vue                             # Main Vue.js application component
│       ├── main.js                             # Entry point for Vue.js application
│       ├── .gitignore                          # Git ignore rules
│       ├── babel.config.js                     # Babel configuration for Vue
│       ├── jsconfig.json                       # JS configuration (optional for IDE)
│       ├── package.json                        # Project metadata and npm dependencies
│       ├── package-lock.json                   # Lock file for npm to ensure consistent installs
│       └── vue.config.js                       # Vue.js project configuration            
```

## 📦 **Frontend Components**

The frontend of **Quiz Master - V2** is built with **Vue.js**, following a modular architecture. Each Vue component handles specific UI features, making the codebase organized, scalable, and easy to maintain.

### **Component List:**

1. **`AdminDashboardComponent.vue`**  
   - Displays admin statistics, quiz analytics, and user activity reports.  
   - Provides quick links for managing quizzes, subjects, and users.  

2. **`LoginComponent.vue`**  
   - Handles user and admin login functionality.  
   - Integrates with the backend authentication API to verify credentials.  

3. **`ManageChapters.vue`**  
   - Allows the admin to create, update, and delete chapters under specific subjects.  
   - Provides a dynamic list view with search and filter options.  

4. **`ManageQuestions.vue`**  
   - Used for adding, editing, and deleting quiz questions.  
   - Supports MCQ question format with single correct answers.  

5. **`ManageQuizzes.vue`**  
   - Enables the admin to create, modify, or delete quizzes under various chapters.  
   - Includes features for setting quiz duration, scheduling dates, and adding remarks.  

6. **`ManageSubjects.vue`**  
   - Admin can create, edit, or remove subjects for quizzes.  
   - Each subject can have multiple chapters linked to it.  

7. **`RegisterComponent.vue`**  
   - Facilitates new user registrations.  
   - Includes validation for user details such as email, password, and personal information.  

8. **`ScoreView.vue`**  
   - Displays quiz scores for users.  
   - Shows detailed reports including the number of correct answers, quiz duration, and performance analysis.  

9. **`StartQuizComponent.vue`**  
   - Provides users with instructions before starting a quiz.  
   - Displays quiz metadata such as title, subject, time limit, and total questions.  

10. **`TakeQuizComponent.vue`**  
    - Core component for users to attempt quizzes.  
    - Features a timer, auto-save progress, and navigation between questions.  

11. **`UserDashboardComponent.vue`**  
    - User-specific dashboard displaying attempted quizzes, upcoming quizzes, and performance stats.  
    - Provides quick links to start new quizzes and view historical scores.  

---

### 📊 **Component Interaction Flow:**

- **Admin Dashboard** ⟶ **Manage Subjects** ⟶ **Manage Chapters** ⟶ **Manage Quizzes** ⟶ **Manage Questions**  
- **User Dashboard** ⟶ **Start Quiz** ⟶ **Take Quiz** ⟶ **Score View**  

Each component communicates with the backend via **Axios** for CRUD operations and real-time data updates. State management is handled using **Vuex** to ensure smooth transitions between components.

---

## ⚙️ **Installation Guide**

### ✅ Prerequisites:
- **Python 3.10+**
- **Node.js & npm**
- **Redis Server** (Ensure Redis is installed and running)
- **Git**

---

### 📥 1. Clone the Repository:

```bash
git clone https://github.com/your-username/quiz-master-v2.git
cd quiz-master-v2
```

---

### 🐍 2. Backend Setup:

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python app.py                  # Start the Flask server
```

---

### 🌐 3. Frontend Setup:

```bash
cd frontend
npm install
npm run serve                  # Run the Vue.js development server
```

---

## 🔑 **Authentication & Authorization**

- **JWT Authentication:** Secured token-based system with role-based access.
- **Role-Based Permissions:** Only admins can manage quizzes, users, and system configurations.
- **Secure Sessions:** Tokens are stored securely in `localStorage` with automatic expiration.

---

## 🌐 **API Endpoints**

### **Authentication API:**
- `POST /api/v1/login` - User/Admin login
- `POST /api/v1/register` - User registration
- `POST /api/v1/logout` - Logout the current user

### **Subject API:**
- `GET /api/v1/subjects` - Get all subjects
- `POST /api/v1/subjects` - Add a subject
- `PUT /api/v1/subjects/:id` - Update a subject
- `DELETE /api/v1/subjects/:id` - Delete a subject

### **Quiz API:**
- `GET /api/v1/quizzes` - List quizzes
- `POST /api/v1/quizzes` - Create a quiz
- `PUT /api/v1/quizzes/:id` - Update quiz
- `DELETE /api/v1/quizzes/:id` - Delete quiz

### **User API:**
- `GET /api/v1/users` - Get all users (Admin only)
- `POST /api/v1/users` - Add user
- `DELETE /api/v1/users/:id` - Delete user

---

## 🗄️ **Database Schema**

- **Users Table:** `id`, `username`, `password`, `role`, `created_at`
- **Subjects Table:** `id`, `name`, `description`
- **Chapters Table:** `id`, `subject_id`, `name`, `description`
- **Quizzes Table:** `id`, `chapter_id`, `date_of_quiz`, `time_duration`
- **Questions Table:** `id`, `quiz_id`, `question_statement`, `options`, `correct_answer`
- **Scores Table:** `id`, `quiz_id`, `user_id`, `score`, `timestamp`

---

## ⏱️ **Scheduled Jobs (Batch Processing)**

- **Daily Reminders:** Notifies inactive users to attempt pending quizzes.
- **Monthly Reports:** Auto-generates user performance reports and sends via email.
- **CSV Export:** Users and Admins can trigger exports of quiz data asynchronously.

---

## 📊 **Performance Optimization & Caching**

- **Redis Caching:** Reduces API response times.
- **Optimized Database Queries:** Efficient SQL queries to handle large datasets.
- **Celery with Redis:** Manages background tasks like report generation without blocking the main app.

---

## 📈 **Deployment Guide**

1. Deploy **Redis** on your server.
2. Run the Flask backend using `Gunicorn` or `uWSGI`.
3. Deploy the Vue frontend with `Nginx` or `Apache`.
4. Set up Celery workers for background tasks.

---

## 💡 **Potential Future Enhancements**

- **Real-Time Quiz Leaderboards:** Track real-time scores during quizzes.
- **Gamification:** Add badges, rewards, and achievements to boost engagement.
- **Mobile App:** Build a mobile version using Vue Native or Flutter.
- **Third-Party Authentication:** Integrate OAuth (Google, GitHub) for easy login.

---

## 📜 **Contributing Guidelines**

1. Fork the repository.
2. Create your feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some amazing feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request.

---

## 📝 **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---
