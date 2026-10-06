import frappe

def execute():
    wf = frappe.get_doc("Web Form", "ventanilla-de-trámites-ciudadanos")
    
    wf.client_script = """
frappe.web_form.after_save = () => {
    setTimeout(() => {
        let tracking_no = frappe.web_form.doc.name;
        $('.web-form-message').html(`
            <div class="text-center" style="padding: 20px;">
                <svg width="80" height="80" viewBox="0 0 16 16" class="bi bi-check-circle-fill text-success mb-3" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                </svg>
                <h2>¡Trámite Validado!</h2>
                <p>Su trámite ha sido registrado exitosamente. Guarde su número de seguimiento para futuras consultas.</p>
                <div class="alert alert-primary mt-4" style="font-size: 1.2rem; background-color: #f8f9fa; border: 2px dashed #007bff; border-radius: 8px;">
                    <strong style="color: #007bff;">NÚMERO DE SEGUIMIENTO:</strong><br>
                    <span style="font-size: 2.2rem; font-family: monospace; letter-spacing: 2px; color: #343a40;">${tracking_no}</span>
                </div>
                <button class="btn btn-primary mt-3" onclick="window.print()" style="font-size: 1.1rem; padding: 10px 20px;">🖨️ Imprimir Comprobante</button>
                <br>
                <a class="btn btn-light mt-3" href="/ventanilla/new">Enviar otro trámite</a>
            </div>
        `);
    }, 100);
};
"""
    wf.save(ignore_permissions=True)
    frappe.db.commit()
    print("Web form client script updated successfully!")
