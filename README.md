# Data Management System

A simple web app to add and view user data using Flask and SQLite.

## Features

- Add user data (name, email, age)
- View all data in a table
- Delete records
- Malaysia timezone support

## Quick Start

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   python app.py
   ```

3. **Open browser and go to:**
   ```
   http://localhost:5000
   ```

## How to Use

### Add Data
1. Click "Add New Data" 
2. Fill in name, email, and age
3. Click "Save Data"

### View Data
1. Click "View Database"
2. See all records in table
3. Delete records if needed

## Files

- `app.py` - Main Flask app
- `templates/` - HTML pages
- `data.db` - SQLite database (auto-created)
- `requirements.txt` - Python packages needed

## Database

Simple `users` table with:
- id (auto-increment)
- name
- email  
- age
- created_at (timestamp)

---

Made with Flask and SQLite

