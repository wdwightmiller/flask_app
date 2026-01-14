# Enhanced Fellowship Evaluation System - Summary of Changes

## Overview
The system has been significantly enhanced to support **multiple survey types**, **2-week rotation blocks**, and **automated Friday scheduling**.

---

## Major New Features

### 1. Multiple Survey Management
**What It Does:** Allows you to create and manage different types of evaluations
- Self evaluations
- Peer evaluations  
- Faculty evaluations
- Rotation evaluations
- Any custom evaluation types

**Why It Matters:** 
- No longer limited to a single Qualtrics link
- Each evaluation type has its own survey
- Fellows can receive different evaluations based on their needs

**How to Use:**
- Navigate to "Surveys" in the sidebar
- Add as many survey types as needed
- Each survey has its own Qualtrics link

---

### 2. Rotation Blocks
**What It Does:** Organizes evaluations into weekly periods
- Create 7-day blocks (typically Monday-Sunday)
- Each block represents one week with one Friday
- Each block can have different fellows and surveys assigned
- Bulk creation tool to set up many weeks at once

**Why It Matters:**
- Matches your actual weekly rotation schedule
- Different rotations/assignments each week
- Easy to plan an entire semester in minutes
- Maximum flexibility

**How to Use:**
- Navigate to "Rotation Blocks"
- Use "Bulk Create Weeks" to create multiple weeks at once
- Or create individual blocks one at a time
- Name them descriptively (e.g., "Week 1 - Jan 6-12, 2025")

---

### 3. Flexible Assignment System
**What It Does:** Links fellows to specific surveys for specific rotation blocks
- Assign different surveys to different fellows
- Bulk assign multiple fellows to multiple surveys
- Each assignment tracked independently

**Why It Matters:**
- Different fellows can get different evaluations during the same period
- Easy to set up complex evaluation schedules
- Prevents sending wrong surveys to wrong people

**How to Use:**
- Go to a rotation block → click "Assignments"
- Select fellows and surveys
- Click "Add Selected" for bulk operations

---

### 4. Friday Automation
**What It Does:** Automatically determines what to send each Friday
- Finds all active rotation blocks
- Gets assignments for those blocks
- Sends appropriate surveys to each fellow
- Tracks what was sent to prevent duplicates

**Why It Matters:**
- No more manual selection each week
- Prevents forgetting to send evaluations
- Automatic duplicate prevention
- One-click sending

**How to Use:**
- Every Friday, go to "Send Friday Evaluations"
- Review the preview
- Click "Send All Evaluations"

---

## What Changed in the Code

### New Database Models
```python
- Survey: Stores different evaluation types
- RotationBlock: Represents 2-week periods  
- RotationAssignment: Links fellows to surveys for specific blocks
- Updated Evaluation model to track which survey was sent
```

### New Routes/Pages
```
/surveys - Manage survey types
/surveys/add - Create new survey
/surveys/edit/<id> - Edit survey

/rotation-blocks - View all blocks
/rotation-blocks/add - Create new block
/rotation-blocks/edit/<id> - Edit block

/assignments - View assignments overview
/assignments/block/<id> - Manage assignments for a block
/assignments/bulk-add - Add multiple assignments at once

/send-friday-evaluations - New Friday sending interface
```

### Updated Features
- Dashboard now shows active rotation blocks and Friday countdown
- Navigation menu reorganized with new sections
- Settings page updated to show survey count
- Tracking page shows which survey was sent

---

## Migration from Old System

If you were using the original version:

### What Stays the Same
- Fellows management (unchanged)
- Faculty management (unchanged)
- Tracking system (enhanced but compatible)
- Login/authentication (unchanged)
- Twilio integration (unchanged)

### What You Need to Do
1. **Create Surveys:** Add your evaluation types (even if just one)
2. **Create Rotation Blocks:** Set up your 2-week periods
3. **Make Assignments:** Link fellows to surveys for each block
4. **Change Workflow:** Use "Send Friday Evaluations" instead of "Send Evaluations"

### Database Migration
The new system requires running `flask init-db` which will create new tables. Your existing fellows and faculty will be preserved.

---

## Benefits Over Original System

| Aspect | Original | Enhanced |
|--------|----------|----------|
| **Survey Types** | Single link | Unlimited types |
| **Scheduling** | Manual each time | Rotation-based automation |
| **Flexibility** | One-size-fits-all | Customized per fellow/rotation |
| **Planning** | Week-by-week | Months in advance |
| **Duplicate Prevention** | None | Automatic tracking |
| **Workflow Complexity** | Simple but limited | Powerful and flexible |
| **Setup Time** | 5 minutes | 30 minutes initial |
| **Weekly Time** | 10 minutes | 2 minutes (just click) |

---

## Use Cases This System Handles

### ✅ Simple Program
- All fellows get same evaluation weekly
- Create one survey, one rotation block
- Assign all fellows to same survey

