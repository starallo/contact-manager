import pytest


def test_login_admin_success(page):
    """Test successful login with admin credentials."""
    page.goto("http://localhost:5000/login")
    page.fill('input[name="username"]', "bob")
    page.fill('input[name="password"]', "pwd")
    page.click('button[type="submit"]')

    page.wait_for_url("http://localhost:5000/dashboard")
    assert "bob" in page.content()
    assert "Admin" in page.content() or "admin" in page.content()


def test_login_readonly_success(page):
    """Test successful login with read-only credentials."""
    page.goto("http://localhost:5000/login")
    page.fill('input[name="username"]', "alice")
    page.fill('input[name="password"]', "pwd")
    page.click('button[type="submit"]')

    page.wait_for_url("http://localhost:5000/dashboard")
    assert "alice" in page.content()
    assert "Read" in page.content() or "read" in page.content()


def test_login_invalid_credentials(page):
    """Test login with invalid credentials stays on login page."""
    page.goto("http://localhost:5000/login")
    page.fill('input[name="username"]', "invalid")
    page.fill('input[name="password"]', "wrong")
    page.click('button[type="submit"]')

    # Should stay on login page
    assert page.url == "http://localhost:5000/login"


def test_logout_clears_session(authenticated_page):
    """Test logout clears session and redirects to login."""
    page = authenticated_page

    page.click('a:has-text("Logout")')
    page.wait_for_url("http://localhost:5000/login")

    assert page.url == "http://localhost:5000/login"


def test_unauthenticated_access_to_dashboard_redirects(page):
    """Test accessing dashboard without auth redirects to login."""
    page.goto("http://localhost:5000/dashboard")

    page.wait_for_url("http://localhost:5000/login")
    assert page.url == "http://localhost:5000/login"
