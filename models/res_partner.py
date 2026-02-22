from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Por qué: Permite activar el reporte ARCA por contacto individual
    # Patrón: Flag booleano en partner para selección dinámica de reporte
    x_modelo_factura_arca = fields.Boolean(
        string="Modelo Factura ARCA",
        help="Usar el reporte de factura estándar ARCA para este contacto",
    )
