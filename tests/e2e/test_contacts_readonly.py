import pytest


def test_readonly_can_view_contacts(authenticated_readonly_page):
    """Test read-only user can view contacts on dashboard."""
    page = authenticated_readonly_page

    # Check that contact table exists with data
    table = page.query_selector('table')
    assert table is not None
    rows = page.query_selector_all('tbody tr')
    assert len(rows) > 0


def test_readonly_no_add_button(authenticated_readonly_page):
    """Test 'Add New Contact' button is NOT visible for read-only user."""
    page = authenticated_readonly_page

    add_button = page.query_selector('button:has-text("+ Add New Contact")')
    assert add_button is None


def test_readonly_no_edit_buttons(authenticated_readonly_page):
    """Test Edit buttons are NOT visible for read-only user."""
    page = authenticated_readonly_page

    edit_buttons = page.query_selector_all('button:has-text("Edit")')
    assert len(edit_buttons) == 0


def test_readonly_no_delete_buttons(authenticated_readonly_page):
    """Test Delete buttons are NOT visible for read-only user."""
    page = authenticated_readonly_page

    delete_buttons = page.query_selector_all('button:has-text("Delete")')
    assert len(delete_buttons) == 0


def test_readonly_cannot_access_add_form_directly(authenticated_readonly_page):
    """Test read-only user cannot access /contact/add directly."""
    page = authenticated_readonly_page

    page.goto("http://localhost:5000/contact/add", wait_until="load")

    # Should redirect back to dashboard or be on different page
    assert "dashboard" in page.url or "/contact/add" not in page.url


def test_readonly_cannot_access_edit_form_directly(authenticated_readonly_page):
    """Test read-only user cannot access /contact/<id>/edit directly."""
    page = authenticated_readonly_page

    page.goto("http://localhost:5000/contact/1/edit", wait_until="load")

    # Should redirect back to dashboard or be on different page
    assert "dashboard" in page.url or "/edit" not in page.url


def test_readonly_cannot_submit_delete_request(authenticated_readonly_page):
    """Test read-only user cannot access delete endpoint."""
    page = authenticated_readonly_page

    # Try to access the delete endpoint directly via GET (should fail)
    response = page.goto("http://localhost:5000/contact/1/delete", wait_until="domcontentloaded")

    # Either gets a 405 error (GET on POST-only endpoint) or is on dashboard
    status = response.status if response else 500
    assert status in [302, 405] or "dashboard" in page.url
