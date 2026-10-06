import frappe

def execute():
    wf = frappe.get_doc("Web Form", "ventanilla-de-trámites-ciudadanos")
    
    wf.client_script = """
// Hook into the browser's Fetch API to intercept the save request natively
const originalFetch = window.fetch;
window.fetch = async function(...args) {
    const response = await originalFetch.apply(this, args);
    const url = args[0];
    
    // Check if this is the Web Form save request
    if (typeof url === 'string' && url.includes('frappe.website.doctype.web_form.web_form.accept')) {
        // Clone the response so we can read the JSON without consuming the stream for Frappe
        const clone = response.clone();
        clone.json().then(data => {
            if (data && data.message && data.message.name) {
                let tracking_no = data.message.name;
                
                // Wait for Frappe to render its default success page, then overwrite it
                setTimeout(() => {
                    $('.success-page').html(`
                        <div class="text-center" style="padding: 30px;">
                            <svg width="80" height="80" viewBox="0 0 16 16" class="text-success mb-3" fill="#28a745" xmlns="http://www.w3.org/2000/svg">
                              <path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                            </svg>
                            <h2 style="font-weight: bold; color: #333;">¡Trámite Validado!</h2>
                            <p style="font-size: 1.1rem; color: #666;">Su trámite ha sido registrado exitosamente. Guarde su número de seguimiento para futuras consultas.</p>
                            <div class="mt-4" style="font-size: 1.2rem; background-color: #f0f7ff; border: 2px dashed #007bff; border-radius: 12px; padding: 25px;">
                                <strong style="color: #007bff; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 1px;">Número de Seguimiento:</strong><br>
                                <span style="font-size: 2.5rem; font-family: monospace; font-weight: bold; letter-spacing: 2px; color: #1a1a1a;">${tracking_no}</span>
                            </div>
                            <button class="btn btn-primary mt-4" onclick="window.print()" style="font-size: 1.1rem; padding: 12px 24px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,123,255,0.2);">🖨️ Imprimir Comprobante</button>
                            <br>
                            <a class="btn btn-light mt-4" href="/ventanilla/new" style="color: #666; text-decoration: underline;">Enviar otro trámite</a>
                        </div>
                    `);
                }, 200); // 200ms ensures Frappe is completely done with DOM manipulations
            }
        }).catch(err => console.error("Error reading fetch response:", err));
    }
    return response;
};
"""
    wf.save(ignore_permissions=True)
    frappe.db.commit()
    print("Web form JS patched successfully with Fetch Interceptor!")
