import frappe

def execute():
    try:
        # Enable Guest Uploads and set Max File Size
        sys_settings = frappe.get_doc("System Settings")
        sys_settings.allow_guest_to_upload_files = 1
        sys_settings.max_file_size = 31457280  # 30 MB
        sys_settings.save(ignore_permissions=True)
        frappe.db.commit()
        print("Guest uploads enabled and max file size set to 30MB.")
    except Exception as e:
        print(f"Error setting sys settings: {e}")

    try:
        errors = frappe.db.sql("SELECT method, error FROM `tabError Log` ORDER BY creation DESC LIMIT 5", as_dict=True)
        for e in errors:
            print(f"Method: {e.get('method')}")
            print(f"Error: {e.get('error')[:200]}")
            print("---")
    except Exception as e:
        print(f"Error fetching logs: {e}")
