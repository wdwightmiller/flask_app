#!/usr/bin/env python3
"""
Migrates database to support faculty assignments
Run this ONCE before deploying the new code
"""

import sqlite3
import os

db_path = 'instance/fellowship_evals.db'

if not os.path.exists(db_path):
    print("❌ Database not found. Make sure you're in the flask_app directory.")
    exit(1)

print("Migrating database for faculty assignments...")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(rotation_assignment)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'recipient_type' not in columns:
        print("Adding recipient_type column...")
        cursor.execute("ALTER TABLE rotation_assignment ADD COLUMN recipient_type VARCHAR(20) DEFAULT 'fellow'")
        
        print("Adding faculty_id column...")
        cursor.execute("ALTER TABLE rotation_assignment ADD COLUMN faculty_id INTEGER")
        
        print("Updating existing records...")
        cursor.execute("UPDATE rotation_assignment SET recipient_type = 'fellow' WHERE recipient_type IS NULL")
        
        conn.commit()
        print("✅ Database migration complete!")
    else:
        print("✅ Database already migrated - skipping")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error during migration: {e}")
    print("You may need to run this on the Render server instead")

print("\nNext step: Update code files and push to GitHub")
