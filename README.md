# 🐄 Enkang Livestock Tracker

**A full-stack livestock management system designed for Maasai herders to track cattle health, detect fevers, and manage their herds efficiently—built with a focus on offline-first architecture and enterprise-grade patterns.**

> **"Enkang"** (Maasai for *homestead* or *enclosure*) represents the heart of the community. This app brings digital herd management to the manyatta.

---

## 📸 Screenshots

*(Add your screenshots here!)*
> Example: Login Page | Herd Dashboard | Health Alerts | Profile Settings

---

## 🚀 Features (Modules A, B & C)

| Module | Feature | Description |
| :--- | :--- | :--- |
| **A (Auth)** | JWT Authentication | Secure registration & login using `bcrypt` hashing and `python-jose` tokens. |
| **A (Profile)** | User Settings | View username, update email, and securely change passwords (requires current password). |
| **B (Herd)** | Pagination & Search | Browse your livestock with `limit`/`skip` pagination. Search for animals by name instantly. |
| **B (Checkup)** | Health Logging | Record daily temperatures, milk yields, and appetite (Good/Low/None). |
| **B (Alerts)** | Smart Health Warnings | Automatically detects **Fever** (>39.5°C) or **Low Milk & Appetite** and displays alerts. |
| **C (Safety)** | Soft Delete | Animals are never permanently deleted. Restore them easily from the "Show Deleted" view. |
| **C (UX)** | Responsive UI | Works on desktop, tablets, and mobile phones (field-ready for herders). |

---

## 🛠️ Tech Stack

**Backend**
- **Python 3.12** + **FastAPI** (High-performance API framework)
- **SQLAlchemy** ORM (Database abstraction)
- **SQLite** (Local file-based database, zero configuration)
- **JWT** (Authentication via `python-jose`)
- **Bcrypt** (Password hashing without `passlib` compatibility issues)

**Frontend**
- **Vanilla HTML5, CSS3 & JavaScript** (No heavy frameworks, runs in any browser)
- **Font Awesome** (Icons)
- **Google Inter** (Typography)

---

## 📁 Project Structure
maasai-herd-tracker/
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI app, endpoints, CORS
│ │ ├── models.py # SQLAlchemy tables (User, Animal, HealthRecord)
│ │ ├── schemas.py # Pydantic validation models
│ │ ├── auth.py # JWT creation, bcrypt hashing, get_current_user
│ │ └── database.py # SQLite connection setup
│ ├── livestock.db # (Auto-generated) SQLite database file
│ └── requirements.txt # Python dependencies
├── frontend/
│ └── index.html # Single-page application (all CSS + JS)
└── README.md # This file



---

## ⚙️ Installation & Setup (Local Development)

Follow these steps to get the application running on your machine:

### Prerequisites
- **Python 3.10+** installed.
- **Git** (to clone the repository).

### Step 1: Clone the repository
```bash
git clone https://github.com/your-username/maasai-herd-tracker.git
cd maasai-herd-tracker


# Navigate to the backend folder
cd backend

# (Optional but recommended) Create a virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt



🏗️ What I Learned Building This
JWT Authentication on a FastAPI backend.

Password hashing with bcrypt and handling Windows compatibility issues.

SQLAlchemy ORM relationships (One-to-Many: User → Animals → HealthRecords).

Soft Delete patterns using deleted_at timestamps.

Pagination & Search using SQLAlchemy filter and offset/limit.

Asynchronous frontend state management with Vanilla JS (storing JWT, handling 401s).

🚧 Future Improvements (Roadmap)
CSV Export: Download herd data as a spreadsheet.

Email Notifications: Send alerts to the herder's email.

Dockerize: Create a Dockerfile for one-click deployment.

PostgreSQL: Swap SQLite for PostgreSQL in production.

Audit Log: Track who deleted/restored animals.



🤝 Contributing
This project was built as a final-year portfolio piece. Contributions are welcome! Please open an issue first to discuss what you would like to change.


📄 License
This project is open-source and available under the MIT License.

🙏 Acknowledgments
Built with ❤️ for the Maasai community. Inspired by the need for simple, offline-capable tech solutions in remote pastoralist regions.




