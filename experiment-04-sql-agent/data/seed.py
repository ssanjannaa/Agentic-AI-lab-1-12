"""
Database Seeder Script — Company Analytics Domain
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)

Populates data/company.db with synthetic corporate records across:
- departments (5 records)
- employees (20 records)
- projects (8 records)
- employee_projects (30 junction records)
"""

import os
import sqlite3

def init_db(db_path: str = "data/company.db"):
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

    # Remove existing db file for fresh deterministic seed
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable Foreign Key support in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Create Tables
    cursor.execute("""
    CREATE TABLE departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        code TEXT NOT NULL UNIQUE,
        location TEXT NOT NULL,
        budget REAL NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_code TEXT NOT NULL UNIQUE,
        department_id INTEGER NOT NULL,
        job_title TEXT NOT NULL,
        salary REAL NOT NULL,
        hire_date TEXT NOT NULL,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        department_id INTEGER NOT NULL,
        budget REAL NOT NULL,
        status TEXT NOT NULL, -- 'active' | 'completed' | 'on_hold'
        FOREIGN KEY (department_id) REFERENCES departments(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE employee_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        hours_allocated INTEGER NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        FOREIGN KEY (project_id) REFERENCES projects(id)
    );
    """)

    # 2. Seed Departments (5 departments)
    departments_data = [
        (1, "Engineering", "ENG", "Building A - Floor 4", 1500000.0),
        (2, "Data Science & AI", "DS", "Building B - Floor 2", 1200000.0),
        (3, "Product Management", "PM", "Building A - Floor 3", 800000.0),
        (4, "Cybersecurity Operations", "SEC", "Building C - Floor 5", 950000.0),
        (5, "Cloud Infrastructure", "CLOUD", "Building C - Floor 1", 1100000.0)
    ]
    cursor.executemany("INSERT INTO departments VALUES (?, ?, ?, ?, ?);", departments_data)

    # 3. Seed Employees (20 employees)
    employees_data = [
        # Engineering (dept_id=1)
        (1, "Alice Vance", "EMP-101", 1, "Principal Software Engineer", 145000.0, "2021-03-15"),
        (2, "Bob Miller", "EMP-102", 1, "Senior Backend Engineer", 125000.0, "2022-01-10"),
        (3, "Charlie Davis", "EMP-103", 1, "Frontend Lead", 118000.0, "2022-06-01"),
        (4, "Diana Prince", "EMP-104", 1, "Software Engineer", 95000.0, "2023-04-20"),

        # Data Science & AI (dept_id=2)
        (5, "Dr. Evan Wright", "EMP-201", 2, "Lead AI Research Scientist", 165000.0, "2020-11-01"),
        (6, "Fiona Gallagher", "EMP-202", 2, "Senior ML Engineer", 138000.0, "2021-08-15"),
        (7, "George Clark", "EMP-203", 2, "Data Engineer", 112000.0, "2022-09-10"),
        (8, "Hannah Abbott", "EMP-204", 2, "AI Ethics Analyst", 92000.0, "2023-02-01"),

        # Product Management (dept_id=3)
        (9, "Ian Malcolm", "EMP-301", 3, "VP of Product", 155000.0, "2019-05-12"),
        (10, "Julia Roberts", "EMP-302", 3, "Senior Product Manager", 128000.0, "2021-04-18"),
        (11, "Kevin Bacon", "EMP-303", 3, "Product Owner", 98000.0, "2022-11-15"),

        # Cybersecurity Operations (dept_id=4)
        (12, "Laura Croft", "EMP-401", 4, "Chief Information Security Officer", 160000.0, "2020-02-10"),
        (13, "Michael Scott", "EMP-402", 4, "Lead Security Architect", 135000.0, "2021-07-01"),
        (14, "Nina Williams", "EMP-403", 4, "SOC Incident Manager", 110000.0, "2022-03-22"),
        (15, "Oscar Martinez", "EMP-404", 4, "Penetration Tester", 102000.0, "2023-01-05"),

        # Cloud Infrastructure (dept_id=5)
        (16, "Peter Parker", "EMP-501", 5, "Principal DevOps Architect", 148000.0, "2020-09-15"),
        (17, "Quinn Fabray", "EMP-502", 5, "Senior Site Reliability Engineer", 130000.0, "2021-12-01"),
        (18, "Rachel Green", "EMP-503", 5, "Cloud Security Specialist", 115000.0, "2022-05-20"),
        (19, "Steve Rogers", "EMP-504", 5, "Systems Administrator", 88000.0, "2023-06-10"),
        (20, "Tony Stark", "EMP-505", 5, "Automation Engineer", 105000.0, "2023-08-01")
    ]
    cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?);", employees_data)

    # 4. Seed Projects (8 projects)
    projects_data = [
        (1, "Agentic AI Laboratory Suite", 2, 450000.0, "active"),
        (2, "Enterprise Zero-Trust Mesh", 4, 380000.0, "active"),
        (3, "Next-Gen Cloud Orchestration", 5, 520000.0, "active"),
        (4, "High-Throughput SQL Engine", 1, 310000.0, "active"),
        (5, "Customer Analytics Platform", 3, 220000.0, "completed"),
        (6, "SIEM Threat Intelligence Feed", 4, 290000.0, "completed"),
        (7, "Autonomous RAG Knowledge Hub", 2, 340000.0, "active"),
        (8, "Legacy Database Migration", 5, 180000.0, "completed")
    ]
    cursor.executemany("INSERT INTO projects VALUES (?, ?, ?, ?, ?);", projects_data)

    # 5. Seed Employee-Project Allocations (30 junction records)
    employee_projects_data = [
        # Project 1: Agentic AI Laboratory Suite (DS & AI)
        (1, 5, 1, 160),  # Dr. Evan Wright
        (2, 6, 1, 140),  # Fiona Gallagher
        (3, 7, 1, 120),  # George Clark
        (4, 1, 1, 80),   # Alice Vance (cross-dept engineering support)

        # Project 2: Enterprise Zero-Trust Mesh (Security)
        (5, 12, 2, 150), # Laura Croft
        (6, 13, 2, 160), # Michael Scott
        (7, 14, 2, 130), # Nina Williams
        (8, 18, 2, 90),  # Rachel Green (cross-dept cloud sec)

        # Project 3: Next-Gen Cloud Orchestration (Cloud Infra)
        (9, 16, 3, 170), # Peter Parker
        (10, 17, 3, 150), # Quinn Fabray
        (11, 19, 3, 110), # Steve Rogers
        (12, 20, 3, 100), # Tony Stark
        (13, 2, 3, 70),   # Bob Miller (cross-dept backend)

        # Project 4: High-Throughput SQL Engine (Engineering)
        (14, 1, 4, 120), # Alice Vance
        (15, 2, 4, 140), # Bob Miller
        (16, 3, 4, 150), # Charlie Davis
        (17, 4, 4, 110), # Diana Prince

        # Project 5: Customer Analytics Platform (PM)
        (18, 9, 5, 90),  # Ian Malcolm
        (19, 10, 5, 120), # Julia Roberts
        (20, 11, 5, 100), # Kevin Bacon
        (21, 7, 5, 60),   # George Clark

        # Project 6: SIEM Threat Intelligence Feed (Security)
        (22, 13, 6, 80), # Michael Scott
        (23, 14, 6, 100), # Nina Williams
        (24, 15, 6, 140), # Oscar Martinez

        # Project 7: Autonomous RAG Knowledge Hub (DS & AI)
        (25, 5, 7, 110), # Dr. Evan Wright
        (26, 6, 7, 130), # Fiona Gallagher
        (27, 8, 7, 150), # Hannah Abbott
        (28, 10, 7, 50),  # Julia Roberts

        # Project 8: Legacy Database Migration (Cloud)
        (29, 16, 8, 60), # Peter Parker
        (30, 19, 8, 90)  # Steve Rogers
    ]
    cursor.executemany("INSERT INTO employee_projects VALUES (?, ?, ?, ?);", employee_projects_data)

    conn.commit()
    conn.close()
    print(f"[OK] Successfully initialized and seeded company database at: {os.path.abspath(db_path)}")

if __name__ == "__main__":
    db_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "company.db")
    init_db(db_file)
