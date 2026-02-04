#!/usr/bin/env python3
"""
Applies faculty assignment updates to app.py
"""

with open('app.py', 'r') as f:
    content = f.read()

# Check if already updated
if 'recipient_type' in content and 'add_assignment_faculty' in content:
    print("✅ app.py already updated")
    exit()

print("Updating app.py...")

# 1. Update RotationAssignment model - change fellow_id to nullable and add new fields
old_line1 = "    fellow_id = db.Column(db.Integer, db.ForeignKey('fellow.id'), nullable=False)"
new_line1 = "    fellow_id = db.Column(db.Integer, db.ForeignKey('fellow.id'), nullable=True)"

if old_line1 in content:
    content = content.replace(old_line1, new_line1)
    print("  ✅ Made fellow_id nullable")

# 2. Add new fields after fellow_id
insert_after = "    fellow_id = db.Column(db.Integer, db.ForeignKey('fellow.id'), nullable=True)"
new_fields = """    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=True)
    recipient_type = db.Column(db.String(20), default='fellow')  # 'fellow' or 'faculty'"""

if insert_after in content and 'faculty_id = db.Column' not in content:
    content = content.replace(insert_after, insert_after + "\n" + new_fields)
    print("  ✅ Added faculty_id and recipient_type fields")

# 3. Add get_recipient method to RotationAssignment class
get_recipient_method = '''
    
    def get_recipient(self):
        """Get the fellow or faculty member for this assignment"""
        if self.recipient_type == 'faculty':
            return Faculty.query.get(self.faculty_id)
        else:
            return Fellow.query.get(self.fellow_id)
    
    def get_recipient_name(self):
        """Get the name of the recipient"""
        recipient = self.get_recipient()
        return recipient.name if recipient else "Unknown"'''

# Find where to insert (before the Evaluation model)
insert_before = "class Evaluation(db.Model):"
if insert_before in content and 'def get_recipient(self):' not in content:
    content = content.replace(insert_before, get_recipient_method + "\n\n" + insert_before)
    print("  ✅ Added get_recipient methods")

# 4. Update add_assignment route to handle both fellows and faculty
old_add = '''@app.route('/assignments/add', methods=['POST'])
@login_required
def add_assignment():
    fellow_id = request.form.get('fellow_id')
    survey_id = request.form.get('survey_id')
    rotation_block_id = request.form.get('rotation_block_id')
    notes = request.form.get('notes')
    
    # Check if assignment already exists
    existing = RotationAssignment.query.filter_by(
        fellow_id=fellow_id,
        survey_id=survey_id,
        rotation_block_id=rotation_block_id
    ).first()
    
    if existing:
        flash('This assignment already exists!', 'warning')
    else:
        assignment = RotationAssignment(
            fellow_id=fellow_id,
            survey_id=survey_id,
            rotation_block_id=rotation_block_id,
            notes=notes
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Assignment added successfully!', 'success')
    
    return redirect(url_for('view_block_assignments', block_id=rotation_block_id))'''

new_add = '''@app.route('/assignments/add', methods=['POST'])
@login_required
def add_assignment():
    fellow_id = request.form.get('fellow_id')
    faculty_id = request.form.get('faculty_id')
    survey_id = request.form.get('survey_id')
    rotation_block_id = request.form.get('rotation_block_id')
    notes = request.form.get('notes')
    
    # Determine recipient type
    if faculty_id:
        recipient_type = 'faculty'
        recipient_id = faculty_id
        check_field = 'faculty_id'
    else:
        recipient_type = 'fellow'
        recipient_id = fellow_id
        check_field = 'fellow_id'
    
    # Check if assignment already exists
    existing = RotationAssignment.query.filter_by(
        **{check_field: recipient_id},
        survey_id=survey_id,
        rotation_block_id=rotation_block_id,
        recipient_type=recipient_type
    ).first()
    
    if existing:
        flash('This assignment already exists!', 'warning')
    else:
        assignment = RotationAssignment(
            **{check_field: recipient_id},
            survey_id=survey_id,
            rotation_block_id=rotation_block_id,
            recipient_type=recipient_type,
            notes=notes
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Assignment added successfully!', 'success')
    
    return redirect(url_for('view_block_assignments', block_id=rotation_block_id))'''

if old_add in content:
    content = content.replace(old_add, new_add)
    print("  ✅ Updated add_assignment route")

