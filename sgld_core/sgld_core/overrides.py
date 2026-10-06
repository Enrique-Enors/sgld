import frappe
from frappe.handler import upload_file as original_upload_file

@frappe.whitelist(allow_guest=True)
def custom_upload_file():
    # If the user is Guest and no doctype is provided, we assume it's for the public Web Form
    # This bypasses the 'None Doctype' block.
    if frappe.session.user == "Guest" and not frappe.form_dict.get("doctype"):
        frappe.form_dict.doctype = "Tramite Ciudadano"
        # We also need to temporarily inject the allowed doctype just in case the backend checks it again
        frappe.form_dict.is_private = 0
    return original_upload_file()