### ✅ Complex Program  
- Different fellows on different rotations
- Each rotation has unique evaluations
- Peer evaluations + self evaluations + faculty evaluations
- Different schedules overlapping

### ✅ Your Situation
- Fellows evaluate themselves, each other, and faculty
- Different rotations every 2 weeks
- Evaluations sent every Friday
- Multiple survey types needed

---

## Quick Start Checklist

Week 1-2: Setup Phase
- [ ] Run through initial setup (install, configure, create admin)
- [ ] Add all fellows to the system
- [ ] Create all survey types in Qualtrics
- [ ] Add surveys to the system with their links
- [ ] Create first rotation block (current 2 weeks)
- [ ] Assign fellows to appropriate surveys
- [ ] Test with one fellow (use Test SMS feature)

Week 3+: Operational Phase
- [ ] Thursday: Review next week's rotation block
- [ ] Friday morning: Go to "Send Friday Evaluations"
- [ ] Review preview, click send
- [ ] Check tracking to verify success
- [ ] Monitor Qualtrics for completions

Monthly Maintenance
- [ ] Create rotation blocks for next month
- [ ] Update assignments as fellows rotate
- [ ] Backup database
- [ ] Review and archive old data

---

## Files in This Package

```
flask_app/
├── app.py                          # Main application (UPDATED)
├── requirements.txt               # Dependencies (same)
├── .env.example                   # Configuration template (UPDATED)
├── .gitignore                     # Git ignore file (same)
├── FLASK_SETUP_GUIDE.md          # Original setup guide
├── UPDATED_SETUP_GUIDE.md        # NEW: Comprehensive guide for enhanced features
├── templates/
│   ├── base.html                  # Base template (UPDATED - new navigation)
│   ├── login.html                 # Login page (same)
│   ├── index.html                 # Dashboard (UPDATED - new stats)
│   ├── settings.html              # Settings (UPDATED)
│   ├── fellows.html               # Fellows list (same)
│   ├── add_fellow.html           # Add fellow (same)
│   ├── edit_fellow.html          # Edit fellow (same)
│   ├── faculty.html               # Faculty list (same)
│   ├── add_faculty.html          # Add faculty (same)
│   ├── tracking.html              # Tracking (same)
│   ├── surveys.html               # NEW: Survey management
│   ├── add_survey.html           # NEW: Add survey
│   ├── edit_survey.html          # NEW: Edit survey
│   ├── rotation_blocks.html      # NEW: Rotation blocks list
│   ├── add_rotation_block.html   # NEW: Add rotation block
│   ├── edit_rotation_block.html  # NEW: Edit rotation block
│   ├── block_assignments.html    # NEW: Manage assignments
│   └── send_friday_evaluations.html # NEW: Friday sending interface
```

---

## Technical Notes

### Database Schema
- Uses SQLite (no separate database server needed)
- Supports SQLAlchemy for potential PostgreSQL migration
- Foreign keys maintain referential integrity
- Unique constraints prevent duplicate assignments

### Performance
- Handles 100+ fellows easily
- Scales to thousands of evaluations
- Consider PostgreSQL for very large programs (50+ fellows, years of data)

### Security
- Password hashing with werkzeug
- Session-based authentication
- CSRF protection via Flask
- SQL injection protection via SQLAlchemy

### Deployment Options
- Local: Great for testing
- Render/Railway: Recommended for production
- PythonAnywhere: Good for small programs
- Self-hosted: Full control

---

## Support and Questions

### Common Questions

**Q: Can I still use this for simple weekly evaluations?**
A: Yes! Just create one survey type and one ongoing rotation block.

**Q: What if I don't use 2-week blocks?**
A: The system is flexible - you can create any length blocks, though 14 days is recommended.

**Q: Can I send evaluations on days other than Friday?**
A: Yes! The "Send Friday Evaluations" button works any day.

**Q: How do I handle fellows on vacation/leave?**
A: Just don't assign them to surveys during that rotation block.

**Q: Can fellows get evaluations mid-block?**
A: Yes, you can add assignments anytime and they'll be included in the next Friday send.

**Q: What if I need to change an assignment?**
A: Go to the block's assignments page, remove the old one, add the new one.

---

## Next Steps

1. **Read UPDATED_SETUP_GUIDE.md** - Comprehensive instructions
2. **Follow the setup** - Get the system running
3. **Create your surveys** - Add your evaluation types
4. **Plan your blocks** - Create 2-week rotation periods
5. **Make assignments** - Link fellows to surveys
6. **Test it** - Use Settings → Test SMS
7. **Go live** - Send your first Friday evaluation batch!

---

## Version History

- **v1.0** (Original): Single survey, manual selection, basic tracking
- **v2.0** (This version): Multiple surveys, rotation blocks, Friday automation

---

Good luck with your fellowship evaluations! This system will save you significant time while providing much better organization and tracking.
