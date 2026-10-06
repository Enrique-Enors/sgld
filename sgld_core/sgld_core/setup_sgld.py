import frappe

def execute():
    roles = [
        "Presidente",
        "Concejal",
        "Asesor",
        "Secretaría",
        "Comisiones",
        "Asesoramiento Legal",
        "Ventanilla",
        "Actuario"
    ]
    for role_name in roles:
        if not frappe.db.exists("Role", role_name):
            doc = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": 1
            })
            doc.insert(ignore_permissions=True)
            print(f"Role created: {role_name}")
        else:
            print(f"Role exists: {role_name}")

    doctype_name = "Tramite Ciudadano"
    if not frappe.db.exists("DocType", doctype_name):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": doctype_name,
            "module": "Sgld Core",
            "custom": 1,
            "istable": 0,
            "naming_rule": "Expression",
            "autoname": "TRAMITE-.YYYY.-.####",
            "fields": [
                {"fieldname": "nombre_completo", "label": "Nombre Completo", "fieldtype": "Data", "reqd": 1, "in_list_view": 1},
                {"fieldname": "carnet_identidad", "label": "Carnet de Identidad", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "celular", "label": "Celular de Contacto", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "asunto", "label": "Asunto o Motivo", "fieldtype": "Data", "reqd": 1, "in_list_view": 1},
                {"fieldname": "descripcion", "label": "Descripción Detallada", "fieldtype": "Text Editor", "reqd": 1},
                {"fieldname": "estado", "label": "Estado del Trámite", "fieldtype": "Select", "options": "Recibido\nEn Revisión\nDerivado a Comisión\nFinalizado\nRechazado", "default": "Recibido", "in_list_view": 1},
                {"fieldname": "archivo_adjunto", "label": "Archivo Adjunto (PDF)", "fieldtype": "Attach"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Ventanilla", "read": 1, "write": 1, "create": 1},
                {"role": "Concejal", "read": 1},
                {"role": "Comisiones", "read": 1}
            ]
        })
        doc.insert(ignore_permissions=True)
        print(f"DocType created: {doctype_name}")
    else:
        print(f"DocType exists: {doctype_name}")

    frappe.db.commit()
