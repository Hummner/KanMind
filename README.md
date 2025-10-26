# 📌 KanMind – Backend API

## 🧾 Description
This is the **backend API** for the Project.  
The backend is built with **Django** and **Django REST Framework** and provides all core features required for authentication, board and task management, and comment handling.

🧠 **Frontend and backend are in separate repositories.**  
This repository contains only the backend code.

---

## 🚀 Features
- 🔐 User registration and authentication (Token-based)  
- 📝 Task & Board management  
- 🧑‍🤝‍🧑 Role and permission system  
- 💬 Comment system  
- ✅ Follows PEP8 style guide  
- 🧪 Ready for API testing with Postman or curl

---

## 🛠️ Tech Stack
- Python 3.10+
- Django
- Django REST Framework
- djangorestframework-simplejwt or Token Auth
- SQLite (or your preferred DB — not included in repo)

---

## 📂 Project Structure
```
project/
│
├── auth_app/
├── boards/
├── comments/
├── tasks/
│
├── requirements.txt
├── manage.py
└── README.md
```

---

## 🧰 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-backend-repo.git
cd your-backend-repo
```

### 2. Create & activate virtual environment
```bash
python -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 6. Start the development server
```bash
python manage.py runserver
```

Server will be available at 👉 `http://127.0.0.1:8000/`

---

## 🧪 Testing
Use `curl`, `Postman`, or any API testing tool to interact with the endpoints.  
Example:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/
```

---

## 🔐 Environment Variables
Create a `.env` file in the project root with your secrets:

```
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

🚨 **Important:** Never upload `.env` or any database files to GitHub!

---

## 📜 Requirements
All Python dependencies are listed in `requirements.txt`.  
Example:
```
asgiref==3.10.0
Django==5.2.7
djangorestframework==3.16.1
drf-nested-routers==0.95.0
sqlparse==0.5.3
tzdata==2025.2
```

Install them with:
```bash
pip install -r requirements.txt
```

---

## 🛡️ Security
- `.env` and database files are excluded in `.gitignore`  
- Tokens / credentials must **never** be committed  
- Use environment variables for sensitive data

---

## 🧑‍💻 Contributing
1. Fork the repo  
2. Create a feature branch  
3. Commit your changes  
4. Push to your branch  
5. Create a pull request

---

## 📝 License
This project is licensed under the MIT License.

---
