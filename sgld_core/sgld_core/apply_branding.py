import frappe

def execute():
    try:
        # 1. Update System Settings (Backend Branding)
        sys_settings = frappe.get_doc("System Settings")
        sys_settings.app_name = "SGLD - Concejo Municipal"
        sys_settings.brand_html = '<div style="font-weight: bold; font-size: 16px; color: #007a33;">SGLD</div>'
        sys_settings.save(ignore_permissions=True)

        # 2. Update Website Settings (Frontend Branding)
        web_settings = frappe.get_doc("Website Settings")
        web_settings.app_name = "SGLD - Concejo Municipal"
        web_settings.app_logo = "/files/image1.jpg"
        web_settings.banner_image = "/files/image1.jpg"
        web_settings.brand_html = '<span style="color: #007a33; font-weight: bold;">Concejo Municipal</span>'
        web_settings.footer_powered_by = "DESARROLLADO POR ENORS S.R.L."
        web_settings.hide_footer_signup = 1
        web_settings.save(ignore_permissions=True)

        # 3. Create a Custom Website Theme (Pro Green Design)
        theme_name = "SGLD Theme"
        if not frappe.db.exists("Website Theme", theme_name):
            theme = frappe.new_doc("Website Theme")
            theme.theme = theme_name
            theme.theme_scss = """
// Variables base de colores Cruceños
$primary: #008f39; // Verde bandera de Santa Cruz
$secondary: #ffffff;
$body-bg: #f4f7f6;
$text-color: #333333;

// Estilos Globales Pro
body {
    background-color: $body-bg;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

// Botones con estilo moderno (Glassmorphism / Sombras)
.btn-primary {
    background-color: $primary !important;
    border-color: darken($primary, 5%) !important;
    box-shadow: 0 4px 6px rgba(0, 143, 57, 0.2) !important;
    border-radius: 8px !important;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    background-color: darken($primary, 10%) !important;
    box-shadow: 0 6px 12px rgba(0, 143, 57, 0.3) !important;
    transform: translateY(-1px);
}

// Ocultar Powered By Frappe en el footer estándar (por si el campo footer_powered_by no pisa todo)
.powered-by {
    visibility: hidden;
    position: relative;
}
.powered-by::after {
    content: "DESARROLLADO POR ENORS S.R.L.";
    visibility: visible;
    position: absolute;
    left: 0;
    font-weight: bold;
    color: #666;
}

// Login Page Styling
.login-content {
    background: white;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    border-top: 5px solid $primary;
}

.for-login {
    .page-card-head {
        img {
            max-width: 150px;
            margin-bottom: 20px;
        }
    }
}
"""
            theme.save(ignore_permissions=True)
            print("Website Theme created.")
        else:
            print("Website Theme already exists.")

        # Activate Theme
        frappe.db.set_single_value("Website Settings", "website_theme", theme_name)

        frappe.db.commit()
        print("Branding and styling updated successfully!")
    except Exception as e:
        print(f"Error updating branding: {e}")
