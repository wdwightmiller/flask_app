# Fellowship Evaluation System - Complete Setup Guide
## Version 2.1: Weekly Blocks with Bulk Creation

---

## What This System Does

This system manages fellowship evaluations with:
- ✅ **Multiple survey types** (self, peer, faculty, rotation)
- ✅ **Weekly rotation blocks** (7-day periods, typically Mon-Sun)
- ✅ **Flexible assignments** (different surveys for different fellows each week)
- ✅ **Automated Friday sending** (system knows what to send when)
- ✅ **Bulk planning** (set up entire semester in minutes)

---

## Key Concept: How It Works

### The System Has 4 Components:

**1. Fellows** - Your residents/fellows
   - Name, phone number, email
   - Add once, reuse every week

**2. Surveys** - Different evaluation types
   - Each survey = one Qualtrics form
   - Examples: "Self Evaluation", "Peer Evaluation", "Attending Evaluation"

**3. Rotation Blocks** - Weekly time periods
   - Each block = 7 days (Monday-Sunday)
   - Contains one Friday when evaluations are sent
   - Create many weeks at once with bulk tool

**4. Assignments** - Links fellows to surveys for specific weeks
   - "During Week 1, John gets Survey A and Survey B"
   - "During Week 2, John gets Survey C"
   - Different assignments each week

### The Workflow:

**Setup Phase (Do Once):**
1. Add all your fellows
2. Create all your survey types
3. Use bulk tool to create 8-12 weeks of rotation blocks
4. Go through each week and assign fellows to appropriate surveys

**Weekly Phase (Every Friday):**
1. Click "Send Friday Evaluations"
2. Review what will be sent
3. Click "Send All"
4. Done! System sends appropriate texts to each fellow

---

## Part 1: Initial Setup

### Step 1: Install and Configure

