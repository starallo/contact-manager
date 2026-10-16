# E2E Test Suite - Quick Reference

## Running Tests

```bash
# Run all tests
pytest tests/e2e/ -v

# Run specific test file
pytest tests/e2e/test_auth.py -v

# Run single test
pytest tests/e2e/test_auth.py::test_login_admin_success -v

# Run with short traceback
pytest tests/e2e/ -v --tb=short

# Run with detailed output
pytest tests/e2e/ -vv -s
```

## Test Organization

| File | Tests | Purpose |
|------|-------|---------|
| `test_auth.py` | 5 | Login, logout, session management |
| `test_contacts_admin.py` | 6 | Add, edit, delete, view contacts (admin) |
| `test_contacts_readonly.py` | 7 | Permission enforcement, access control |
| `test_forms.py` | 5 | Form fields, validation, submission |

## Test Credentials

```
Admin User:
  Username: bob
  Password: pwd

Read-Only User:
  Username: alice
  Password: pwd
```

## Sample Contacts

Four contacts are created for each test session:
- John Doe (+1-555-0101)
- Jane Smith (+1-555-0102)
- Bob Johnson (+1-555-0103)
- peppe lanzetta (+971655011301)

## Fixtures Available

```python
# Browser and page fixtures
page              # New browser page for each test
browser           # Shared browser instance (session scope)

# Authenticated pages
authenticated_page           # Logged in as admin (bob)
authenticated_readonly_page  # Logged in as read-only (alice)
```

## Writing a Test

```python
def test_example(authenticated_page):
    """Test description."""
    page = authenticated_page
    
    # Navigate
    page.goto("http://localhost:5000/dashboard")
    
    # Interact
    page.fill('input[name="field"]', "value")
    page.click('button:has-text("Click")')
    
    # Assert
    assert "expected text" in page.content()
```

## Common Playwright Methods

```python
# Navigation
page.goto(url)
page.wait_for_url(pattern)
page.wait_for_load_state("load")

# Interaction
page.fill('selector', value)
page.click(selector)
page.check(selector)
page.select('select', option)

# Query
page.query_selector(selector)
page.query_selector_all(selector)
page.content()
page.url

# Wait
page.wait_for_selector(selector)
page.wait_for_timeout(milliseconds)
```

## Selectors

```python
# By text (Playwright shorthand)
'button:has-text("Click Me")'
'a:has-text("Link Text")'

# Standard CSS
'input[name="username"]'
'input[type="submit"]'
'button[class="btn"]'

# ID and class
'#element-id'
'.element-class'

# Combinations
'form input[name="first_name"]'
'table tbody tr'
```

## Troubleshooting

**Tests hang?**
```bash
# Kill any stuck Chrome processes
pkill -f chromium

# Run with timeout
pytest tests/e2e/ --timeout=60
```

**Browser not found?**
```bash
source venv/bin/activate
playwright install chromium
```

**Need to see what the browser is doing?**
```bash
# Run test in headed mode (if supported in conftest)
# Tests use headless=True by default for CI/CD
```

## Test Results

Latest run:
```
========================== 23 passed in 12.73s ==========================
✅ All authentication tests pass
✅ All admin CRUD tests pass
✅ All permission enforcement tests pass
✅ All form validation tests pass
```

---

For detailed information, see [../TESTING.md](../TESTING.md)
