import sqlite3
import random
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('campus.db')
    cursor = conn.cursor()
    
    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # 2. Complaints Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT UNIQUE NOT NULL,
            student_name TEXT NOT NULL,
            department TEXT NOT NULL,
            building TEXT NOT NULL,
            room_no TEXT NOT NULL,
            category TEXT NOT NULL,
            problem TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            date TEXT NOT NULL
        )
    ''')
    
    # 3. Maintenance Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT NOT NULL,
            staff_name TEXT NOT NULL,
            repair_date TEXT NOT NULL,
            cost REAL NOT NULL,
            remarks TEXT,
            FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    
    # Seed default user accounts if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('student', 'student123', 'student')")
        conn.commit()

    # Seed sample complaints if empty
    cursor.execute("SELECT COUNT(*) FROM complaints")
    if cursor.fetchone()[0] == 0:
        seed_sample_data(conn)
        
    conn.close()

def seed_sample_data(conn):
    cursor = conn.cursor()
    names = ["Rahul Sharma", "Ankita Roy", "Priya Singh", "Aman Verma", "Sneha Patel", "Rohan Mehta"]
    departments = ["BCA", "CSE", "ECE", "Mechanical", "Civil", "MBA"]
    buildings = ["Block A", "Block B", "Block C", "Computer Lab", "Library", "Hostel Block"]
    categories = ["Electrical", "Furniture", "Plumbing", "IT", "Internet", "Cleaning", "AC/Cooling", "Other"]
    priorities = ["Low", "Medium", "High"]
    statuses = ["Pending", "In Progress", "Resolved"]
    
    problems_map = {
        "Electrical": "Fan making loud noise and not reaching full speed",
        "Furniture": "Broken desk leg causing instability",
        "Plumbing": "Continuous water leakage from tap",
        "IT": "Projector HDMI port damaged",
        "Internet": "Wi-Fi connection keeps dropping",
        "Cleaning": "Classroom needs deep cleaning",
        "AC/Cooling": "AC is blowing warm air",
        "Other": "Door lock jammed"
    }

    start_date = datetime(2026, 3, 1)
    
    for i in range(1, 49):
        cid = f"CMP{i:03d}"
        s_name = random.choice(names)
        dept = random.choice(departments)
        bldg = random.choice(buildings)
        room = str(random.randint(101, 404))
        cat = random.choice(categories)
        prob = problems_map[cat]
        prio = random.choice(priorities)
        stat = random.choices(statuses, weights=[35, 25, 40])[0]
        
        random_days = random.randint(0, 175)
        c_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
        
        cursor.execute('''
            INSERT INTO complaints (complaint_id, student_name, department, building, room_no, category, problem, priority, status, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (cid, s_name, dept, bldg, room, cat, prob, prio, stat, c_date))
        
        if stat == "Resolved":
            r_days = random.randint(1, 5)
            r_date = (datetime.strptime(c_date, "%Y-%m-%d") + timedelta(days=r_days)).strftime("%Y-%m-%d")
            cost = float(random.choice([250, 500, 800, 1200, 2500, 8000]))
            cursor.execute('''
                INSERT INTO maintenance (complaint_id, staff_name, repair_date, cost, remarks)
                VALUES (?, ?, ?, ?, ?)
            ''', (cid, "Amit Technician", r_date, cost, "Issue diagnosed and resolved."))
            
    conn.commit()

if __name__ == '__main__':
    init_db()
    print("Database schema and users initialized successfully.")