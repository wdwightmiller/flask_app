#!/usr/bin/env python3
"""
This script updates faculty.html to add Edit and Delete buttons
"""

with open('faculty.html', 'r') as f:
    content = f.read()

# Check if already updated
if '<th>Actions</th>' in content:
    print("⚠️  faculty.html already has Actions column - skipping")
    exit()

# Add Actions column to header
content = content.replace(
    '                        <th>Added</th>\n                    </tr>',
    '                        <th>Added</th>\n                        <th>Actions</th>\n                    </tr>'
)

# Find and replace the table row
old_row = '''                        <td>{{ member.created_at.strftime('%Y-%m-%d') }}</td>
                    </tr>'''

new_row = '''                        <td>{{ member.created_at.strftime('%Y-%m-%d') }}</td>
                        <td>
                            <a href="{{ url_for('edit_faculty', id=member.id) }}" class="btn btn-sm btn-outline-primary">
                                <i class="bi bi-pencil"></i> Edit
                            </a>
                            {% if member.active %}
                            <a href="{{ url_for('delete_faculty', id=member.id) }}" class="btn btn-sm btn-outline-danger" 
                               onclick="return confirm('Deactivate {{ member.name }}?')">
                                <i class="bi bi-x-circle"></i> Deactivate
                            </a>
                            {% endif %}
                        </td>
                    </tr>'''

content = content.replace(old_row, new_row)

# Write back
with open('faculty.html', 'w') as f:
    f.write(content)

print("✅ Successfully updated faculty.html with Edit and Delete buttons!")

