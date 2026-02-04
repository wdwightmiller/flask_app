#!/usr/bin/env python3
"""
Script 4: Update UI Templates
Updates assignment page, sending page, and navigation
"""

print("=" * 60)
print("SCRIPT 4: Updating UI Templates")
print("=" * 60)
print()

changes = []

# 1. Update base.html - rename navigation
print("Updating navigation...")
with open('templates/base.html', 'r') as f:
    content = f.read()

if 'Send Friday Evaluations' in content:
    content = content.replace('Send Friday Evaluations', 'Send Evaluations Now')
    with open('templates/base.html', 'w') as f:
        f.write(content)
    changes.append("Updated navigation to 'Send Evaluations Now'")
    print("  ✅ Renamed to 'Send Evaluations Now'")
else:
    print("  ℹ️  Already renamed")

print()

# 2. Update send_friday_evaluations.html
print("Updating send_friday_evaluations.html...")
with open('templates/send_friday_evaluations.html', 'r') as f:
    content = f.read()

# Change title
if 'Send Friday Evaluations' in content:
    content = content.replace(
        '<i class="bi bi-calendar-check"></i> Send Friday Evaluations',
        '<i class="bi bi-send"></i> Send Evaluations Now'
    )
    changes.append("Updated send page title")
    print("  ✅ Updated title")

# Update the table to show recipient type
if 'recipient_type' not in content:
    old_row = '''                    {% for item in preview_assignments[:20] %}
                    <tr>
                        <td><strong>{{ item.fellow.name }}</strong></td>
                        <td class="small">{{ item.fellow.phone_number }}</td>'''
    
    new_row = '''                    {% for item in preview_assignments[:20] %}
                    <tr>
                        <td>
                            <strong>{{ item.recipient.name }}</strong>
                            {% if item.recipient_type == 'faculty' %}
                            <span class="badge bg-info">Faculty</span>
                            {% else %}
                            <span class="badge bg-primary">Fellow</span>
                            {% endif %}
                        </td>
                        <td class="small">{{ item.recipient.phone_number }}</td>'''
    
    if old_row in content:
        content = content.replace(old_row, new_row)
        changes.append("Updated preview table")
        print("  ✅ Added recipient type badges")

with open('templates/send_friday_evaluations.html', 'w') as f:
    f.write(content)

print()

# 3. Update block_assignments.html - BIG UPDATE
print("Updating block_assignments.html...")
with open('templates/block_assignments.html', 'r') as f:
    content = f.read()

# Add faculty selection if not present
if 'faculty_ids' not in content:
    # Change from 2 columns to 3 columns (fellows, faculty, surveys)
    old_section = '''            <div class="row">
                <div class="col-md-5">
                    <label class="form-label"><strong>Select Fellows:</strong></label>'''
    
    new_section = '''            <div class="row">
                <div class="col-md-4">
                    <label class="form-label"><strong>Select Fellows:</strong></label>'''
    
    if old_section in content:
        content = content.replace(old_section, new_section)
    
    # Add faculty column after fellows
    old_surveys = '''                </div>

                <div class="col-md-5">
                    <label class="form-label"><strong>Select Surveys:</strong></label>'''
    
    new_faculty_and_surveys = '''                </div>

                <div class="col-md-4">
                    <label class="form-label"><strong>Select Faculty:</strong></label>
                    <div class="border rounded p-2" style="max-height: 200px; overflow-y: auto;">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="selectAllFaculty">
                            <label class="form-check-label fw-bold" for="selectAllFaculty">
                                Select All Faculty
                            </label>
                        </div>
                        <hr class="my-2">
                        {% for member in faculty %}
                        <div class="form-check">
                            <input class="form-check-input faculty-checkbox" type="checkbox" name="faculty_ids" 
                                   value="{{ member.id }}" id="faculty{{ member.id }}">
                            <label class="form-check-label" for="faculty{{ member.id }}">
                                {{ member.name }}
                            </label>
                        </div>
                        {% endfor %}
                    </div>
                </div>

                <div class="col-md-4">
                    <label class="form-label"><strong>Select Surveys:</strong></label>'''
    
    if old_surveys in content:
        content = content.replace(old_surveys, new_faculty_and_surveys)
        changes.append("Added faculty selection")
        print("  ✅ Added faculty selection column")
    
    # Add faculty select-all script
    old_script = '''// Select All Fellows
document.getElementById('selectAllFellows').addEventListener('change', function() {
    const checkboxes = document.querySelectorAll('.fellow-checkbox');
    checkboxes.forEach(cb => cb.checked = this.checked);
});

// Select All Surveys'''
    
    new_script = '''// Select All Fellows
document.getElementById('selectAllFellows').addEventListener('change', function() {
    const checkboxes = document.querySelectorAll('.fellow-checkbox');
    checkboxes.forEach(cb => cb.checked = this.checked);
});

// Select All Faculty
document.getElementById('selectAllFaculty').addEventListener('change', function() {
    const checkboxes = document.querySelectorAll('.faculty-checkbox');
    checkboxes.forEach(cb => cb.checked = this.checked);
});

// Select All Surveys'''
    
    if old_script in content:
        content = content.replace(old_script, new_script)

