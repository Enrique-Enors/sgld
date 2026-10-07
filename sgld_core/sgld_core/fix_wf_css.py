import frappe

def execute():
    try:
        # Fix Website Settings (Logo precedence)
        web_settings = frappe.get_doc("Website Settings")
        # Clear app_logo so brand_html takes over
        web_settings.app_logo = ""
        # The logo image
        img_src = "/files/image1.jpg"
        web_settings.brand_html = f'<div style="display:flex; align-items:center;"><img src="{img_src}" style="height:40px; margin-right:10px;"><span style="color: #008f39; font-weight: 800; font-size: 1.4rem; letter-spacing: -0.5px;">Concejo Municipal</span></div>'
        web_settings.save(ignore_permissions=True)

        # Fix Web Form CSS (Direct injection)
        wf = frappe.get_doc("Web Form", "ventanilla-de-trámites-ciudadanos")
        wf.custom_css = """
/* Colores corporativos Cruceños */
:root {
    --primary-color: #008f39;
    --primary-hover: #006b2a;
}

/* Fondo de la pagina */
body {
    background-color: #f4f7f6 !important;
}

/* El contenedor del formulario */
.web-form-container {
    background-color: white !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 30px rgba(0, 143, 57, 0.1) !important;
    padding: 2.5rem !important;
    border-top: 5px solid var(--primary-color) !important;
}

/* Boton Guardar / Submit */
.btn-primary, .submit-btn {
    background-color: var(--primary-color) !important;
    border-color: var(--primary-hover) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 8px 24px !important;
    box-shadow: 0 4px 10px rgba(0, 143, 57, 0.25) !important;
    transition: all 0.3s ease !important;
}

.btn-primary:hover, .submit-btn:hover {
    background-color: var(--primary-hover) !important;
    box-shadow: 0 6px 15px rgba(0, 143, 57, 0.35) !important;
    transform: translateY(-2px) !important;
}

/* Inputs focus */
.form-control:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 0.2rem rgba(0, 143, 57, 0.25) !important;
}

/* Titulo principal */
.web-form-title h1 {
    color: #222 !important;
    font-weight: 800 !important;
    letter-spacing: -1px !important;
}
"""
        wf.save(ignore_permissions=True)

        frappe.clear_cache()
        frappe.db.commit()
        print("Web Form CSS and Logo fixed successfully!")
    except Exception as e:
        print(f"Error: {e}")
