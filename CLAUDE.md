# Contact Manager - Claude Code Guide

## Project Overview

**Contact Manager** is a Flask web application for managing contacts with role-based access control and comprehensive E2E testing.

- **Status:** ✅ Complete with 23 automated tests (100% pass rate)
- **Tech Stack:** Flask 3.0, SQLAlchemy, Playwright, pytest
- **Test Coverage:** Authentication, CRUD, permissions, form validation

## Quick Start

### Setup
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Run Application
```bash
python3 app.py
# Visit http://localhost:5000
```

### Run Tests
```bash
pytest tests/e2e/ -v              # Run all tests
pytest tests/e2e/test_auth.py -v  # Run specific file
pytest tests/e2e/ -v -s           # Show print statements
```

## Project Structure

```
.
├── app.py                 # Main Flask app with routes
├── models.py              # SQLAlchemy models (User, Contact)
├── requirements.txt       # Python dependencies
├── pytest.ini             # Test configuration
├── CLAUDE.md             # This file
├── README.md             # Project overview
├── TESTING.md            # Testing guide (400+ lines)
├── FEATURES.md           # Feature roadmap
│
├── templates/            # HTML templates
│   ├── base.html         # Base with dark mode
│   ├── login.html        # Login page
│   ├── dashboard.html    # Contact listing
│   ├── add_contact.html  # Add form
│   └── edit_contact.html # Edit form
│
├── tests/e2e/            # E2E test suite
│   ├── conftest.py       # Flask + Playwright fixtures
│   ├── test_auth.py      # Authentication (5 tests)
│   ├── test_contacts_admin.py      # Admin CRUD (6 tests)
│   ├── test_contacts_readonly.py   # Permissions (7 tests)
│   └── test_forms.py     # Form validation (5 tests)
│
└── backup/               # Original CSV data
    ├── users.csv
    └── contacts.csv
```

## Key Commands

### Testing
```bash
# Run all tests
pytest tests/e2e/ -v

# Run with coverage
pytest tests/e2e/ --cov=. --cov-report=html

# Run specific test
pytest tests/e2e/test_auth.py::test_login_admin_success -v

# Stop on first failure
pytest tests/e2e/ -x -v
```

### Application
```bash
# Start dev server
python3 app.py

# Access login page
# http://localhost:5000

# Demo credentials
# Admin: bob / pwd
# Read-only: alice / pwd
```

### Git
```bash
# View commits
git log --oneline

# Check status
git status

# Make changes
git add .
git commit -m "Description"
git push origin main
```

## Architecture

### Authentication Flow
1. Login form → `POST /login`
2. Username/password validated via `check_password_hash`
3. Session created with user_id, username, role
4. Redirected to dashboard

### Authorization
- **Admin**: Can view, add, edit, delete contacts
- **Read-only**: Can only view contacts
- Enforced via decorators: `@login_required`, `@admin_required`
- UI elements hidden based on role (edit/delete buttons)

### Database
- **SQLite** (`app.db`): File-based database
- **Models**: User, Contact (defined in `models.py`)
- **ORM**: Flask-SQLAlchemy with SQLAlchemy queries
- **Test DB**: In-memory SQLite for test isolation

### Testing Strategy
- **Fixtures**: Flask app, Playwright browser, authenticated pages
- **Isolation**: Each test gets fresh in-memory database
- **Scope**: Session (server/browser), Function (page/data)
- **Coverage**: Auth, CRUD, permissions, forms

## Common Workflows

### Adding a New Feature
1. **Plan**: Update FEATURES.md with description
2. **Code**: Add route in app.py, template, or update models.py
3. **Test**: Add test case in appropriate tests/e2e/test_*.py file
4. **Verify**: Run `pytest tests/e2e/ -v` to ensure nothing broke
5. **Document**: Update README.md or TESTING.md if needed
6. **Commit**: `git add .` → `git commit -m "Add feature X"`

### Debugging a Test
```bash
# Run with full output
pytest tests/e2e/test_file.py::test_name -vv -s

# Show last failed
pytest tests/e2e/ --lf -v

# Generate HTML report
pytest tests/e2e/ --html=report.html --self-contained-html
```