```bash
# Extract the ZIP file
cd fellowship-evaluations

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### Step 2: Configure Twilio

Edit `.env` file:
```
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+15551234567
SECRET_KEY=generate_random_string_here
```

Get these from twilio.com console.

### Step 3: Initialize Database

```bash
flask init-db
flask create-admin
# Enter username and password when prompted
```

### Step 4: Start Application

```bash
python app.py
```

Open browser: http://localhost:5000

---

## Part 2: System Setup

### Step 1: Add Fellows

**Navigate:** Fellows → Add Fellow

Add each fellow:
- **Name:** John Smith
- **Phone:** (555) 123-4567
- **Email:** jsmith@hospital.edu (optional)

Repeat for all fellows.

### Step 2: Create Survey Types

**Navigate:** Surveys → Add Survey

Create each evaluation type you need:

**Example Surveys:**

**Survey 1:**
- Name: "Self Evaluation"
- Type: Self
- Link: https://yourschool.qualtrics.com/jfe/form/SV_self123
- Description: "Fellows assess their performance"

**Survey 2:**
- Name: "Peer Evaluation"
- Type: Peer
- Link: https://yourschool.qualtrics.com/jfe/form/SV_peer456
- Description: "Fellows evaluate colleagues"

**Survey 3:**
- Name: "Attending Evaluation"
- Type: Faculty
- Link: https://yourschool.qualtrics.com/jfe/form/SV_attend789
- Description: "Fellows evaluate attendings"

**Survey 4:**
- Name: "Rotation Evaluation"
- Type: Rotation
- Link: https://yourschool.qualtrics.com/jfe/form/SV_rotation321
- Description: "End-of-rotation feedback"

**Pro Tip:** Create separate surveys for different rotations if needed:
- "ICU Rotation Evaluation"
- "Clinic Rotation Evaluation"
- "Consult Rotation Evaluation"

### Step 3: Create Weekly Blocks (BULK METHOD - Recommended)

**Navigate:** Rotation Blocks → Bulk Create Weeks

**Settings:**
- **First Week Start Date:** Jan 6, 2025 (choose a Monday)
- **Number of Weeks:** 12 (or however many you want)
- **Name Template:** `Week {week} - {start} to {end}, {year}`

Click "Preview Blocks" to see what will be created.
Click "Create All Blocks" to create them.

**Result:** System creates 12 consecutive weekly blocks automatically!
- Week 1 - Jan 6 to Jan 12, 2025
- Week 2 - Jan 13 to Jan 19, 2025
- Week 3 - Jan 20 to Jan 26, 2025
- ... and so on

**Alternative Name Templates:**
- `ICU Week {week}` - Simple numbering
- `{start}-{end}` - Just dates
- `Block {week} ({start})` - Block number with start date

### Step 4: Make Assignments for Each Week

Now the important part - assign fellows to surveys for each week.

**Navigate:** Rotation Blocks → Click "Assignments" for a specific week

**Example: Week 1 Assignments**

If Week 1 is ICU rotation for John, Sarah, and Michael:

1. Click "Assignments" for Week 1
2. In the bulk add section:
   - **Select Fellows:** Check John, Sarah, Michael
   - **Select Surveys:** Check "Self Evaluation", "Peer Evaluation"
   - Click "Add Selected"

This creates 6 assignments (3 fellows × 2 surveys).

**Example: Week 2 Assignments**

If Week 2 has different fellows on different rotations:
- John in Clinic → assign "Self Evaluation", "Attending Evaluation"
- Sarah in ICU → assign "Self Evaluation", "Peer Evaluation"  
- Michael on vacation → assign nothing

Just repeat this process for each week you created!

---

## Part 3: Weekly Operation

### Every Friday:

**Navigate:** Dashboard → Send Friday Evaluations

**OR:** Click "Send Friday Evaluations" in sidebar

**What You'll See:**
- Preview of all evaluations to be sent today
- List of fellows and their assigned surveys
- Total count

**Click:** "Send All Evaluations"

**System will:**
- Find all active rotation blocks (blocks that include today)
- Get all assignments for those blocks
- Send each fellow their assigned surveys via text
- Track what was sent to prevent duplicates
- Log everything

**Check Results:**
- Go to "Tracking" page
- Verify all sent successfully
- Check for any failures

---

## Part 4: Real-World Example

### Scenario: 6-week ICU and Clinic rotation

**Fellows:**
- Alice, Bob, Carol (3 fellows)

**Surveys:**
1. ICU Self Evaluation
2. Clinic Self Evaluation
3. Peer Evaluation
4. Attending Evaluation

**Rotation Schedule:**
- Weeks 1-3: All in ICU
- Weeks 4-6: All in Clinic

**Setup:**

1. **Create 6 weekly blocks** (bulk create)
   - Week 1 - Jan 6-12
   - Week 2 - Jan 13-19
   - Week 3 - Jan 20-26
   - Week 4 - Jan 27-Feb 2
   - Week 5 - Feb 3-9
   - Week 6 - Feb 10-16

2. **Assign Week 1-3** (ICU weeks):
   - All 3 fellows → ICU Self Evaluation
   - All 3 fellows → Peer Evaluation
   - All 3 fellows → Attending Evaluation

3. **Assign Week 4-6** (Clinic weeks):
   - All 3 fellows → Clinic Self Evaluation
   - All 3 fellows → Attending Evaluation

**Result Each Friday:**
- **Jan 10 (Week 1):** Each fellow gets 3 texts (ICU Self + Peer + Attending)
- **Jan 17 (Week 2):** Each fellow gets 3 texts (same as week 1)
- **Jan 24 (Week 3):** Each fellow gets 3 texts (same as week 1)
- **Jan 31 (Week 4):** Each fellow gets 2 texts (Clinic Self + Attending)
- **Feb 7 (Week 5):** Each fellow gets 2 texts (same as week 4)
- **Feb 14 (Week 6):** Each fellow gets 2 texts (same as week 4)

Total: 78 texts over 6 weeks (3 fellows × 13 evaluations each)
Cost: ~$0.62 for the entire 6-week period

---

## Part 5: Common Scenarios

### Scenario 1: Fellow Switches Rotations Mid-Week

**Problem:** John was supposed to be in ICU this week but switched to Clinic on Wednesday.

**Solution:**
- Go to that week's rotation block
- Go to Assignments
- Remove John's ICU-related assignments
- Add John's Clinic-related assignments
- If Friday hasn't happened yet, he'll get correct surveys
- If Friday already passed, you can manually resend from Settings → Test SMS

### Scenario 2: Fellow on Vacation

**Problem:** Sarah is on vacation Week 3.

**Solution:**
- Simply don't assign Sarah to any surveys for Week 3
- She won't receive any texts that Friday
- Resume assignments in Week 4

### Scenario 3: One-Time Extra Evaluation

**Problem:** Need to send a special evaluation to all fellows this Friday only.

**Solution:**
- Create a new survey for the special evaluation
- Go to this week's block → Assignments
- Bulk add all fellows to the special survey
- It will be sent this Friday only

### Scenario 4: Forgot to Send Last Friday

**Problem:** You were out sick last Friday and forgot to send.

**Solution:**
- The system tracks "last_sent" date
- Go to "Send Friday Evaluations" any day
- Click "Send All Evaluations"
- System will send any assignments that weren't sent

### Scenario 5: Testing Before Going Live

**Problem:** Want to test the system.

**Solution:**
- Create a test week
- Assign yourself to a survey
- Go to Settings → Test SMS
- Enter your phone number
- Send test
- OR use "Send Friday Evaluations" even on non-Friday

---

## Part 6: Advanced Tips

### Tip 1: Plan Entire Semester at Once

**Best Practice:**
1. Use bulk create to make 12-16 weeks
2. Block out 2-3 hours
3. Go through each week and make assignments
4. Now you're done for 3-4 months!

### Tip 2: Rotation-Specific Survey Names

Instead of generic "Self Evaluation", create:
- "ICU Self Evaluation"
- "Clinic Self Evaluation"
- "Procedure Self Evaluation"

This makes it clearer for fellows what they're evaluating.

### Tip 3: Use Consistent Naming

For rotation blocks, use consistent naming:
- `Week {week} - {start} to {end}`
- Makes it easy to find the right week

### Tip 4: Check Assignments Thursday

Every Thursday:
- Review next week's rotation block
- Verify assignments are correct
- Make any last-minute changes

### Tip 5: Backup Your Data

Monthly:
```bash
cp fellowship_evals.db backup_$(date +%Y%m%d).db
```

### Tip 6: Cross-Reference with Qualtrics

Weekly after sending:
- Check Qualtrics for completion rates
- Follow up with fellows who haven't completed
- Export Qualtrics data for analysis

---

## Part 7: Troubleshooting

### "No evaluations ready to send"

**Causes:**
- No active rotation block for this week
- No assignments in the active block
- All assignments already sent today

**Fix:**
1. Go to Rotation Blocks
2. Check if there's a block for this week
3. Click into it and check Assignments
4. Check Tracking to see if already sent

### "Some evaluations failed"

**Causes:**
- Twilio account out of credits
- Invalid phone number
- Twilio service issues

**Fix:**
1. Check Twilio console for details
2. Verify phone numbers are correct
3. Ensure Twilio account is funded
4. Check Tracking page for specific errors

### "Fellow got wrong survey"

**Cause:** Incorrect assignment

**Fix:**
1. Go to that week's rotation block
2. View Assignments
3. Remove incorrect assignment
4. Add correct assignment
5. Fellow will get correct survey next Friday

### "Need to resend to one fellow"

**Solution:**
- Go to Settings → Test SMS
- Select the survey from the dropdown
- Enter fellow's phone number
- Click "Send Test"

---

## Part 8: System Limitations

**What the System Does:**
- ✅ Send evaluation links via SMS
- ✅ Track when evaluations were sent
- ✅ Prevent duplicate sends on same day
- ✅ Organize by week and survey type

**What the System Doesn't Do:**
- ❌ Track if fellow completed the evaluation (check Qualtrics)
- ❌ Send reminders automatically (you can manually resend)
- ❌ Integrate directly with Qualtrics API
- ❌ Handle email notifications (SMS only)

---

## Part 9: Deployment to Production

### For Long-Term Use: Deploy to Render

**Why:** 
- Your computer doesn't need to be running
- Accessible from anywhere
- More reliable

**How:**
1. Sign up at render.com
2. Create new Web Service
3. Connect GitHub repository
4. Set environment variables
5. Deploy

Full deployment instructions in original FLASK_SETUP_GUIDE.md

**Cost:** Free tier available, $7/month for always-on

---

## Part 10: Quick Reference

### Common Tasks

| Task | Location |
|------|----------|
| Add a fellow | Fellows → Add Fellow |
| Create survey type | Surveys → Add Survey |
| Create many weeks | Rotation Blocks → Bulk Create |
| Assign fellows to surveys | Rotation Blocks → [Week] → Assignments |
| Send Friday evaluations | Send Friday Evaluations |
| Check what was sent | Tracking |
| Test the system | Settings → Test SMS |

### Keyboard Shortcuts (None - it's web-based)

Use your browser's standard shortcuts:
- Ctrl+F (Cmd+F on Mac): Find text on page
- Ctrl+Click: Open link in new tab

---

## Summary

This system gives you complete control over a complex evaluation schedule:

1. **One-time setup:** Add fellows, create surveys, bulk create weeks
2. **Planning phase:** Assign fellows to surveys for each week (can do months in advance)
3. **Weekly execution:** One click on Friday to send everything
4. **Tracking:** Monitor what was sent and troubleshoot issues

**Key Advantage:** Each week can have completely different assignments. John can be in ICU Week 1 (getting ICU surveys), Clinic Week 2 (getting Clinic surveys), and Procedure Week 3 (getting Procedure surveys). The system handles all of this automatically.

**Time Investment:**
- Initial setup: 1-2 hours
- Planning semester: 2-3 hours (do once per semester)
- Weekly operation: 2 minutes (just click send on Friday)

You now have a professional, flexible, and powerful evaluation management system!

---

## Need Help?

1. Check this guide's troubleshooting section
2. Review the in-app messages and tooltips
3. Check Tracking page for specific errors
4. Review Twilio console for SMS delivery issues

Good luck with your fellowship evaluations!
