#!/usr/bin/env python3
"""
Script 1: Update Database Model
Adds faculty_id, recipient_type, send_date, and sms_template fields
"""

print("=" * 60)
print("SCRIPT 1: Updating Database Models")
print("=" * 60)
print()

with open('app.py', 'r') as f:
    content = f.read()

changes = []

# 1. Add sms_template to Survey model
if 'sms_template = db.Column' not in content:
    old = 'survey_type = db.Column(db.String(50))'
    new = '''survey_type = db.Column(db.String(50))
    sms_template = db.Column(db.Text)  # Custom SMS message template'''
    
    if old in content:
        content = content.replace(old, new)
        changes.append("Added sms_template to Survey")

# 2. Make fellow_id nullable
old = "fellow_id = db.Column(db.Integer, db.ForeignKey('fellow.id'), nullable=False)"
new = "fellow_id = db.Column(db.Integer, db.ForeignKey('fellow.id'), nullable=True)"

if old in content:
    content = content.replace(old, new)
    changes.append("Made fellow_id nullable")

# 3. Add new fields to RotationAssignment
if 'faculty_id = db.Column' not in content:
    insert_after = "fellow_id = db.Column(db.Integer, db.ForeignKey('fellow.id'), nullable=True)"
    new_fields = """
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=True)
    recipient_type = db.Column(db.String(20), default='fellow')
    send_date = db.Column(db.Date)"""
    
    if insert_after in content:
        content = content.replace(insert_after, insert_after + new_fields)
        changes.append("Added faculty_id, recipient_type, send_date")

# 4. Add helper methods
if 'def get_recipient(self):' not in content:
    helper = '''
    
    def get_recipient(self):
        """Get the fellow or faculty member"""
        if self.recipient_type == 'faculty':
            return Faculty.query.get(self.faculty_id)
        return Fellow.query.get(self.fellow_id)
    
    def get_recipient_name(self):
        """Get recipient name"""
        recipient = self.get_recipient()
        return recipient.name if recipient else "Unknown"
'''
    
    insert_before = "class Evaluation(db.Model):"
    if insert_before in content:
        content = content.replace(insert_before, helper + "\n" + insert_before)
        changes.append("Added helper methods")

# Save
with open('app.py', 'w') as f:
    f.write(content)

print("Changes made:")
for change in changes:
    print(f"  ✅ {change}")

print()
print("✅ Script 1 complete!")
print()