### Modifying a Route
1. Update route in `app.py`
2. Update corresponding template if needed
3. Check which tests might be affected
4. Run affected tests: `pytest tests/e2e/test_auth.py -v`
5. Verify in browser: `python3 app.py` → http://localhost:5000

### Updating Database Schema
1. Modify model in `models.py`
2. Create migration: `flask db migrate -m "description"`
3. Apply migration: `flask db upgrade`
4. Tests use in-memory DB, so no migration needed there
5. Update FEATURES.md

## Test Data

### Users (Created per test session)
```
bob (admin):     password="pwd"
alice (read-only): password="pwd"
```

### Contacts (Sample data for testing)
```
1. John Doe (+1-555-0101)
2. Jane Smith (+1-555-0102)
3. Bob Johnson (+1-555-0103)
4. peppe lanzetta (+971655011301)
```

## Important Files

| File | Purpose | Edit When |
|------|---------|-----------|
| `app.py` | Routes, auth, logic | Adding endpoints |
| `models.py` | Database schemas | Changing data structure |
| `requirements.txt` | Dependencies | Adding packages |
| `tests/e2e/conftest.py` | Test fixtures | Changing test setup |
| `pytest.ini` | Test config | Changing test discovery |
| `TESTING.md` | Testing docs | Updating test guide |

## Development Guidelines

### Before Committing
- [ ] All tests pass: `pytest tests/e2e/ -v`
- [ ] Tested in browser: `python3 app.py`
- [ ] No debug prints left in code
- [ ] Updated FEATURES.md with progress
- [ ] Commit message is descriptive

### Code Style
- Use snake_case for Python functions/variables
- Use kebab-case for file names (unless Python module)
- Keep functions focused and under 50 lines
- Add docstrings to test functions
- Use descriptive names (no single letters except i, j, k for loops)

### Testing
- Each test should be independent (no test interdependencies)
- Use `authenticated_page` fixture for tests requiring login
- Assert one thing per test (or closely related things)
- Test both happy path and error cases

## Troubleshooting

### Tests fail with timeout
```bash
# Increase timeout
pytest tests/e2e/ --timeout=60 -v

# Or check if Flask server is already running
lsof -i :5000  # See what's using port 5000
pkill -f flask  # Kill Flask process
```

### Import errors
```bash
# Verify app imports correctly
python3 -c "from app import app, db; print('OK')"

# Check if venv is activated
source venv/bin/activate
```

### Browser issues
```bash
# Kill stuck Chrome processes
pkill -f chromium

# Reinstall Playwright
playwright install chromium
```

### Database issues
```bash
# Delete SQLite database and recreate
rm app.db
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## Documentation

- **README.md** - Project overview, features, user roles
- **TESTING.md** - Comprehensive testing guide (400+ lines)
- **tests/README.md** - Quick reference for test commands
- **FEATURES.md** - Feature roadmap and development log

## GitHub

**Repository**: https://github.com/starallo/contact-manager

```bash
# Clone
git clone https://github.com/starallo/contact-manager.git

# Push changes
git add .
git commit -m "Description"
git push origin main
```

## Next Steps

### Phase 2 Features (See FEATURES.md)
- Search/filter contacts
- Sorting by column
- Pagination
- CSV/JSON export

### Testing Enhancements
- Add visual regression testing
- Performance testing for large contact lists
- Load testing with multiple concurrent users

### Infrastructure
- CI/CD pipeline (GitHub Actions)
- Automated testing on push
- Code coverage reporting
- Automated deployment

## Notes

- Application uses **development Flask server** (not production-ready)
- Tests use **in-memory SQLite** for speed and isolation
- Dark mode is persistent via **localStorage**
- Passwords are hashed with **PBKDF2-SHA256** (Werkzeug)
- Sessions are **server-side** Flask sessions

---

**Last Updated**: 2026-10-18  
**Test Status**: ✅ 23/23 passing  
**Contributors**: Claude, iperdrummer@gmail.com
