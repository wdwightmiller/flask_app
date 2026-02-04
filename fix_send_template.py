#!/usr/bin/env python3
"""
Fixes send_friday_evaluations.html template
"""

with open('templates/send_friday_evaluations.html', 'r') as f:
    content = f.read()

changes = []

# Fix the message preview that still references item.fellow
old_msg = '''                        <td class="small text-muted">
                            "Hi {{ item.fellow.name }}, please complete your {{ item.survey.name }}:..."
                        </td>'''

new_msg = '''                        <td class="small text-muted">
                            {% if item.survey.sms_template %}
                            "{{ item.survey.sms_template[:60] }}..."
                            {% else %}
                            "Hi {{ item.recipient.name }}, please complete your {{ item.survey.name }}:..."
                            {% endif %}
                        </td>'''

if old_msg in content:
    content = content.replace(old_msg, new_msg)
    changes.append("Fixed message preview")
    print("✅ Fixed message preview to use recipient")
else:
    print("⚠️  Could not find old message preview")

# Also check for any other references to item.fellow that might have been missed
if 'item.fellow' in content:
    print("⚠️  WARNING: Still found 'item.fellow' in template - manual review needed")
    # Show where
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if 'item.fellow' in line:
            print(f"   Line {i}: {line.strip()}")
else:
    print("✅ No more references to 'item.fellow'")

# Write back
with open('templates/send_friday_evaluations.html', 'w') as f:
    f.write(content)

print()
if changes:
    print("Changes made:")
    for change in changes:
        print(f"  ✅ {change}")
    print()
    print("Now push to GitHub!")
else:
    print("No changes needed - might already be fixed")
