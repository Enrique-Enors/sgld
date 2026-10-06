import frappe

def execute():
    # Update DocType to NOT be custom, so it exports to JSON
    dt = frappe.get_doc("DocType", "Tramite Ciudadano")
    dt.custom = 0
    dt.save(ignore_permissions=True)

    # Create Web Form
    webform_name = "ventanilla-ciudadana"
    if not frappe.db.exists("Web Form", webform_name):
        wf = frappe.get_doc({
            "doctype": "Web Form",
            "title": "Ventanilla de Trámites Ciudadanos",
            "route": "ventanilla",
            "doc_type": "Tramite Ciudadano",
            "module": "Sgld Core",
            "is_standard": 1,
            "published": 1,
            "login_required": 0,
            "allow_multiple": 1,
            "allow_delete": 0,
            "allow_comments": 0,
            "allow_edit": 0,
            "allow_incomplete": 0,
            "allow_print": 1,
            "success_message": "Su trámite ha sido registrado exitosamente. Guarde su número de seguimiento.",
            "web_form_fields": [
                {"fieldname": "nombre_completo", "label": "Nombre Completo", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "carnet_identidad", "label": "Carnet de Identidad", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "celular", "label": "Celular de Contacto", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "asunto", "label": "Asunto o Motivo", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "descripcion", "label": "Descripción Detallada", "fieldtype": "Text Editor", "reqd": 1},
                {"fieldname": "archivo_adjunto", "label": "Archivo Adjunto (PDF)", "fieldtype": "Attach"}
            ]
        })
        wf.insert(ignore_permissions=True)
        print("Web Form 'Ventanilla de Trámites Ciudadanos' created!")
    else:
        print("Web Form exists.")

    frappe.db.commit()
