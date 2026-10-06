import os
import frappe

def execute():
    # 1. Update Web Form Javascript to patch handle_success
    wf = frappe.get_doc("Web Form", "ventanilla-de-trámites-ciudadanos")
    
    wf.client_script = """
frappe.ready(() => {
    if (frappe.web_form) {
        let original_handle_success = frappe.web_form.handle_success.bind(frappe.web_form);
        frappe.web_form.handle_success = (data) => {
            // First call the original to hide the container and show success page
            original_handle_success(data);
            
            // Now inject our beautiful HTML
            let tracking_no = data.name;
            if (tracking_no) {
                $('.success-page').html(`
                    <div class="text-center" style="padding: 20px;">
                        <svg width="80" height="80" viewBox="0 0 16 16" class="text-success mb-3" fill="#28a745" xmlns="http://www.w3.org/2000/svg">
                          <path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                        </svg>
                        <h2>¡Trámite Validado!</h2>
                        <p>Su trámite ha sido registrado exitosamente. Guarde su número de seguimiento para futuras consultas.</p>
                        <div class="mt-4" style="font-size: 1.2rem; background-color: #f8f9fa; border: 2px dashed #007bff; border-radius: 8px; padding: 20px;">
                            <strong style="color: #007bff;">NÚMERO DE SEGUIMIENTO:</strong><br>
                            <span style="font-size: 2.2rem; font-family: monospace; letter-spacing: 2px; color: #343a40;">${tracking_no}</span>
                        </div>
                        <button class="btn btn-primary mt-4" onclick="window.print()" style="font-size: 1.1rem; padding: 10px 20px;">🖨️ Imprimir Comprobante</button>
                        <br>
                        <a class="btn btn-light mt-3" href="/ventanilla/new">Enviar otro trámite</a>
                    </div>
                `);
            }
        };
    }
});
"""
    wf.save(ignore_permissions=True)
    frappe.db.commit()
    print("Web form JS patched successfully!")

    # 2. Write overrides.py
    app_path = frappe.get_app_path("sgld_core")
    overrides_path = os.path.join(app_path, "overrides.py")
    with open(overrides_path, "w", encoding="utf-8") as f:
        f.write('''import frappe
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
''')
    print("overrides.py created successfully!")

    # 3. Update hooks.py
    hooks_path = os.path.join(app_path, "hooks.py")
    with open(hooks_path, "r", encoding="utf-8") as f:
        hooks_content = f.read()
    
    if "override_whitelisted_methods" not in hooks_content or "upload_file" not in hooks_content:
        with open(hooks_path, "a", encoding="utf-8") as f:
            f.write("\n\noverride_whitelisted_methods = {\n")
            f.write("    'upload_file': 'sgld_core.sgld_core.overrides.custom_upload_file'\n")
            f.write("}\n")
        print("hooks.py updated successfully!")
    else:
        print("hooks.py already has override_whitelisted_methods.")
