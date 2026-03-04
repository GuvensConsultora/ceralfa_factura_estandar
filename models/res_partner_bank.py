from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    # Por qué: Controla qué cuentas bancarias aparecen en el PDF de factura
    # Patrón: Flag booleano para filtrado selectivo en reportes QWeb
    show_on_invoice = fields.Boolean(
        string="Mostrar en factura",
        default=False,
        help="Si está activo, esta cuenta bancaria se muestra en el PDF de la factura",
    )
