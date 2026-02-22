from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_name_invoice_report(self):
        """Override para seleccionar template ARCA según flag del partner.

        Por qué: Odoo usa este método para determinar qué template QWeb
        renderizar al imprimir la factura. Si el contacto tiene el flag
        activado, usamos nuestro template limpio en vez del estándar (roto por CSS).
        Patrón: Polimorfismo por configuración en partner.
        """
        self.ensure_one()
        if self.partner_id.x_modelo_factura_arca:
            return "ceralfa_factura_estandar.report_invoice_arca_document"
        return super()._get_name_invoice_report()
