#!/usr/bin/env python3
"""
Database migration for Render
Run this AFTER deploying updated code
"""

import sqlite3
import sys

db_path = 'instance/fellowship_evals.db'

print("Migrating database for faculty assignments and SMS templates...")
print()

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Add columns to rotation_assignment
    cursor.execute("PRAGMA table_info(rotation_assignment)")
    ra_columns = [row[1] for row in cursor.fetchall()]
    
    if 'recipient_type' not in ra_columns:
        print("  Adding recipient_type column...")
        cursor.execute("ALTER TABLE rotation_assignment ADD COLUMN recipient_type VARCHAR(20) DEFAULT 'fellow'")
        cursor.execute("UPDATE rotation_assignment SET recipient_type = 'fellow' WHERE recipient_type IS NULL")
        conn.commit()
        print("  ✅ Added recipient_type")
    
    if 'faculty_id' not in ra_columns:
        print("  Adding faculty_id column...")
        cursor.execute("ALTER TABLE rotation_assignment ADD COLUMN faculty_id INTEGER")
        conn.commit()
        print("  ✅ Added faculty_id")
    
    if 'send_date' not in ra_columns:
        print("  Adding send_date column...")
        cursor.execute("ALTER TABLE rotation_assignment ADD COLUMN send_date DATE")
        conn.commit()
        print("  ✅ Added send_date")
    
    # 2. Add sms_template to survey
    cursor.execute("PRAGMA table_info(survey)")
    survey_columns = [row[1] for row in cursor.fetchall()]
    
    if 'sms_template' not in survey_columns:
        print("  Adding sms_template column to survey...")
        cursor.execute("ALTER TABLE survey ADD COLUMN sms_template TEXT")
        conn.commit()
        print("  ✅ Added sms_template")
    
    print()
    print("✅ Database migration complete!")
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
