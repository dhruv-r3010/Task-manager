# Mini Task Manager

A simple Flask based web application to manage tasks with separate **To Do** and **Completed** sections.  
The app includes inline editing, toast notifications, and a clean modern UI.

---

## Features

- Add new tasks
- Edit tasks inline
- Mark tasks as completed
- Delete completed tasks
- Toast notifications for user feedback
- Clean and responsive UI
- Lightweight setup, no database required

---

## Tech Stack

### Backend
- Python 3
- Flask

### Frontend
- HTML
- CSS
- Google Fonts
- JavaScript (for toast notifications)

### Testing
- Playwright (End to End testing)

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/dhruv-r3010/Task-manager.git
cd Task-manager
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Mac / Linux**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install flask
```

Optional best practice:

```bash
pip freeze > requirements.txt
```

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000/
```

You can now add, edit, complete, and delete tasks.

---

## Project Structure

```
Task-manager/
├── app.py
├── static/
│   ├── favicon.ico
│   └── testdino-logo.png
├── README.md
└── venv/
```

---

## Important Notes

- Tasks are stored in memory.
- Restarting the server resets all tasks.
- This project is intended for learning and demo purposes.
- For persistence, you can integrate SQLite or another database.

---

## License

This project is open source and available under the MIT License.