# Add send_date field
if 'send_date' not in content:
    # Find the submit button and add date field before it
    old_button = '''                <div class="col-md-2 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="bi bi-check2-all"></i> Add Selected
                    </button>
                </div>
            </div>'''
    
    new_with_date = '''                <div class="col-md-12 mt-3">
                    <label class="form-label"><strong>Optional: Schedule Send Date</strong></label>
                    <input type="date" class="form-control" name="send_date" id="send_date" style="max-width: 300px;">
                    <small class="text-muted">Leave blank to send on Fridays. Set specific date for holidays.</small>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-md-12">
                    <button type="submit" class="btn btn-primary btn-lg">
                        <i class="bi bi-check2-all"></i> Add Selected Assignments
                    </button>
                </div>
            </div>'''
    
    if old_button in content:
        content = content.replace(old_button, new_with_date)
        changes.append("Added date scheduling")
        print("  ✅ Added date scheduling field")

# Update assignments table to show recipient type
if 'recipient_type' not in content:
    old_header = '''                <thead>
                    <tr>
                        <th>Fellow</th>
                        <th>Survey</th>'''
    
    new_header = '''                <thead>
                    <tr>
                        <th>Recipient</th>
                        <th>Type</th>
                        <th>Survey</th>'''
    
    if old_header in content:
        content = content.replace(old_header, new_header)
    
    old_row = '''                    {% for assignment in assignments %}
                    <tr>
                        <td><strong>{{ assignment.fellow.name }}</strong></td>
                        <td>{{ assignment.survey.name }}</td>'''
    
    new_row = '''                    {% for assignment in assignments %}
                    <tr>
                        <td><strong>{{ assignment.get_recipient_name() }}</strong></td>
                        <td>
                            {% if assignment.recipient_type == 'faculty' %}
                            <span class="badge bg-info">Faculty</span>
                            {% else %}
                            <span class="badge bg-primary">Fellow</span>
                            {% endif %}
                        </td>
                        <td>{{ assignment.survey.name }}</td>'''
    
    if old_row in content:
        content = content.replace(old_row, new_row)
        changes.append("Updated assignments table")
        print("  ✅ Added recipient type to table")

# Add scheduled date column
if 'Scheduled' not in content:
    old_sent = '''                        <th>Last Sent</th>
                        <th>Actions</th>'''
    
    new_sent = '''                        <th>Last Sent</th>
                        <th>Scheduled</th>
                        <th>Actions</th>'''
    
    if old_sent in content:
        content = content.replace(old_sent, new_sent)
    
    old_sent_cell = '''                        <td>
                            {% if assignment.last_sent %}
                            {{ assignment.last_sent.strftime('%b %d, %Y') }}
                            {% else %}
                            <span class="text-muted">Not sent yet</span>
                            {% endif %}
                        </td>
                        <td>'''
    
    new_sent_cell = '''                        <td>
                            {% if assignment.last_sent %}
                            {{ assignment.last_sent.strftime('%b %d, %Y') }}
                            {% else %}
                            <span class="text-muted">Not sent yet</span>
                            {% endif %}
                        </td>
                        <td>
                            {% if assignment.send_date %}
                            <span class="badge bg-warning">{{ assignment.send_date.strftime('%b %d') }}</span>
                            {% else %}
                            <span class="badge bg-secondary">Fridays</span>
                            {% endif %}
                        </td>
                        <td>'''
    
    if old_sent_cell in content:
        content = content.replace(old_sent_cell, new_sent_cell)
        changes.append("Added scheduled date column")
        print("  ✅ Added scheduled date column")

with open('templates/block_assignments.html', 'w') as f:
    f.write(content)

print()

# 4. Update index.html
print("Updating index.html...")
with open('templates/index.html', 'r') as f:
    content = f.read()

if 'Send Friday Evaluations' in content:
    content = content.replace('Send Friday Evaluations', 'Send Evaluations Now')
    with open('templates/index.html', 'w') as f:
        f.write(content)
    changes.append("Updated dashboard button")
    print("  ✅ Updated dashboard button")
else:
    print("  ℹ️  Already updated")

print()

# 5. Create migration script
print("Creating database migration script...")
migration = '''#!/usr/bin/env python3
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
'''

with open('migrate_database.py', 'w') as f:
    f.write(migration)

changes.append("Created migration script")
print("  ✅ Created migrate_database.py")

print()
print("=" * 60)
print("ALL SCRIPTS COMPLETE!")
print("=" * 60)
print()
print("Summary of all changes:")
for change in changes:
    print(f"  ✅ {change}")

print()
print("Next steps:")
print("  1. Push to GitHub")
print("  2. After Render redeploys, run: python3 migrate_database.py")
print("  3. Reinitialize data (flask init-db, create admins, import data)")
print()
