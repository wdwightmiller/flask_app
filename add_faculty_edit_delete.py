#!/usr/bin/env python3
"""
This script adds edit and delete routes for faculty to app.py
"""

# Read the current app.py
with open('app.py', 'r') as f:
    lines = f.readlines()

# New routes to add
new_routes = '''
@app.route('/faculty/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    
    if request.method == 'POST':
        faculty.name = request.form.get('name')
        faculty.phone_number = request.form.get('phone_number')
        faculty.email = request.form.get('email')
        faculty.active = request.form.get('active') == 'on'
        
        db.session.commit()
        flash(f'Faculty member {faculty.name} updated successfully!', 'success')
        return redirect(url_for('faculty_list'))
    
    return render_template('edit_faculty.html', faculty=faculty)


@app.route('/faculty/delete/<int:id>')
@login_required
def delete_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    faculty.active = False
    db.session.commit()
    
    flash(f'Faculty member {faculty.name} deactivated', 'success')
    return redirect(url_for('faculty_list'))


'''

# Find the line after add_faculty route and insert new routes
found = False
output_lines = []

for i, line in enumerate(lines):
    output_lines.append(line)
    
    # Look for the end of add_faculty function
    if "return render_template('add_faculty.html')" in line and not found:
        # Check if routes already exist
        content = ''.join(lines)
        if 'def edit_faculty' not in content:
            output_lines.append(new_routes)
            found = True
            print("✅ Added faculty edit/delete routes!")

if found:
    # Write back
    with open('app.py', 'w') as f:
        f.writelines(output_lines)
    print("✅ Successfully updated app.py")
else:
    print("⚠️  Routes may already exist or couldn't find insertion point")