# 5. Update bulk_add_assignments to support both
old_bulk = '''@app.route('/assignments/bulk-add/<int:block_id>', methods=['POST'])
@login_required
def bulk_add_assignments(block_id):
    """Add multiple assignments at once"""
    fellow_ids = request.form.getlist('fellow_ids')
    survey_ids = request.form.getlist('survey_ids')
    
    added_count = 0
    skipped_count = 0
    
    for fellow_id in fellow_ids:
        for survey_id in survey_ids:
            # Check if assignment already exists
            existing = RotationAssignment.query.filter_by(
                fellow_id=fellow_id,
                survey_id=survey_id,
                rotation_block_id=block_id
            ).first()
            
            if not existing:
                assignment = RotationAssignment(
                    fellow_id=fellow_id,
                    survey_id=survey_id,
                    rotation_block_id=block_id
                )
                db.session.add(assignment)
                added_count += 1
            else:
                skipped_count += 1
    
    db.session.commit()
    
    if skipped_count > 0:
        flash(f'Added {added_count} assignments, skipped {skipped_count} duplicates', 'success')
    else:
        flash(f'Added {added_count} assignments successfully!', 'success')
    
    return redirect(url_for('view_block_assignments', block_id=block_id))'''

new_bulk = '''@app.route('/assignments/bulk-add/<int:block_id>', methods=['POST'])
@login_required
def bulk_add_assignments(block_id):
    """Add multiple assignments at once for fellows OR faculty"""
    fellow_ids = request.form.getlist('fellow_ids')
    faculty_ids = request.form.getlist('faculty_ids')
    survey_ids = request.form.getlist('survey_ids')
    
    added_count = 0
    skipped_count = 0
    
    # Add fellow assignments
    for fellow_id in fellow_ids:
        for survey_id in survey_ids:
            existing = RotationAssignment.query.filter_by(
                fellow_id=fellow_id,
                survey_id=survey_id,
                rotation_block_id=block_id,
                recipient_type='fellow'
            ).first()
            
            if not existing:
                assignment = RotationAssignment(
                    fellow_id=fellow_id,
                    survey_id=survey_id,
                    rotation_block_id=block_id,
                    recipient_type='fellow'
                )
                db.session.add(assignment)
                added_count += 1
            else:
                skipped_count += 1
    
    # Add faculty assignments
    for faculty_id in faculty_ids:
        for survey_id in survey_ids:
            existing = RotationAssignment.query.filter_by(
                faculty_id=faculty_id,
                survey_id=survey_id,
                rotation_block_id=block_id,
                recipient_type='faculty'
            ).first()
            
            if not existing:
                assignment = RotationAssignment(
                    faculty_id=faculty_id,
                    survey_id=survey_id,
                    rotation_block_id=block_id,
                    recipient_type='faculty'
                )
                db.session.add(assignment)
                added_count += 1
            else:
                skipped_count += 1
    
    db.session.commit()
    
    if skipped_count > 0:
        flash(f'Added {added_count} assignments, skipped {skipped_count} duplicates', 'success')
    else:
        flash(f'Added {added_count} assignments successfully!', 'success')
    
    return redirect(url_for('view_block_assignments', block_id=block_id))'''

if old_bulk in content:
    content = content.replace(old_bulk, new_bulk)
    print("  ✅ Updated bulk_add_assignments route")

# 6. Update send_friday_evaluations - the sending part
old_send_loop = '''            for assignment in assignments:
                # Check if already sent today
                if assignment.last_sent == today:
                    already_sent_count += 1
                    continue
                
                fellow = Fellow.query.get(assignment.fellow_id)
                survey = Survey.query.get(assignment.survey_id)
                
                if fellow and survey and fellow.active and survey.active:
                    success, result = send_evaluation_sms(fellow, survey, assignment)
                    if success:
                        success_count += 1
                    else:
                        failed_count += 1'''

new_send_loop = '''            for assignment in assignments:
                # Check if already sent today
                if assignment.last_sent == today:
                    already_sent_count += 1
                    continue
                
                recipient = assignment.get_recipient()
                survey = Survey.query.get(assignment.survey_id)
                
                if recipient and survey and recipient.active and survey.active:
                    success, result = send_evaluation_sms(recipient, survey, assignment)
                    if success:
                        success_count += 1
                    else:
                        failed_count += 1'''

if old_send_loop in content:
    content = content.replace(old_send_loop, new_send_loop)
    print("  ✅ Updated Friday sending loop")

# 7. Update send_friday_evaluations - the preview part
old_preview = '''        for assignment in assignments:
            if assignment.last_sent != today:  # Not already sent today
                preview_assignments.append({
                    'assignment': assignment,
                    'fellow': Fellow.query.get(assignment.fellow_id),
                    'survey': Survey.query.get(assignment.survey_id),
                    'block': block
                })'''

new_preview = '''        for assignment in assignments:
            if assignment.last_sent != today:  # Not already sent today
                recipient = assignment.get_recipient()
                preview_assignments.append({
                    'assignment': assignment,
                    'recipient': recipient,
                    'recipient_type': assignment.recipient_type,
                    'survey': Survey.query.get(assignment.survey_id),
                    'block': block
                })'''

if old_preview in content:
    content = content.replace(old_preview, new_preview)
    print("  ✅ Updated Friday preview")

# Write updated content
with open('app.py', 'w') as f:
    f.write(content)

print("\n✅ Successfully updated app.py!")
print("Next: Update templates")
