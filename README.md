# Contact Manager

A web-based contact management application with SQLite database backend and role-based access control.

## Features

- **User Authentication**: Secure login with password hashing (PBKDF2-SHA256)
- **Role-Based Access**: Admin and read-only user roles
- **Contact Management**: View, add, edit, and delete contacts (admin only)
- **SQLite Database**: Lightweight, file-based database with ACID transactions
- **Dark Mode**: Toggle between light and dark themes with system preference detection
- **Responsive UI**: Modern, gradient-based design with smooth transitions

## Quick Start

### Prerequisites
- Python 3.7+
- Flask 3.0+
- Werkzeug 3.0+

### Installation

1. Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

2. Run the application:
```bash
python3 app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

### Demo Credentials

- **Admin Account**: Username: `bob`, Password: `pwd`
- **Read-Only Account**: Username: `alice`, Password: `pwd`

## Project Structure

```
.
├── app.py                 # Main Flask application with SQLAlchemy
├── models.py              # SQLAlchemy models (User, Contact)
├── app.db                 # SQLite database (auto-created)
├── requirements.txt       # Python dependencies
├── pytest.ini             # Pytest configuration
├── FEATURES.md            # Feature tracker and roadmap
├── README.md              # This file
├── TESTING.md             # Testing documentation
├── templates/
│   ├── base.html          # Base template with dark mode support
│   ├── login.html         # Login page
│   ├── dashboard.html     # Main contact listing
│   ├── add_contact.html   # Add contact form
│   └── edit_contact.html  # Edit contact form
├── tests/
│   ├── e2e/
│   │   ├── conftest.py    # Pytest fixtures & Flask setup
│   │   ├── test_auth.py   # Authentication tests
│   │   ├── test_contacts_admin.py     # Admin CRUD tests
│   │   ├── test_contacts_readonly.py  # Permission tests
│   │   └── test_forms.py  # Form validation tests
│   └── __init__.py
├── backup/                # Archived CSV files (original data)
│   ├── users.csv
│   └── contacts.csv
└── venv/                  # Python virtual environment
```

## User Roles

### Admin
- View all contacts
- Add new contacts
- Edit existing contacts
- Delete contacts

### Read-Only
- View contacts only
- No edit or delete permissions

## Data Storage

### SQLite Database (app.db)

**User Table:**
- `id`: User ID (Integer, Primary Key)
- `username`: Login username (String, Unique)
- `password_hash`: PBKDF2-SHA256 hashed password (String)
- `role`: User role - "admin" or "read_only" (String)

**Contact Table:**
- `id`: Contact ID (Integer, Primary Key)
- `first_name`: Contact's first name (String)
- `last_name`: Contact's last name (String)
- `mobile_phone`: Contact's phone number (String)

**Backup:** Original CSV files preserved in `backup/` folder for reference

## Testing

The application includes a comprehensive end-to-end test suite using Playwright and pytest.

### Run Tests
```bash
pytest tests/e2e/ -v
```

### Test Coverage
- **23 tests** covering authentication, CRUD operations, permissions, and forms
- Tests both admin and read-only user workflows
- Tests form validation and data persistence
- **100% pass rate**

For detailed testing documentation, see [TESTING.md](TESTING.md).

### Key Test Features
- Automated browser testing with Playwright
- Flask test fixtures for isolated testing
- In-memory SQLite database for fast test execution
- Session management and permission verification
- Form submission and validation testing

## Development

See [FEATURES.md](FEATURES.md) for the complete feature roadmap and development log.

### Technology Stack
- **Backend:** Flask 3.0 with Flask-SQLAlchemy ORM
- **Database:** SQLite 3 (file-based)
- **Authentication:** Werkzeug security utilities (PBKDF2-SHA256)
- **Frontend:** HTML5, CSS3 with CSS variables for theming
- **Session Management:** Flask built-in sessions

### Adding Features
1. Update database models in `models.py` if needed
2. Modify `app.py` for backend changes (use ORM queries)
3. Add/update templates in `templates/` as needed
4. Test with both user roles (admin & read_only)
5. Update `FEATURES.md` with progress

### Database Migrations
Flask-Migrate is configured for schema changes:
```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade
```

## Security Notes

⚠️ **Development Only** - This application is designed for development/demonstration purposes.

### Current Implementation
- ✅ SQLite database with ACID transactions
- ✅ PBKDF2-SHA256 password hashing (Werkzeug)
- ✅ Session-based authentication
- ✅ Role-based access control (admin/read_only)

### Before Production Deployment
- [ ] Change the `secret_key` in `app.py` to a secure random value
- [ ] Enable HTTPS/SSL (use reverse proxy like nginx)
- [ ] Implement CSRF protection (Flask-WTF)
- [ ] Add input validation and sanitization
- [ ] Consider moving to PostgreSQL for multi-user environments
- [ ] Add rate limiting on login endpoint
- [ ] Implement logging and monitoring
- [ ] Regular security audits and dependency updates
- [ ] Database backups and recovery procedures
- [ ] Add CORS headers if API endpoints are added

## Future Enhancements

### Planned Features (see [FEATURES.md](FEATURES.md) for detailed roadmap)
- **Phase 2:** Search/filter, sorting, pagination, CSV/JSON export
- **Phase 3:** User management interface, password change, registration flow
- **Phase 4:** Contact categories, favorites, detailed notes, email notifications
- **Phase 5:** Bulk operations, contact history, backup/restore, PDF export
- **Phase 6:** Quick-view modals, inline editing, toast notifications
- **Phase 7:** Caching, rate limiting, SSL/TLS, enhanced validation

### Database-Enabled Capabilities
With SQLite backend, the foundation is now in place for:
- Complex queries and filtering
- Proper transaction handling
- Data relationships (foreign keys)
- Efficient pagination
- Full-text search optimization

## Support

For issues or questions, refer to the FEATURES.md file for development status and planned improvements.
