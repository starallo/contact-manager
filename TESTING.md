# Web Testing Automation Guide

This document describes the end-to-end (E2E) testing setup for the Contact Manager application using Playwright and pytest.

## Overview

The test suite provides comprehensive coverage of:
- **Authentication workflows** (login, logout, session management)
- **Admin CRUD operations** (create, read, update, delete contacts)
- **Permission enforcement** (read-only user access control)
- **Form validation** (field validation, submission, data persistence)

**Test Statistics:**
- 23 total tests
- 4 test files
- 100% pass rate

## Quick Start

### Prerequisites
- Python 3.11+
- Virtual environment activated: `source venv/bin/activate`
- Dependencies installed: `pip install -r requirements.txt`

### Run All Tests
```bash
pytest tests/e2e/ -v
```

### Run Specific Test File
```bash
pytest tests/e2e/test_auth.py -v
pytest tests/e2e/test_contacts_admin.py -v
pytest tests/e2e/test_contacts_readonly.py -v
pytest tests/e2e/test_forms.py -v
```

### Run Single Test
```bash
pytest tests/e2e/test_auth.py::test_login_admin_success -v
```

### Run Tests with Detailed Output
```bash
pytest tests/e2e/ -v --tb=short
```

## Project Structure

```
tests/
├── e2e/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures & Flask setup
│   ├── test_auth.py             # Authentication tests (5)
│   ├── test_contacts_admin.py   # Admin CRUD tests (6)
│   ├── test_contacts_readonly.py # Permission tests (7)
│   └── test_forms.py            # Form validation tests (5)
└── __init__.py

pytest.ini                        # Pytest configuration
requirements.txt                 # Project dependencies (includes Playwright)
TESTING.md                        # This file
```

## Test Categories

### 1. Authentication Tests (`test_auth.py`)

Tests user login/logout and session management.

| Test | Purpose |
|------|---------|
| `test_login_admin_success` | Admin login redirects to dashboard |
| `test_login_readonly_success` | Read-only user can login |
| `test_login_invalid_credentials` | Invalid login stays on login page |
| `test_logout_clears_session` | Logout clears session, redirects to login |
| `test_unauthenticated_access_to_dashboard_redirects` | Unauthenticated access is blocked |

**Test Credentials:**
- Admin: `bob` / `pwd`
- Read-only: `alice` / `pwd`

### 2. Admin Contact CRUD Tests (`test_contacts_admin.py`)

Tests contact management operations available to admin users.

| Test | Purpose |
|------|---------|
| `test_view_all_contacts_on_dashboard` | Admin can view all contacts |
| `test_add_new_contact_button_visible_for_admin` | Add button visible for admin |
| `test_add_new_contact_success` | New contact is saved to database |
| `test_edit_contact_button_visible_for_admin` | Edit buttons visible in table |
| `test_delete_contact_button_visible_for_admin` | Delete buttons visible in table |
| `test_edit_existing_contact` | Contact data can be modified and saved |

### 3. Read-Only Permission Tests (`test_contacts_readonly.py`)

Tests that read-only users cannot modify contacts.

| Test | Purpose |
|------|---------|
| `test_readonly_can_view_contacts` | Read-only user can view contacts |
| `test_readonly_no_add_button` | Add button hidden for read-only |
| `test_readonly_no_edit_buttons` | Edit buttons hidden for read-only |
| `test_readonly_no_delete_buttons` | Delete buttons hidden for read-only |
| `test_readonly_cannot_access_add_form_directly` | Direct /contact/add access redirected |
| `test_readonly_cannot_access_edit_form_directly` | Direct /contact/<id>/edit access redirected |
| `test_readonly_cannot_submit_delete_request` | Direct delete request is rejected |

### 4. Form Validation Tests (`test_forms.py`)

Tests form fields and validation.

| Test | Purpose |
|------|---------|
| `test_add_contact_form_requires_first_name` | First name field exists |
| `test_add_contact_form_requires_last_name` | Last name field exists |
| `test_add_contact_form_all_fields_filled` | Form submission with all fields works |
| `test_edit_contact_form_prefills_data` | Edit form pre-fills existing data |
| `test_cancel_button_returns_to_dashboard` | Cancel button discards changes |

## Test Fixtures

Fixtures are defined in `conftest.py` and provide reusable setup/teardown:

### `configure_app()` (session scope)
- Configures Flask app for testing (in-memory SQLite)
- Starts Flask development server on port 5000
- Creates test users and sample contacts
- Cleans up after all tests

### `browser()` (session scope)
- Creates a Playwright Chromium browser instance
- Shared across all tests for efficiency
- Closed after all tests complete

### `page()` (function scope)
- Creates a new browser page for each test
- Ensures test isolation
- Automatically closed after each test

### `authenticated_page()` (function scope)
- Provides a page already logged in as admin (bob)
- Navigates to dashboard
- Ready for admin-specific tests

### `authenticated_readonly_page()` (function scope)
- Provides a page already logged in as read-only user (alice)
- Navigates to dashboard
- Ready for permission-checking tests

## Test Data

The following test data is created for each test session:

**Users:**
```
Username: bob
Role: admin
Password: pwd

Username: alice
Role: read-only
Password: pwd
```

**Sample Contacts:**
```
1. John Doe (+1-555-0101)
2. Jane Smith (+1-555-0102)
3. Bob Johnson (+1-555-0103)
4. peppe lanzetta (+971655011301)
```

## Configuration Files

### `pytest.ini`
```ini
[pytest]
testpaths = tests/e2e
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### `requirements.txt`
```
Flask==3.0.0
Werkzeug==3.0.1
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
pytest==7.4.3
pytest-asyncio==0.21.1
playwright==1.40.0
```

## Running Tests in Different Modes

### Verbose Output
```bash
pytest tests/e2e/ -vv
```

### Show Print Statements
```bash
pytest tests/e2e/ -v -s
```

### Stop on First Failure
```bash
pytest tests/e2e/ -v -x
```

### Run Last Failed Tests
```bash
pytest tests/e2e/ --lf
```

### Generate HTML Report
```bash
pytest tests/e2e/ --html=report.html --self-contained-html
```

## Troubleshooting

### Tests Hanging
If tests hang when running, check:
1. Flask server is not already running on port 5000
2. Browser process is not stuck: `ps aux | grep chrome`
3. Increase timeout: `pytest tests/e2e/ --timeout=60`

### Browser Not Found
If you see "Executable doesn't exist" error:
```bash
source venv/bin/activate
playwright install chromium
```

### Database Conflicts
Tests use an in-memory SQLite database that's reset between sessions. If you see unique constraint errors:
1. Ensure only one pytest session is running
2. Clear pytest cache: `pytest --cache-clear`

### Import Errors
Make sure Flask app can be imported:
```bash
python3 -c "from app import app, db; print('OK')"
```

## CI/CD Integration

To run tests in CI/CD pipeline:

```bash
#!/bin/bash
set -e

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/e2e/ -v --tb=short --junit-xml=results.xml

# Generate coverage
pytest tests/e2e/ --cov=. --cov-report=html
```

## Extending the Tests

### Adding a New Test

1. Create test function in appropriate file:
```python
def test_new_feature(authenticated_page):
    """Test description."""
    page = authenticated_page
    page.goto("http://localhost:5000/path")
    assert "expected" in page.content()
```

2. Run the test:
```bash
pytest tests/e2e/test_file.py::test_new_feature -v
```

### Common Playwright Methods

```python
# Navigation
page.goto("url")
page.wait_for_url("url_pattern")

# Interaction
page.fill('input[name="field"]', "value")
page.click('button:has-text("text")')
page.select('select[name="field"]', "option")

# Assertion
assert "text" in page.content()
assert page.url == "expected_url"

# Waiting
page.wait_for_selector('element')
page.wait_for_load_state('load')
```

## Performance

Test execution times:
- Full suite: ~13 seconds
- Single test: ~2-5 seconds

Time is spent:
1. Flask server startup (~2s)
2. Browser initialization (~1s per test)
3. User interactions & assertions (~1s per test)

## Maintenance

### Monthly Tasks
- [ ] Update Playwright: `pip install --upgrade playwright`
- [ ] Review failed tests and update as needed
- [ ] Check for deprecated Flask-SQLAlchemy patterns

### When Application Changes
- [ ] Update test URLs if routes change
- [ ] Update selectors if HTML structure changes
- [ ] Add new tests for new features
- [ ] Update test credentials if user management changes

## Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/testing/)

## Contact

For questions or issues with the test suite, check the app logs:
```bash
tail -f /tmp/flask.log
```

---

**Last Updated:** 2026-10-16  
**Test Count:** 23  
**Pass Rate:** 100%
