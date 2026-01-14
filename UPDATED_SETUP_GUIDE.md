# Fellowship Evaluation System - UPDATED Setup Guide
## Enhanced Version with Multiple Surveys, Rotation Blocks, and Friday Scheduling

---

## What's New in This Version

✅ **Multiple Survey Types** - Support for self, peer, faculty, and rotation evaluations
✅ **Rotation Blocks** - Manage 2-week rotation periods
✅ **Flexible Assignments** - Assign different surveys to different fellows per block
✅ **Friday Automation** - Automatically send evaluations every Friday
✅ **Advanced Tracking** - Know exactly which survey was sent when
✅ **Duplicate Prevention** - Never send the same evaluation twice in one day

---

## Key Concepts

### 1. Surveys
Surveys are the different types of evaluations you want fellows to complete:
- **Self Evaluations** - Fellows evaluate themselves
- **Peer Evaluations** - Fellows evaluate each other
- **Faculty Evaluations** - Fellows evaluate attending physicians
- **Rotation Evaluations** - Fellows evaluate their rotation experience

Each survey type has its own Qualtrics link.

### 2. Rotation Blocks
A rotation block is a 2-week period (14 days) during which specific evaluations are assigned. For example:
- **ICU Block 1**: Jan 6-19, 2025
- **Outpatient Block 1**: Jan 20-Feb 2, 2025

Each block can have different fellows and different surveys assigned.

### 3. Assignments
Assignments link fellows to surveys for a specific rotation block. For example:
- **John Smith** gets **Self Evaluation** + **Peer Evaluation** during **ICU Block 1**
- **Sarah Johnson** gets **Faculty Evaluation** + **Rotation Evaluation** during **ICU Block 1**

