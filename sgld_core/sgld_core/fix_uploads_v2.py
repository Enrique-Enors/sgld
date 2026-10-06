import frappe

def execute():
    try:
        sys_settings = frappe.get_doc("System Settings")
        sys_settings.allow_guests_to_upload_files = 1
        # Set allowed doctype, each on new line if multiple
        sys_settings.allowed_doctypes_for_guest_uploads = "Tramite Ciudadano"
        sys_settings.save(ignore_permissions=True)
        frappe.db.commit()
        print("Guest uploads properly enabled!")
    except Exception as e:
        print(f"Error: {e}")
