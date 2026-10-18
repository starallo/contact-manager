import csv
import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask_migrate import Migrate
from models import db, User, Contact

app = Flask(__name__)

# SQLAlchemy Configuration - use absolute path for SQLite
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dev-secret-key-change-in-production'

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(DATA_DIR, 'users.csv')
CONTACTS_FILE = os.path.join(DATA_DIR, 'contacts.csv')
BACKUP_DIR = os.path.join(DATA_DIR, 'backup')


def migrate_csv_to_db():
    """Migrate data from CSV files to SQLite database on first run."""
    # Check if database already has data
    if db.session.query(User).first():
        return  # Database already populated

    # Migrate users
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    user = User(
                        id=int(row['id']),
                        username=row['username'],
                        password_hash=row['password_hash'],
                        role=row['role']
                    )
                    db.session.add(user)
            db.session.commit()
            print("✓ Migrated users from CSV")
        except Exception as e:
            print(f"Error migrating users: {e}")
            db.session.rollback()

    # Migrate contacts
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    contact = Contact(
                        id=int(row['id']),
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        mobile_phone=row['mobile_phone']
                    )
                    db.session.add(contact)
            db.session.commit()
            print("✓ Migrated contacts from CSV")
        except Exception as e:
            print(f"Error migrating contacts: {e}")
            db.session.rollback()

    # Archive CSV files
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    if os.path.exists(USERS_FILE):
        shutil.move(USERS_FILE, os.path.join(BACKUP_DIR, 'users.csv'))
        print(f"✓ Archived users.csv to {BACKUP_DIR}/")

    if os.path.exists(CONTACTS_FILE):
        shutil.move(CONTACTS_FILE, os.path.join(BACKUP_DIR, 'contacts.csv'))
        print(f"✓ Archived contacts.csv to {BACKUP_DIR}/")


def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# Initialize database on app startup
def init_db():
    """Initialize database on app startup."""
    db_path = os.path.join(DATA_DIR, 'app.db')
    with app.app_context():
        db.create_all()
        if not os.path.exists(db_path) or db.session.query(User).count() == 0:
            migrate_csv_to_db()

init_db()


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))

        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    contacts = Contact.query.all()
    return render_template('dashboard.html', contacts=[c.to_dict() for c in contacts])


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@app.route('/contact/add', methods=['GET', 'POST'])
@admin_required
def add_contact():
    if request.method == 'POST':
        contact = Contact(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            mobile_phone=request.form.get('mobile_phone')
        )
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('add_contact.html')


@app.route('/contact/<contact_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)

    if request.method == 'POST':
        contact.first_name = request.form.get('first_name')
        contact.last_name = request.form.get('last_name')
        contact.mobile_phone = request.form.get('mobile_phone')
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('edit_contact.html', contact=contact.to_dict())


@app.route('/contact/<contact_id>/delete', methods=['POST'])
@admin_required
def delete_contact_route(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
