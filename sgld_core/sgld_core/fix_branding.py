import frappe

def execute():
    try:
        # Fix Website Settings Footer
        web_settings = frappe.get_doc("Website Settings")
        web_settings.footer_powered = "<strong>DESARROLLADO POR ENORS S.R.L.</strong>"
        web_settings.hide_footer_signup = 1
        web_settings.app_name = "Concejo Municipal"
        web_settings.brand_html = '<span style="color: #008f39; font-weight: bold; font-size: 1.2rem;"><img src="/files/image1.jpg" style="height: 30px; margin-right: 10px;">Concejo Municipal SGLD</span>'
        web_settings.save(ignore_permissions=True)

        # Fix Website Theme CSS Class and compile
        theme_name = "SGLD Theme"
        if frappe.db.exists("Website Theme", theme_name):
            theme = frappe.get_doc("Website Theme", theme_name)
            theme.theme_scss = """
$primary: #008f39; // Verde Cruceño
$secondary: #ffffff;
$body-bg: #f4f7f6;
$text-color: #333333;

body {
    background-color: $body-bg;
}

// Botones Pro
.btn-primary, .submit-btn {
    background-color: $primary !important;
    border-color: darken($primary, 5%) !important;
    color: white !important;
    border-radius: 8px !important;
    transition: all 0.3s ease;
}

.btn-primary:hover, .submit-btn:hover {
    background-color: darken($primary, 10%) !important;
    transform: translateY(-1px);
}

// Ocultar logo por defecto de frappe si existe
.footer-powered {
    color: #666 !important;
    font-size: 14px;
}

// Para las paginas de web form que quizas tengan fondos blancos
.web-form-container {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    padding: 2rem;
    margin-top: 2rem;
}
"""
            theme.save(ignore_permissions=True)
            print("Website Theme updated and compiled.")

        # Activate Theme
        frappe.db.set_single_value("Website Settings", "website_theme", theme_name)
        
        # Clear caches
        frappe.clear_cache()
        frappe.db.commit()
        print("Branding fixed successfully!")
    except Exception as e:
        print(f"Error updating branding: {e}")
