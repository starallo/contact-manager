import pytest


def test_view_all_contacts_on_dashboard(authenticated_page):
    """Test admin can view all contacts on dashboard."""
    page = authenticated_page

    # Check that at least the initial contacts exist
    assert "Doe" in page.content() or "Smith" in page.content()


def test_add_new_contact_button_visible_for_admin(authenticated_page):
    """Test 'Add New Contact' button is visible for admin."""
    page = authenticated_page

    add_button = page.query_selector('button:has-text("+ Add New Contact")')
    assert add_button is not None
    assert add_button.is_visible()


def test_add_new_contact_success(authenticated_page):
    """Test adding a new contact with valid data."""
    page = authenticated_page

    page.click('button:has-text("+ Add New Contact")')
    page.wait_for_url("http://localhost:5000/contact/add")

    page.fill('input[name="first_name"]', "NewAdmin")
    page.fill('input[name="last_name"]', "Contact")
    page.fill('input[name="mobile_phone"]', "+1-555-9999")
    page.click('button[type="submit"]')

    page.wait_for_url("http://localhost:5000/dashboard")
    assert "NewAdmin" in page.content()
    assert "Contact" in page.content()


def test_edit_contact_button_visible_for_admin(authenticated_page):
    """Test Edit buttons are visible for admin on each contact row."""
    page = authenticated_page

    edit_buttons = page.query_selector_all('button:has-text("Edit")')
    assert len(edit_buttons) > 0
    assert all(btn.is_visible() for btn in edit_buttons)


def test_delete_contact_button_visible_for_admin(authenticated_page):
    """Test Delete buttons are visible for admin on each contact row."""
    page = authenticated_page

    delete_buttons = page.query_selector_all('button:has-text("Delete")')
    assert len(delete_buttons) > 0
    assert all(btn.is_visible() for btn in delete_buttons)


def test_edit_existing_contact(authenticated_page):
    """Test editing an existing contact."""
    page = authenticated_page

    # Click first Edit button
    edit_buttons = page.query_selector_all('button:has-text("Edit")')
    edit_buttons[0].click()

    page.wait_for_url("**/edit")

    # Check that form is pre-filled
    first_name_input = page.query_selector('input[name="first_name"]')
    assert first_name_input is not None
    current_value = first_name_input.input_value()

    # Edit the contact
    page.fill('input[name="first_name"]', "Updated" + current_value)
    page.click('button[type="submit"]')

    page.wait_for_url("http://localhost:5000/dashboard")
    assert "Updated" in page.content()
