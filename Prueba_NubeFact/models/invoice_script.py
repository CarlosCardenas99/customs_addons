from .models import AccountMove

# Obtener registros del modelo AccountMove
invoices = AccountMove.search([('type', '=', 'out_invoice')], limit=5)

# Recorrer los registros e imprimir información
for invoice in invoices:
    print('Número de Factura:', invoice.name)
    print('Cliente:', invoice.partner_id.name)
    print('Fecha de Emisión:', invoice.invoice_date)
    print('Total:', invoice.amount_total)
    print('---')


