# Fellowship Evaluation System - Flask Web Application Setup Guide

## Overview
This is a complete web application for managing fellowship evaluations with SMS notifications via Twilio. It includes user authentication, database storage, and a professional web interface.

---

## Features

✅ **Professional Web Interface** - Modern, responsive design using Bootstrap 5
✅ **User Authentication** - Secure login system
✅ **Fellow Management** - Add, edit, and track fellows
✅ **Faculty Management** - Maintain faculty directory
✅ **SMS Integration** - Send evaluation requests via Twilio
✅ **Tracking & Logging** - Complete history of all sent evaluations
✅ **Database Storage** - SQLite database for all data
✅ **Test Functionality** - Send test SMS before going live

---

## Part 1: System Requirements

### What You Need:
- Python 3.8 or higher
- A computer (Mac, Windows, or Linux)
- A Twilio account (you have this ✓)
- A Qualtrics survey link

### Recommended Hosting:
- **For Testing/Personal Use:** Run locally on your computer
- **For Production:** Deploy to Render, PythonAnywhere, or Railway (all have free tiers)

---

## Part 2: Initial Setup

### Step 1: Install Python
If you don't have Python installed:
- **Mac/Linux:** Python is usually pre-installed. Check with `python3 --version`
- **Windows:** Download from python.org

### Step 2: Create Project Folder
Create a folder for your project and extract all the files there:
```
fellowship-evaluations/
├── app.py
├── requirements.txt
├── .env.example
└── templates/
    ├── base.html
    ├── login.html
    ├── index.html
    ├── send_evaluations.html
    ├── fellows.html
    ├── add_fellow.html
    ├── edit_fellow.html
    ├── tracking.html
    ├── faculty.html
    ├── add_faculty.html
    └── settings.html
```

### Step 3: Create Virtual Environment
Open Terminal (Mac/Linux) or Command Prompt (Windows) and navigate to your project folder:

```bash
cd path/to/fellowship-evaluations

# Create virtual environment
python3 -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs Flask, Twilio, and other required packages.

---

## Part 3: Configuration

### Step 1: Create .env File
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

### Step 2: Edit .env File
Open `.env` in a text editor and fill in your credentials:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=AC1234567890abcdef1234567890abcdef
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+15551234567

# Qualtrics Survey Link
QUALTRICS_SURVEY_LINK=https://yourschool.qualtrics.com/jfe/form/SV_xxxxxxxxxxxxx

# Flask Secret Key (generate a random string)
SECRET_KEY=generate-a-random-secret-key-here
```

**To generate a secure SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Step 3: Get Twilio Credentials
1. Log into twilio.com
2. Go to Console Dashboard
3. Copy:
   - **Account SID** (starts with "AC...")
   - **Auth Token** (click "Show" to reveal)
   - **Phone Number** (from your active numbers)

### Step 4: Get Qualtrics Link
1. Log into Qualtrics
2. Go to your evaluation survey
3. Click "Distributions" → "Anonymous Link"
4. Copy the full URL

---

## Part 4: Initialize the Database

### Step 1: Initialize Database
```bash
flask init-db
```

This creates the SQLite database file (`fellowship_evals.db`).

### Step 2: Create Admin User
```bash
flask create-admin
```

Follow the prompts to create your admin account:
- Enter username (e.g., `admin`)
- Enter password (choose a secure password)
- Enter email (optional)

**Important:** Remember these credentials - you'll need them to log in!

---

## Part 5: Run the Application

### For Local Testing:
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

Open your web browser and go to: **http://localhost:5000**

### First Login:
1. Use the admin credentials you created
2. You should see the Dashboard

---

## Part 6: Using the System

### Add Fellows
1. Click **Fellows** in the sidebar
2. Click **Add Fellow** button
3. Enter:
   - Fellow's name
   - Phone number (any format)
   - Email (optional)
4. Click **Add Fellow**

### Add Faculty (Optional)
1. Click **Faculty** in the sidebar
2. Click **Add Faculty** button
3. Enter faculty information
4. Click **Add Faculty Member**

### Send Evaluations
1. Click **Send Evaluations** in the sidebar
2. Check the boxes next to fellows who should receive evaluations
3. (Optional) Enter a custom message
4. Click **Send Evaluation Texts**

### View Tracking
1. Click **Tracking** in the sidebar
2. See all sent evaluations with status (sent/failed)
3. Review any error messages

### Test SMS Function
1. Go to **Settings**
2. Scroll to "Test SMS"
3. Enter your phone number
4. Click **Send Test**
5. You should receive a text within seconds

---

## Part 7: Deploy to the Web (Optional)

### Option A: Deploy to Render (Recommended - Free Tier Available)

1. **Sign up for Render:** Go to render.com and create a free account

2. **Create requirements.txt for production:**
Add `gunicorn` to your requirements.txt:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
twilio==8.11.0
python-dotenv==1.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

3. **Create Procfile:**
Create a file named `Procfile` (no extension) with:
```
web: gunicorn app:app
```