### 4. Friday Sending
Every Friday, the system:
1. Finds all active rotation blocks (blocks that include today's date)
2. Gets all assignments for those blocks
3. Sends each fellow their assigned survey links via text
4. Tracks what was sent to prevent duplicates

---

## Part 1: Initial Setup (Same as Before)

Follow steps 1-5 from the original FLASK_SETUP_GUIDE.md:

1. Install Python
2. Create project folder and extract files
3. Create virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `.env` file with Twilio credentials
6. Initialize database: `flask init-db`
7. Create admin user: `flask create-admin`
8. Run application: `python app.py`

---

## Part 2: Setting Up Your Evaluation System

### Step 1: Add Fellows
1. Go to **Fellows** → **Add Fellow**
2. Enter each fellow's:
   - Name
   - Phone number
   - Email (optional)
3. Add all your fellows

**Example:**
- John Smith - (555) 123-4567
- Sarah Johnson - (555) 234-5678
- Michael Lee - (555) 345-6789

### Step 2: Create Your Surveys
1. Go to **Surveys** → **Add Survey**
2. For each evaluation type you need, create a survey:

**Example Setup:**

**Survey 1: Fellow Self-Evaluation**
- Name: "Fellow Self-Evaluation"
- Type: Self
- Link: https://yourschool.qualtrics.com/jfe/form/SV_self123
- Description: "Fellows assess their own performance"

**Survey 2: Peer Evaluation**
- Name: "Peer Evaluation"
- Type: Peer
- Link: https://yourschool.qualtrics.com/jfe/form/SV_peer456
- Description: "Fellows evaluate their peers"

**Survey 3: Attending Evaluation**
- Name: "Attending Evaluation"
- Type: Faculty
- Link: https://yourschool.qualtrics.com/jfe/form/SV_faculty789
- Description: "Fellows evaluate attending physicians"

**Survey 4: ICU Rotation Evaluation**
- Name: "ICU Rotation Evaluation"
- Type: Rotation
- Link: https://yourschool.qualtrics.com/jfe/form/SV_icu321
- Description: "End-of-rotation feedback for ICU"

### Step 3: Create Rotation Blocks
1. Go to **Rotation Blocks** → **Add Rotation Block**
2. Create a block for each 2-week period

**Example: Q1 2025 ICU Rotations**
- **Block 1**: ICU Rotation - Jan 6-19, 2025
- **Block 2**: ICU Rotation - Jan 20-Feb 2, 2025
- **Block 3**: ICU Rotation - Feb 3-16, 2025

**Tips:**
- Start on Monday, end on Sunday (14 days)
- Each block will have 2 Fridays
- Name blocks descriptively (include rotation type and dates)

### Step 4: Make Assignments
For each rotation block, assign fellows to their required surveys:

1. Go to **Rotation Blocks**
2. Click **Assignments** for the block you want to configure
3. Use the **Bulk Add** feature:
   - Select fellows (e.g., all 3 fellows)
   - Select surveys (e.g., Self Evaluation + Peer Evaluation)
   - Click **Add Selected**

**Example Assignments for "ICU Block 1":**
- John Smith → Self Evaluation
- John Smith → Peer Evaluation
- Sarah Johnson → Self Evaluation
- Sarah Johnson → Faculty Evaluation
- Michael Lee → Self Evaluation
- Michael Lee → Rotation Evaluation

Each fellow-survey combination becomes one assignment. On Fridays, each assignment will result in one text message.

---

## Part 3: Weekly Workflow

### Thursday (Preparation Day)
1. **Review Next Week's Blocks**
   - Go to **Rotation Blocks**
   - Verify the upcoming block is configured
   - Check assignments are complete

2. **Add Any Missing Assignments**
   - Click into the active block
   - Add any fellows or surveys that were missed

### Friday Morning (Send Day)
1. **Go to Dashboard**
   - Dashboard shows "Next Friday" or "Today is Friday!"

2. **Click "Send Friday Evaluations"**
   - Review the preview of what will be sent
   - Verify fellows and surveys are correct
   - Click **"Send All Evaluations"**

3. **Confirm Success**
   - System shows "Sent X evaluations successfully"
   - Check **Tracking** page to verify all sent

4. **Handle Any Failures**
   - If any fail, check error details in Tracking
   - Fix issues (phone number, Twilio credits, etc.)
   - Can manually resend if needed

### During the Week
- Monitor Qualtrics for completed responses
- Fellows receive evaluations every Friday during their 2-week block
- Typically, fellows receive 2 texts per evaluation (Week 1 Friday + Week 2 Friday)

---

## Part 4: Common Scenarios

### Scenario 1: Fellow Needs Different Evaluations
**Situation:** John rotates to ICU for 2 weeks, needs Self + Peer evaluation

**Solution:**
1. Create "ICU Block 1" rotation (14 days)
2. Assign John → Self Evaluation
3. Assign John → Peer Evaluation
4. On Fridays during those 2 weeks, John gets both texts

### Scenario 2: All Fellows Get Same Evaluations
**Situation:** All 10 fellows need Self + Rotation evaluation for ICU

**Solution:**
1. Create "ICU Block 1"
2. Go to Assignments
3. Select all 10 fellows
4. Select both surveys (Self + Rotation)
5. Click "Add Selected"
6. System creates 20 assignments (10 fellows × 2 surveys)

### Scenario 3: Different Fellows, Different Rotations, Same Week
**Situation:** Week of Jan 6-19:
- 3 fellows in ICU (need ICU evaluations)
- 2 fellows in Clinic (need Clinic evaluations)

**Solution:**
1. Create "ICU Block - Jan 6-19"
   - Assign 3 ICU fellows → ICU surveys
2. Create "Clinic Block - Jan 6-19"
   - Assign 2 clinic fellows → Clinic surveys
3. On Fridays, system sends appropriate evaluations to each group

### Scenario 4: Missed a Friday
**Situation:** You forgot to send evaluations last Friday

**Solution:**
- The system tracks "last_sent" date
- Next Friday, it will send evaluations that weren't sent
- Or you can manually send using "Send Friday Evaluations" any day

### Scenario 5: Testing the System
**Situation:** Want to test before going live

**Solution:**
1. Go to **Settings** → **Test SMS**
2. Enter your phone number
3. Send a test
4. Or create a test rotation block with just yourself

---

## Part 5: Best Practices

### Setting Up Surveys
- Create separate Qualtrics forms for each evaluation type
- Use descriptive names: "Fellow Self-Assessment Q1 2025"
- Include a field in Qualtrics asking for the fellow's name
- Use anonymous links (easier) or personalized links (more tracking)

### Planning Rotation Blocks
- Create blocks 2-3 months in advance
- Name them consistently: "[Rotation] - [Month] [Year]"
- Always use 14-day blocks (Mon-Sun typically)
- Add notes for special circumstances

### Managing Assignments
- Use bulk add for efficiency
- Double-check assignments before the block starts
- Can modify assignments mid-block if needed
- Remove fellows who drop out or are on leave

### Friday Sending
- Establish a routine: Friday 9-10 AM
- Preview before sending
- Check tracking immediately after
- Keep Twilio account funded

### Data Management
- Backup database monthly
- Export tracking data periodically
- Cross-reference with Qualtrics completion data
- Archive old rotation blocks

---

## Part 6: Troubleshooting

### "No evaluations ready to send"
**Cause:** No active rotation blocks, or all already sent today
**Fix:** 
- Check Rotation Blocks - is there one active today?
- Check Assignments - are there assignments in the active block?
- Check Tracking - were they already sent today?

### "Some evaluations failed"
**Cause:** Usually Twilio issues (credits, phone number)
**Fix:**
- Check Twilio console for specific error
- Verify phone numbers in Fellows page
- Ensure Twilio account has credits
- Check tracking page for error details

### "Fellow received wrong survey"
**Cause:** Incorrect assignment
**Fix:**
- Go to the rotation block's assignments
- Remove incorrect assignment
- Add correct assignment
- Fellow will get correct survey next Friday

### "Fellow didn't receive text"
**Cause:** Phone number issue, already sent, or spam filter
**Fix:**
- Verify phone number is correct
- Check tracking - was it marked as "sent"?
- Check Twilio console - did it deliver?
- Ask fellow to check spam/blocked messages
- Can manually resend from Settings → Test SMS

### "Want to send evaluations on Thursday instead"
**Solution:** Just click "Send Friday Evaluations" on Thursday - it works any day!

---

## Part 7: Advanced Features

### Automatic Scheduling (Optional)
You can set up a cron job or scheduled task to run the Friday send automatically:

**Using system cron (Linux/Mac):**
```bash
# Open crontab
crontab -e

# Add this line to send every Friday at 9 AM
0 9 * * 5 cd /path/to/fellowship-evaluations && /path/to/venv/bin/python -c "from app import app, send_friday_evaluations; with app.app_context(): send_friday_evaluations()"
```

**Using Task Scheduler (Windows):**
1. Open Task Scheduler
2. Create new task
3. Trigger: Weekly, Friday, 9:00 AM
4. Action: Run python script

### Customizing Messages
Edit the message template in `app.py`:
```python
# Find this line in send_evaluation_sms function:
message_body = f"Hi {fellow.name}, please complete your {survey.name}: {survey.survey_link}"

# Customize it:
message_body = f"Hello Dr. {fellow.name}, your {survey.name} is ready. Please complete by end of day: {survey.survey_link}"
```

### Multiple Program Directors
Create additional admin users:
```bash
flask create-admin
```

Each can log in independently.

---

## Part 8: Comparison with Original System

| Feature | Original | Enhanced Version |
|---------|----------|------------------|
| Survey Management | Single survey link | Multiple survey types |
| Scheduling | Manual selection | Rotation blocks + Friday automation |
| Flexibility | One evaluation type | Different evaluations per fellow/rotation |
| Assignment Tracking | Basic | Detailed with duplicate prevention |
| Workflow | Select & send | Plan blocks, auto-send on Fridays |
| Use Case | Simple weekly evals | Complex rotation-based programs |

---

## Part 9: Quick Reference

### Common Tasks

**Add a new fellow:**
`Fellows → Add Fellow`

**Create a new survey type:**
`Surveys → Add Survey`

**Set up next rotation:**
`Rotation Blocks → Add Rotation Block`

**Assign fellows to surveys:**
`Rotation Blocks → [Block Name] → Assignments`

**Send Friday evaluations:**
`Dashboard → Send Friday Evaluations` OR `Send Friday Evaluations (sidebar)`

**Check what was sent:**
`Tracking`

**Test the system:**
`Settings → Test SMS`

### Database Backup
```bash
# Backup database
cp fellowship_evals.db fellowship_evals_backup_$(date +%Y%m%d).db
```

---

## Part 10: Example Complete Setup

**Program:** 6-fellow pulmonary/critical care program, 2-week ICU rotations

**Fellows:**
- Alice, Bob, Carol, Dan, Emma, Frank

**Surveys Created:**
1. ICU Self-Evaluation
2. Peer Evaluation 
3. Attending Evaluation
4. ICU Rotation Feedback

**Rotation Blocks (January-February):**
1. ICU Team A - Jan 6-19 (Alice, Bob, Carol)
2. ICU Team B - Jan 6-19 (Dan, Emma, Frank)
3. ICU Team A - Jan 20-Feb 2 (Dan, Emma, Frank)
4. ICU Team B - Jan 20-Feb 2 (Alice, Bob, Carol)

**Assignments for "ICU Team A - Jan 6-19":**
- Alice → ICU Self-Evaluation
- Alice → Peer Evaluation
- Alice → Attending Evaluation
- Bob → ICU Self-Evaluation
- Bob → Peer Evaluation
- Bob → Attending Evaluation
- Carol → ICU Self-Evaluation
- Carol → Peer Evaluation
- Carol → Attending Evaluation
(9 total assignments = 3 fellows × 3 surveys)

**Friday Schedule:**
- Friday Jan 10: All 3 fellows receive 3 texts each (9 total texts)
- Friday Jan 17: All 3 fellows receive 3 texts each (9 total texts)
- Friday Jan 24: Different 3 fellows (next rotation block)

**Total texts per rotation:** 18 texts (9 on each Friday)
**Cost:** ~$0.14 per 2-week rotation

---

## Support

For questions or issues:
1. Check this guide's troubleshooting section
2. Review the in-app help messages
3. Check Flask/Twilio documentation
4. Review the tracking page for specific errors

---

## Summary

This enhanced system provides complete flexibility for managing complex fellowship evaluation requirements across different rotations, multiple survey types, and varying schedules. The key workflow is:

1. **Setup** (once): Add fellows, create surveys, plan rotation blocks
2. **Assignment** (per rotation): Assign fellows to appropriate surveys
3. **Execution** (weekly): Click one button on Fridays to send everything
4. **Tracking** (ongoing): Monitor completion and troubleshoot issues

You now have a professional, scalable system that can handle even the most complex evaluation schedules!
