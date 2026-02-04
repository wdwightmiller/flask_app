#!/usr/bin/env python3
"""
Updates the system to support faculty assignments
This modifies the database to track whether assignment is for fellow or faculty
"""

from app import app, db
from sqlalchemy import text

print("Updating database schema for faculty assignments...")

with app.app_context():
    # Add recipient_type column to rotation_assignment table
    try:
        with db.engine.connect() as conn:
            # Check if column already exists
            result = conn.execute(text("PRAGMA table_info(rotation_assignment)"))
            columns = [row[1] for row in result]
            
            if 'recipient_type' not in columns:
                # Add new columns
                conn.execute(text("ALTER TABLE rotation_assignment ADD COLUMN recipient_type VARCHAR(20) DEFAULT 'fellow'"))
                conn.execute(text("ALTER TABLE rotation_assignment ADD COLUMN faculty_id INTEGER"))
                conn.commit()
                
                # Update existing records to have recipient_type = 'fellow'
                conn.execute(text("UPDATE rotation_assignment SET recipient_type = 'fellow' WHERE recipient_type IS NULL"))
                conn.commit()
                
                print("✅ Successfully added recipient_type and faculty_id columns")
            else:
                print("✅ Columns already exist - skipping")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("You may need to reinitialize the database")

print("\nDone! The database is ready for faculty assignments.")
