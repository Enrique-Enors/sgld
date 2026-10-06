import os
import frappe

def execute():
    app_path = frappe.get_app_path("sgld_core")
    overrides_path = os.path.join(app_path, "overrides.py")
    
    with open(overrides_path, "w", encoding="utf-8") as f:
        f.write('''import frappe
from frappe.handler import upload_file as original_upload_file

@frappe.whitelist(allow_guest=True)
def custom_upload_file():
    # Bypass Frappe 15 Guest Upload strict validations for Web Forms
    if frappe.session.user == "Guest":
        if not frappe.form_dict.get("doctype"):
            frappe.form_dict.doctype = "Tramite Ciudadano"
        if not frappe.form_dict.get("docname"):
            frappe.form_dict.docname = "nuevo-tramite-borrador"
            
        frappe.form_dict.is_private = 0

    return original_upload_file()
''')
    print("overrides.py updated successfully!")
