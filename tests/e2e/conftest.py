import os
import time
import pytest
from threading import Thread
from playwright.sync_api import sync_playwright
from werkzeug.security import generate_password_hash
from app import app as flask_app, db, User, Contact


@pytest.fixture(scope="session", autouse=True)
def configure_app():
    """Configure app for testing and start server."""
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["TESTING"] = True
    flask_app.config["WTF_CSRF_ENABLED"] = False

    # Initialize the database
    with flask_app.app_context():
        db.drop_all()
        db.create_all()

        # Create test users (the CSV migration won't work with in-memory db)
        existing_bob = User.query.filter_by(username="bob").first()
        if not existing_bob:
            admin_user = User(username="bob", password_hash=generate_password_hash("pwd"), role="admin")
            db.session.add(admin_user)

        existing_alice = User.query.filter_by(username="alice").first()
        if not existing_alice:
            readonly_user = User(username="alice", password_hash=generate_password_hash("pwd"), role="read-only")
            db.session.add(readonly_user)

        db.session.commit()

        # Create test contacts
        if Contact.query.count() == 0:
            contacts = [
                Contact(first_name="John", last_name="Doe", mobile_phone="+1-555-0101"),
                Contact(first_name="Jane", last_name="Smith", mobile_phone="+1-555-0102"),
                Contact(first_name="Bob", last_name="Johnson", mobile_phone="+1-555-0103"),
                Contact(first_name="peppe", last_name="lanzetta", mobile_phone="+971655011301"),
            ]
            for contact in contacts:
                db.session.add(contact)
            db.session.commit()

    # Start Flask server in background thread
    server_thread = Thread(
        target=lambda: flask_app.run(port=5000, debug=False, use_reloader=False),
        daemon=True
    )
    server_thread.start()
    time.sleep(2)

    yield

    # Cleanup after tests
    with flask_app.app_context():
        db.drop_all()


@pytest.fixture(scope="session")
def browser():
    """Create a Playwright browser instance for the session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Create a new browser page for each test."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def authenticated_page(page):
    """Provide a page authenticated as admin user."""
    page.goto("http://localhost:5000/login")
    page.fill('input[name="username"]', "bob")
    page.fill('input[name="password"]', "pwd")
    page.click('button[type="submit"]')
    page.wait_for_url("http://localhost:5000/dashboard")
    return page


@pytest.fixture
def authenticated_readonly_page(page):
    """Provide a page authenticated as read-only user."""
    page.goto("http://localhost:5000/login")
    page.fill('input[name="username"]', "alice")
    page.fill('input[name="password"]', "pwd")
    page.click('button[type="submit"]')
    page.wait_for_url("http://localhost:5000/dashboard")
    return page
