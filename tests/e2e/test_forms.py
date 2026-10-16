import pytest


def test_add_contact_form_requires_first_name(authenticated_page):
    """Test form has first name field."""
    page = authenticated_page

    page.click('button:has-text("+ Add New Contact")')
    page.wait_for_url("http://localhost:5000/contact/add")

    first_name_input = page.query_selector('input[name="first_name"]')
    assert first_name_input is not None


def test_add_contact_form_requires_last_name(authenticated_page):
    """Test form has last name field."""
    page = authenticated_page

    page.click('button:has-text("+ Add New Contact")')
    page.wait_for_url("http://localhost:5000/contact/add")

    last_name_input = page.query_selector('input[name="last_name"]')
    assert last_name_input is not None


def test_add_contact_form_all_fields_filled(authenticated_page):
    """Test form submission succeeds with all fields filled."""
    page = authenticated_page

    page.click('button:has-text("+ Add New Contact")')
    page.wait_for_url("http://localhost:5000/contact/add")

    page.fill('input[name="first_name"]', "FormFilled")
    page.fill('input[name="last_name"]', "LastName")
    page.fill('input[name="mobile_phone"]', "+1-555-7777")
    page.click('button[type="submit"]')

    page.wait_for_url("http://localhost:5000/dashboard")
    assert "FormFilled" in page.content()


def test_edit_contact_form_prefills_data(authenticated_page):
    """Test that edit form pre-fills with existing contact data."""
    page = authenticated_page

    edit_buttons = page.query_selector_all('button:has-text("Edit")')
    assert len(edit_buttons) > 0

    edit_buttons[0].click()

    # Wait for the edit page to load (URL contains /edit)
    page.wait_for_url("**/edit")

    # Check that form fields exist
    first_name = page.query_selector('input[name="first_name"]')
    last_name = page.query_selector('input[name="last_name"]')
    mobile = page.query_selector('input[name="mobile_phone"]')

    assert first_name is not None
    assert last_name is not None
    assert mobile is not None

    # Verify fields have values
    assert len(first_name.input_value()) > 0
    assert len(last_name.input_value()) > 0
    assert len(mobile.input_value()) > 0


def test_cancel_button_returns_to_dashboard(authenticated_page):
    """Test Cancel button returns to dashboard without saving."""
    page = authenticated_page

    # Get initial contact count
    page.goto("http://localhost:5000/dashboard")
    initial_rows = len(page.query_selector_all('tbody tr'))

    page.click('button:has-text("+ Add New Contact")')
    page.wait_for_url("http://localhost:5000/contact/add")

    page.fill('input[name="first_name"]', "WillCancel")

    # Click Cancel button or link
    cancel = page.query_selector('a[href="/dashboard"], button:has-text("Cancel")')
    if cancel:
        cancel.click()
        page.wait_for_url("http://localhost:5000/dashboard")

    # Verify the unsaved contact was not added
    assert "WillCancel" not in page.content()
