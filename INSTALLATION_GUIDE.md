# SASO App — Installation & Setup Guide

This guide will walk you through installing and running the **SASO Records Management System** on your computer. No programming experience is required — just follow each step carefully.

---

## What Is This App?

The **SASO App** is a web-based system for managing student affairs, including:
- Student records and profiles
- Disciplinary cases (minor, moderate, major)
- Clearance requirements and counseling records
- Student activities and participation
- Reports and statistics dashboard

You access it through your web browser (like Chrome or Edge) — no installation of the app itself is needed after setup.

---

## Before You Begin — What You Need to Install

You need three free tools installed on your computer first. If you already have them, skip ahead.

### 1. Python 3.12 (or newer)

Python is the programming language the backend of this app runs on.

- Go to: https://www.python.org/downloads/
- Click the big yellow **"Download Python"** button
- Run the installer
- **IMPORTANT:** On the first screen of the installer, check the box that says **"Add Python to PATH"** before clicking Install

To confirm it's installed, open **Command Prompt** (search "cmd" in the Start menu) and type:
```
python --version
```
You should see something like `Python 3.12.x`.

---

### 2. Node.js (version 18 or newer)

Node.js is needed to run the frontend (the visual part) of the app.

- Go to: https://nodejs.org/
- Download the **LTS** version (the one labeled "Recommended For Most Users")
- Run the installer with all default settings

To confirm it's installed, open **Command Prompt** and type:
```
node --version
```
You should see something like `v20.x.x`.

---

### 3. Git

Git is used to download the project files.

- Go to: https://git-scm.com/downloads
- Download and install for your operating system
- Use all default settings during installation

To confirm it's installed, open **Command Prompt** and type:
```
git --version
```
You should see something like `git version 2.x.x`.

---

## Step-by-Step Installation

### Step 1 — Download the Project

Open **Command Prompt** or **Terminal** and navigate to where you want to save the project. For example, your Desktop:

```
cd Desktop
```

Then download (clone) the project:

```
git clone git@github.com:your-github-username/saso-app.git
```

This will create a folder called `saso-app`. Move into it:

```
cd saso-app
```

---

### Step 2 — Set Up the Backend (Python/Django)

The backend is the "brain" of the app that handles data and logic.

#### 2a. Create a virtual environment

A virtual environment keeps the app's Python packages separate from the rest of your computer.

```
python -m venv venv
```

#### 2b. Activate the virtual environment

**On Windows:**
```
venv\Scripts\activate
```

**On Mac/Linux:**
```
source venv/bin/activate
```

After activation, you will see `(venv)` at the beginning of your command prompt line. This means it's active.

#### 2c. Install Python packages

```
pip install -r requirements.txt
```

This will download and install all the required packages. It may take a few minutes.

#### 2d. Set up the environment file

The app needs a configuration file to run. Copy the example file:

**On Windows:**
```
copy .env.example .env
```

**On Mac/Linux:**
```
cp .env.example .env
```

You don't need to change anything in this file for local use.

#### 2e. Set up the database

This creates all the necessary database tables:

```
python manage.py migrate
```

#### 2f. Load sample data (optional but recommended)

This creates an admin account and fills the app with sample student data so you can explore it right away:

```
python manage.py shell < apps/seed.py
```

After this runs, a default admin account is created:
- **Username:** `admin`
- **Password:** `admin1234`

> **Important:** Change this password after your first login if this will be used in a real environment.

---

### Step 3 — Set Up the Frontend (React)

The frontend is the visual interface you see in the browser.

Open a **new** Command Prompt window (keep the first one open), navigate to the project's `frontend` folder:

```
cd Desktop\saso-app\frontend
```

Install the frontend packages:

```
npm install
```

This may take a few minutes.

---

## Running the App

You need **two** Command Prompt windows open at the same time — one for the backend, one for the frontend.

### Window 1 — Start the Backend

Make sure you're in the `saso-app` root folder with the virtual environment active (`(venv)` shown):

```
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

Leave this window open. **Do not close it.**

### Window 2 — Start the Frontend

Make sure you're in the `saso-app/frontend` folder:

```
npm run dev
```

You should see:
```
  VITE v6.x.x  ready in x ms

  ➜  Local:   http://localhost:5173/
```

Leave this window open. **Do not close it.**

---

## Opening the App

Open your web browser (Chrome, Edge, Firefox) and go to:

```
http://localhost:5173
```

You will see the SASO App login page. Use the admin account created earlier:

- **Username:** `admin`
- **Password:** `admin1234`

---

## Creating Additional Users

Once logged in as admin, you can create other user accounts through the app's user management section. There are three user roles:

| Role | Access |
|------|--------|
| Super Admin | Full access to everything |
| Admin | Manage students, cases, activities |
| Assistant | Limited read/write access |

---

## Stopping the App

To stop the app, go to each Command Prompt window and press:

```
Ctrl + C
```

Do this in both windows (frontend and backend).

---

## Starting Again Next Time

You do not need to reinstall everything. Just:

1. Open Command Prompt, go to the `saso-app` folder, activate the virtual environment, and run `python manage.py runserver`
2. Open another Command Prompt, go to `saso-app/frontend`, and run `npm run dev`
3. Open your browser and go to `http://localhost:5173`

---

## Troubleshooting

### "python is not recognized as a command"
Python was not added to PATH during installation. Uninstall Python and reinstall it, making sure to check **"Add Python to PATH"** on the first screen.

### "npm is not recognized as a command"
Node.js is not installed or not added to PATH. Reinstall Node.js from https://nodejs.org/.

### The browser shows a blank page or connection error
Make sure both Command Prompt windows are still running (backend on port 8000 and frontend on port 5173). If either was closed, restart it.

### "No module named..." error
The virtual environment may not be active. Run `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux) before running any Python commands.

### Port already in use
Another program is using port 8000 or 5173. Restart your computer and try again, or close the application using those ports.

---

## Need Help?

If you run into an issue not covered here, contact the system developer or submit an issue at:
https://github.com/your-github-username/saso-app/issues
