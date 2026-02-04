#!/usr/bin/env python3
"""
Script 3: Update Survey Templates
Adds SMS template fields to survey forms
"""

print("=" * 60)
print("SCRIPT 3: Updating Survey Templates")
print("=" * 60)
print()

changes = []

# 1. Update add_survey.html
print("Updating add_survey.html...")
with open('templates/add_survey.html', 'r') as f:
    content = f.read()

if 'sms_template' not in content:
    # Find where to insert (after survey_link field, before description)
    old = '''                    </div>

                    <div class="mb-3">
                        <label for="description" class="form-label">Description (Optional)</label>'''
    
    new = '''                    </div>

                    <div class="mb-3">
                        <label for="sms_template" class="form-label">SMS Message Template (Optional)</label>
                        <textarea class="form-control" id="sms_template" name="sms_template" rows="3"
                                  placeholder="Hi {name}, please complete your {survey}: {link}"></textarea>
                        <small class="text-muted">
                            Variables: {name}, {survey}, {link}, {date}<br>
                            Leave blank for default: "Hi {name}, please complete your {survey}: {link}"
                        </small>
                    </div>

                    <div class="mb-3">
                        <label for="description" class="form-label">Description (Optional)</label>'''
    
    if old in content:
        content = content.replace(old, new)
        with open('templates/add_survey.html', 'w') as f:
            f.write(content)
        changes.append("Updated add_survey.html")
        print("  ✅ Added SMS template field")
    else:
        print("  ⚠️  Could not find insertion point")
else:
    print("  ℹ️  Already has SMS template field")

print()

# 2. Update edit_survey.html
print("Updating edit_survey.html...")
with open('templates/edit_survey.html', 'r') as f:
    content = f.read()

if 'sms_template' not in content:
    # Find where to insert
    old = '''                    </div>

                    <div class="mb-3">
                        <label for="description" class="form-label">Description (Optional)</label>
                        <textarea class="form-control" id="description" name="description" rows="3">{{ survey.description or '' }}</textarea>'''
    
    new = '''                    </div>

                    <div class="mb-3">
                        <label for="sms_template" class="form-label">SMS Message Template (Optional)</label>
                        <textarea class="form-control" id="sms_template" name="sms_template" rows="3"
                                  placeholder="Hi {name}, please complete your {survey}: {link}">{{ survey.sms_template or '' }}</textarea>
                        <small class="text-muted">
                            Variables: {name}, {survey}, {link}, {date}<br>
                            Leave blank for default: "Hi {name}, please complete your {survey}: {link}"
                        </small>
                    </div>

                    <div class="mb-3">
                        <label for="description" class="form-label">Description (Optional)</label>
                        <textarea class="form-control" id="description" name="description" rows="3">{{ survey.description or '' }}</textarea>'''
    
    if old in content:
        content = content.replace(old, new)
        with open('templates/edit_survey.html', 'w') as f:
            f.write(content)
        changes.append("Updated edit_survey.html")
        print("  ✅ Added SMS template field")
    else:
        print("  ⚠️  Could not find insertion point")
else:
    print("  ℹ️  Already has SMS template field")

print()
print("Changes made:")
for change in changes:
    print(f"  ✅ {change}")

print()
print("✅ Script 3 complete!")
print()