4. **Push to GitHub:**
   - Create a GitHub repository
   - Push your code (don't commit .env file!)

5. **Connect to Render:**
   - In Render, click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** fellowship-evaluations
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`

6. **Add Environment Variables:**
   In Render dashboard, go to "Environment" and add:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_PHONE_NUMBER`
   - `QUALTRICS_SURVEY_LINK`
   - `SECRET_KEY`

7. **Deploy:**
   - Click "Create Web Service"
   - Render will build and deploy your app
   - You'll get a URL like: `https://fellowship-evaluations.onrender.com`

8. **Initialize Database on Render:**
   - Go to "Shell" tab in Render
   - Run: `flask init-db`
   - Run: `flask create-admin`

### Option B: Deploy to PythonAnywhere

1. Sign up at pythonanywhere.com (free tier available)
2. Upload your files
3. Configure web app in dashboard
4. Set environment variables
5. Initialize database using bash console

### Option C: Deploy to Railway

1. Sign up at railway.app
2. Similar process to Render
3. Connect GitHub repository
4. Configure environment variables
5. Deploy

---

## Part 8: Security Best Practices

### Important Security Notes:

1. **Never commit .env file to Git**
   Add `.env` to your `.gitignore` file:
   ```
   .env
   fellowship_evals.db
   venv/
   __pycache__/
   ```

2. **Use Strong Passwords**
   - Admin password should be complex
   - Change default SECRET_KEY

3. **HTTPS in Production**
   - Render/Railway provide HTTPS automatically
   - Don't use HTTP for production

4. **Backup Your Database**
   - Regularly backup `fellowship_evals.db`
   - Export fellows data periodically

5. **Limit Access**
   - Only share login credentials with trusted individuals
   - Consider adding more user accounts if needed

---

## Part 9: Troubleshooting

### "Module not found" errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Can't connect to database
```bash
# Reinitialize database
flask init-db
flask create-admin
```

### Twilio errors
- Check your Twilio account balance
- Verify phone numbers are formatted correctly
- Check Twilio console logs for specific errors

### Can't log in
- Make sure you created an admin user
- Password is case-sensitive
- Try creating a new admin user:
  ```bash
  flask create-admin
  ```

### Port already in use
If port 5000 is in use, run on a different port:
```bash
flask run --port 5001
```

---

## Part 10: Daily Workflow

### Weekly Evaluation Process:
1. **Log in** to the web application
2. Go to **Send Evaluations**
3. **Select fellows** who need evaluations this week
4. **Review** the message preview
5. **Click** "Send Evaluation Texts"
6. **Check** Tracking page to confirm all sent successfully
7. **Monitor** Qualtrics for completed responses

### Adding New Fellows:
1. Click **Fellows** → **Add Fellow**
2. Enter their information
3. They'll automatically be included in future evaluations

### Viewing History:
1. Click **Tracking** to see all sent evaluations
2. Use pagination to browse older records
3. Check for any failed sends

---

## Part 11: Cost Estimate

### Twilio Costs:
- **SMS:** ~$0.0079 per message
- **Monthly Example:** 10 fellows × 4 weeks = 40 texts = **~$0.32/month**

### Hosting Costs:
- **Render Free Tier:** $0/month (with limitations)
- **Render Starter:** $7/month (recommended for production)
- **PythonAnywhere Free:** $0/month (limited)
- **Railway Free:** $5 credit/month

### Total Monthly Cost:
- **Development/Testing:** $0
- **Small Fellowship (10 fellows):** ~$7-10/month
- **Large Fellowship (30 fellows):** ~$8-12/month

Very affordable for what it provides!

---

## Part 12: Advanced Features (Future Enhancements)

You can extend this system to:
- **Email notifications** instead of SMS
- **Scheduled sending** (automatic weekly sends)
- **Qualtrics integration** to track completions automatically
- **Multiple survey links** for different rotation types
- **Reports and analytics** dashboard
- **Reminder texts** for incomplete evaluations
- **Faculty evaluation requests** using the same system

---

## Support & Maintenance

### Regular Maintenance:
- Backup database monthly
- Review Twilio usage and costs
- Update Python packages periodically:
  ```bash
  pip install --upgrade -r requirements.txt
  ```

### Getting Help:
- Check the Tracking page for error details
- Review Twilio console logs
- Check Flask debug output in terminal

---

## Quick Reference Commands

```bash
# Start application
python app.py

# Initialize database
flask init-db

# Create admin user
flask create-admin

# Run on different port
flask run --port 5001

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Deactivate virtual environment
deactivate
```

---

## Comparison: Flask vs Google Sheets

### Flask Web App Advantages:
✅ Professional interface
✅ Better data management
✅ User authentication
✅ Scalable for larger programs
✅ Can add more features easily
✅ Better tracking and reporting

### Google Sheets Advantages:
✅ Simpler setup (no programming required)
✅ No hosting needed
✅ Easy to share with others
✅ Familiar spreadsheet interface
✅ Quick to get started

**Recommendation:** 
- **Small program (< 10 fellows):** Google Sheets solution is perfect
- **Larger program or multiple users:** Flask web app is better
- **Technical comfort:** If comfortable with terminal/code, Flask is more powerful

---

## Conclusion

You now have a complete, professional fellowship evaluation system! The Flask app provides:
- Secure web interface
- Complete fellow management
- SMS integration via Twilio
- Comprehensive tracking
- Easy to use and maintain

For questions or issues, refer back to the troubleshooting section or review the Flask and Twilio documentation.

Good luck with your fellowship evaluations!
