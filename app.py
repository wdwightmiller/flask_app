from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from twilio.rest import Client
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-to-a-random-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fellowship_evals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')


# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Fellow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    evaluations = db.relationship('Evaluation', backref='fellow', lazy=True)
    assignments = db.relationship('RotationAssignment', backref='fellow', lazy=True)


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Survey(db.Model):
    """Different types of surveys/evaluations"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., "Fellow Self-Evaluation", "Peer Evaluation"
    description = db.Column(db.Text)
    survey_link = db.Column(db.String(500), nullable=False)
    survey_type = db.Column(db.String(50))  # 'self', 'peer', 'faculty', 'rotation'
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assignments = db.relationship('RotationAssignment', backref='survey', lazy=True)


class RotationBlock(db.Model):
    """Weekly rotation blocks (typically 7 days, Monday-Sunday)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., "ICU Week 1 - Jan 6-12, 2025"
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assignments = db.relationship('RotationAssignment', backref='rotation_block', lazy=True)
    
    def get_friday(self):
        """Return the Friday date in this rotation block (if any)"""
        current_date = self.start_date
        while current_date <= self.end_date:
            if current_date.weekday() == 4:  # Friday is 4
                return current_date
            current_date += timedelta(days=1)
        return None
    
    def get_fridays(self):
        """Return all Friday dates in this rotation block (for backward compatibility)"""
        friday = self.get_friday()
        return [friday] if friday else []
    
    @property
    def is_active(self):
        """Check if this block is currently active"""
        today = datetime.now().date()
        return self.start_date <= today <= self.end_date
    
    @property
    def is_upcoming(self):
        """Check if this block is in the future"""
        today = datetime.now().date()
        return self.start_date > today


class RotationAssignment(db.Model):
    """Assigns fellows to surveys for specific rotation blocks"""
    id = db.Column(db.Integer, primary_key=True)
    fellow_id = db.Column(db.Integer, db.ForeignKey('fellow.id'), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    rotation_block_id = db.Column(db.Integer, db.ForeignKey('rotation_block.id'), nullable=False)
    send_on_fridays = db.Column(db.Boolean, default=True)
    last_sent = db.Column(db.Date)  # Track last send date to avoid duplicates
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint: one fellow can't have the same survey twice in the same rotation
    __table_args__ = (db.UniqueConstraint('fellow_id', 'survey_id', 'rotation_block_id'),)


class Evaluation(db.Model):
    """Log of sent evaluations"""
    id = db.Column(db.Integer, primary_key=True)
    fellow_id = db.Column(db.Integer, db.ForeignKey('fellow.id'), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
    rotation_assignment_id = db.Column(db.Integer, db.ForeignKey('rotation_assignment.id'))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='sent')  # sent, failed, completed
    message_sid = db.Column(db.String(100))  # Twilio message ID
    completed_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Helper Functions
def format_phone_number(phone):
    """Format phone number to E.164 format"""
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    # Add +1 if it's a 10-digit US number
    if len(digits) == 10:
        return f'+1{digits}'
    elif len(digits) == 11 and digits.startswith('1'):
        return f'+{digits}'
    else:
        return f'+{digits}'


def send_evaluation_sms(fellow, survey, rotation_assignment=None, custom_message=None):
    """Send evaluation SMS via Twilio"""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        if custom_message:
            message_body = custom_message.replace('{name}', fellow.name).replace('{link}', survey.survey_link)
        else:
            message_body = f"Hi {fellow.name}, please complete your {survey.name}: {survey.survey_link}"
        
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=format_phone_number(fellow.phone_number)
        )
        
        # Log the evaluation
        evaluation = Evaluation(
            fellow_id=fellow.id,
            survey_id=survey.id,
            rotation_assignment_id=rotation_assignment.id if rotation_assignment else None,
            status='sent',
            message_sid=message.sid
        )
        db.session.add(evaluation)
        
        # Update last_sent date on the assignment
        if rotation_assignment:
            rotation_assignment.last_sent = datetime.now().date()
        
        db.session.commit()
        
        return True, message.sid
    except Exception as e:
        # Log failed evaluation
        evaluation = Evaluation(
            fellow_id=fellow.id,
            survey_id=survey.id if survey else None,
            rotation_assignment_id=rotation_assignment.id if rotation_assignment else None,
            status='failed',
            notes=str(e)
        )
        db.session.add(evaluation)
        db.session.commit()
        
        return False, str(e)


