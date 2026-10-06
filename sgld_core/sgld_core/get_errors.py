import frappe

def execute():
    errors = frappe.get_all("Error Log", fields=["method", "error", "creation"], order_by="creation desc", limit=5)
    for e in errors:
        print(f"[{e.creation}] {e.method}:")
        print(e.error[:1000])
        print("-" * 50)