# Routes
@app.route('/')
@login_required
def index():
    fellows = Fellow.query.filter_by(active=True).all()
    faculty = Faculty.query.filter_by(active=True).all()
    surveys = Survey.query.filter_by(active=True).all()
    
    # Get recent evaluations
    recent_evals = Evaluation.query.order_by(Evaluation.sent_at.desc()).limit(10).all()
    
    # Calculate statistics
    total_fellows = len(fellows)
    total_surveys = len(surveys)
    total_evals_sent = Evaluation.query.filter_by(status='sent').count()
    total_evals_failed = Evaluation.query.filter_by(status='failed').count()
    
    # Get active rotation blocks
    today = datetime.now().date()
    active_blocks = RotationBlock.query.filter(
        RotationBlock.start_date <= today,
        RotationBlock.end_date >= today
    ).all()
    
    # Get upcoming Friday info
    days_until_friday = (4 - today.weekday()) % 7
    if days_until_friday == 0:
        next_friday_message = "Today is Friday!"
    else:
        next_friday = today + timedelta(days=days_until_friday)
        next_friday_message = f"Next Friday: {next_friday.strftime('%B %d, %Y')}"
    
    return render_template('index.html', 
                         fellows=fellows,
                         faculty=faculty,
                         surveys=surveys,
                         recent_evals=recent_evals,
                         total_fellows=total_fellows,
                         total_surveys=total_surveys,
                         total_evals_sent=total_evals_sent,
                         total_evals_failed=total_evals_failed,
                         active_blocks=active_blocks,
                         next_friday_message=next_friday_message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/fellows')
@login_required
def fellows():
    fellows_list = Fellow.query.all()
    return render_template('fellows.html', fellows=fellows_list)


@app.route('/fellows/add', methods=['GET', 'POST'])
@login_required
def add_fellow():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone_number')
        email = request.form.get('email')
        
        fellow = Fellow(name=name, phone_number=phone, email=email)
        db.session.add(fellow)
        db.session.commit()
        
        flash(f'Fellow {name} added successfully!', 'success')
        return redirect(url_for('fellows'))
    
    return render_template('add_fellow.html')


@app.route('/fellows/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_fellow(id):
    fellow = Fellow.query.get_or_404(id)
    
    if request.method == 'POST':
        fellow.name = request.form.get('name')
        fellow.phone_number = request.form.get('phone_number')
        fellow.email = request.form.get('email')
        fellow.active = request.form.get('active') == 'on'
        
        db.session.commit()
        flash(f'Fellow {fellow.name} updated successfully!', 'success')
        return redirect(url_for('fellows'))
    
    return render_template('edit_fellow.html', fellow=fellow)


@app.route('/fellows/delete/<int:id>')
@login_required
def delete_fellow(id):
    fellow = Fellow.query.get_or_404(id)
    fellow.active = False
    db.session.commit()
    
    flash(f'Fellow {fellow.name} deactivated', 'success')
    return redirect(url_for('fellows'))


@app.route('/faculty')
@login_required
def faculty_list():
    faculty = Faculty.query.all()
    return render_template('faculty.html', faculty=faculty)


@app.route('/faculty/add', methods=['GET', 'POST'])
@login_required
def add_faculty():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone_number')
        email = request.form.get('email')
        
        faculty = Faculty(name=name, phone_number=phone, email=email)
        db.session.add(faculty)
        db.session.commit()
        
        flash(f'Faculty member {name} added successfully!', 'success')
        return redirect(url_for('faculty_list'))
    
    return render_template('add_faculty.html')

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




@app.route('/send-evaluations', methods=['GET', 'POST'])
@login_required
def send_evaluations():
    if request.method == 'POST':
        selected_fellow_ids = request.form.getlist('fellow_ids')
        custom_message = request.form.get('custom_message', '').strip()
        
        if not selected_fellow_ids:
            flash('Please select at least one fellow', 'error')
            return redirect(url_for('send_evaluations'))
        
        success_count = 0
        failed_count = 0
        
        for fellow_id in selected_fellow_ids:
            fellow = Fellow.query.get(fellow_id)
            if fellow:
                success, result = send_evaluation_sms(
                    fellow, 
                    custom_message if custom_message else None
                )
                if success:
                    success_count += 1
                else:
                    failed_count += 1
        
        if failed_count == 0:
            flash(f'Successfully sent {success_count} evaluation requests!', 'success')
        else:
            flash(f'Sent {success_count} successfully, {failed_count} failed. Check the tracking page for details.', 'warning')
        
        return redirect(url_for('tracking'))
    
    fellows = Fellow.query.filter_by(active=True).all()
    return render_template('send_evaluations.html', fellows=fellows, qualtrics_link=QUALTRICS_SURVEY_LINK)


# Survey Management Routes
@app.route('/surveys')
@login_required
def surveys():
    surveys_list = Survey.query.all()
    return render_template('surveys.html', surveys=surveys_list)


@app.route('/surveys/add', methods=['GET', 'POST'])
@login_required
def add_survey():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        survey_link = request.form.get('survey_link')
        survey_type = request.form.get('survey_type')
        
        survey = Survey(
            name=name,
            description=description,
            survey_link=survey_link,
            survey_type=survey_type
        )
        db.session.add(survey)
        db.session.commit()
        
        flash(f'Survey "{name}" added successfully!', 'success')
        return redirect(url_for('surveys'))
    
    return render_template('add_survey.html')


@app.route('/surveys/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_survey(id):
    survey = Survey.query.get_or_404(id)
    
    if request.method == 'POST':
        survey.name = request.form.get('name')
        survey.description = request.form.get('description')
        survey.survey_link = request.form.get('survey_link')
        survey.survey_type = request.form.get('survey_type')
        survey.active = request.form.get('active') == 'on'
        
        db.session.commit()
        flash(f'Survey "{survey.name}" updated successfully!', 'success')
        return redirect(url_for('surveys'))
    
    return render_template('edit_survey.html', survey=survey)


@app.route('/surveys/delete/<int:id>')
@login_required
def delete_survey(id):
    survey = Survey.query.get_or_404(id)
    survey.active = False
    db.session.commit()
    
    flash(f'Survey "{survey.name}" deactivated', 'success')
    return redirect(url_for('surveys'))


# Rotation Block Management Routes
@app.route('/rotation-blocks')
@login_required
def rotation_blocks():
    blocks = RotationBlock.query.order_by(RotationBlock.start_date.desc()).all()
    return render_template('rotation_blocks.html', blocks=blocks)


@app.route('/rotation-blocks/add', methods=['GET', 'POST'])
@login_required
def add_rotation_block():
    if request.method == 'POST':
        name = request.form.get('name')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        notes = request.form.get('notes')
        
        # Validate that it's a 1-week block (7 days)
        days_diff = (end_date - start_date).days
        if days_diff != 6:
            flash(f'Warning: Block is {days_diff + 1} days. Typically blocks should be 7 days (1 week, Mon-Sun).', 'warning')
        
        block = RotationBlock(
            name=name,
            start_date=start_date,
            end_date=end_date,
            notes=notes
        )
        db.session.add(block)
        db.session.commit()
        
        flash(f'Rotation block "{name}" added successfully!', 'success')
        return redirect(url_for('rotation_blocks'))
    
    return render_template('add_rotation_block.html')


@app.route('/rotation-blocks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_rotation_block(id):
    block = RotationBlock.query.get_or_404(id)
    
    if request.method == 'POST':
        block.name = request.form.get('name')
        block.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        block.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        block.notes = request.form.get('notes')
        
        db.session.commit()
        flash(f'Rotation block "{block.name}" updated successfully!', 'success')
        return redirect(url_for('rotation_blocks'))
    
    return render_template('edit_rotation_block.html', block=block)


@app.route('/rotation-blocks/bulk-create', methods=['GET', 'POST'])
@login_required
def bulk_create_blocks():
    """Create multiple weekly blocks at once"""
    if request.method == 'POST':
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        num_weeks = int(request.form.get('num_weeks'))
        name_template = request.form.get('name_template')
        
        created_blocks = []
        current_start = start_date
        
        for week_num in range(1, num_weeks + 1):
            # Calculate end date (6 days later for 7-day week)
            current_end = current_start + timedelta(days=6)
            
            # Format the name
            block_name = name_template.replace('{week}', str(week_num))
            block_name = block_name.replace('{start}', current_start.strftime('%b %d'))
            block_name = block_name.replace('{end}', current_end.strftime('%b %d'))
            block_name = block_name.replace('{year}', current_start.strftime('%Y'))
            
            # Create the block
            block = RotationBlock(
                name=block_name,
                start_date=current_start,
                end_date=current_end
            )
            db.session.add(block)
            created_blocks.append(block_name)
            
            # Move to next week
            current_start = current_end + timedelta(days=1)
        
        db.session.commit()
        
        flash(f'Successfully created {num_weeks} rotation blocks!', 'success')
        return redirect(url_for('rotation_blocks'))
    
    return render_template('bulk_create_blocks.html')


# Assignment Management Routes
@app.route('/assignments')
@login_required
def assignments():
    # Get current and upcoming rotation blocks
    today = datetime.now().date()
    blocks = RotationBlock.query.filter(RotationBlock.end_date >= today).order_by(RotationBlock.start_date).all()
    
    return render_template('assignments.html', blocks=blocks)


@app.route('/assignments/block/<int:block_id>')
@login_required
def view_block_assignments(block_id):
    block = RotationBlock.query.get_or_404(block_id)
    assignments = RotationAssignment.query.filter_by(rotation_block_id=block_id).all()
    fellows = Fellow.query.filter_by(active=True).all()
    surveys = Survey.query.filter_by(active=True).all()
    
    return render_template('block_assignments.html', block=block, assignments=assignments, 
                         fellows=fellows, surveys=surveys)


@app.route('/assignments/add', methods=['POST'])
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
    
    return redirect(url_for('view_block_assignments', block_id=rotation_block_id))


@app.route('/assignments/delete/<int:id>')
@login_required
def delete_assignment(id):
    assignment = RotationAssignment.query.get_or_404(id)
    block_id = assignment.rotation_block_id
    db.session.delete(assignment)
    db.session.commit()
    
    flash('Assignment deleted', 'success')
    return redirect(url_for('view_block_assignments', block_id=block_id))


@app.route('/assignments/bulk-add/<int:block_id>', methods=['POST'])
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
    
    return redirect(url_for('view_block_assignments', block_id=block_id))


# Automated Friday Send Route
@app.route('/send-friday-evaluations', methods=['GET', 'POST'])
@login_required
def send_friday_evaluations():
    """Send evaluations for all active assignments this Friday"""
    if request.method == 'POST':
        today = datetime.now().date()
        
        # Get all active rotation blocks
        active_blocks = RotationBlock.query.filter(
            RotationBlock.start_date <= today,
            RotationBlock.end_date >= today
        ).all()
        
        success_count = 0
        failed_count = 0
        already_sent_count = 0
        
        for block in active_blocks:
            # Get all assignments for this block
            assignments = RotationAssignment.query.filter_by(
                rotation_block_id=block.id,
                send_on_fridays=True
            ).all()
            
            for assignment in assignments:
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
                        failed_count += 1
        
        message = f'Sent {success_count} evaluations'
        if failed_count > 0:
            message += f', {failed_count} failed'
        if already_sent_count > 0:
            message += f', {already_sent_count} already sent today'
        
        flash(message, 'success' if failed_count == 0 else 'warning')
        return redirect(url_for('tracking'))
    
    # GET request - show preview
    today = datetime.now().date()
    active_blocks = RotationBlock.query.filter(
        RotationBlock.start_date <= today,
        RotationBlock.end_date >= today
    ).all()
    
    preview_assignments = []
    for block in active_blocks:
        assignments = RotationAssignment.query.filter_by(
            rotation_block_id=block.id,
            send_on_fridays=True
        ).all()
        
        for assignment in assignments:
            if assignment.last_sent != today:  # Not already sent today
                preview_assignments.append({
                    'assignment': assignment,
                    'fellow': Fellow.query.get(assignment.fellow_id),
                    'survey': Survey.query.get(assignment.survey_id),
                    'block': block
                })
    
    return render_template('send_friday_evaluations.html', 
                         preview_assignments=preview_assignments,
                         is_friday=today.weekday() == 4)


@app.route('/tracking')
@login_required
def tracking():
    page = request.args.get('page', 1, type=int)
    evaluations = Evaluation.query.order_by(Evaluation.sent_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    return render_template('tracking.html', evaluations=evaluations)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Handle password change
        if 'current_password' in request.form:
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if not current_user.check_password(current_password):
                flash('Current password is incorrect', 'error')
            elif new_password != confirm_password:
                flash('New passwords do not match', 'error')
            else:
                current_user.set_password(new_password)
                db.session.commit()
                flash('Password updated successfully!', 'success')
        
        return redirect(url_for('settings'))
    
    surveys_count = Survey.query.filter_by(active=True).count()
    
    return render_template('settings.html', 
                         twilio_configured=bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN),
                         surveys_count=surveys_count)


@app.route('/api/test-sms', methods=['POST'])
@login_required
def test_sms():
    """API endpoint to send a test SMS"""
    data = request.get_json()
    phone_number = data.get('phone_number')
    survey_id = data.get('survey_id')
    
    if not phone_number:
        return jsonify({'success': False, 'error': 'Phone number required'}), 400
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Get survey if specified
        if survey_id:
            survey = Survey.query.get(survey_id)
            if survey:
                message_body = f"Test message: {survey.name} - {survey.survey_link}"
            else:
                message_body = "Test message from Fellowship Evaluation System"
        else:
            message_body = "Test message from Fellowship Evaluation System"
        
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=format_phone_number(phone_number)
        )
        return jsonify({'success': True, 'message_sid': message.sid})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# CLI Commands for initialization
@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized!")


@app.cli.command()
def create_admin():
    """Create an admin user"""
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    email = input("Enter admin email (optional): ")
    
    user = User(username=username, email=email if email else None)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    print(f"Admin user '{username}' created successfully!")


if __name__ == '__main__':
    app.run(debug=True)
