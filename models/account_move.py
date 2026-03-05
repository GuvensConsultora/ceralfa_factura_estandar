# Por qué: Campos custom para la zona "Forma de pago" en el PDF de factura.
# Facu pide: Anticipo y Forma de pago convenida visibles en la factura impresa.
# Patrón: herencia de account.move con campos Selection/Char editables en la factura.
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Por qué: "Anticipo" indica si la factura requiere pago adelantado
    x_anticipo = fields.Monetary(
        'Anticipo',
        currency_field='currency_id',
        help='Monto de anticipo requerido para esta operación',
    )
    # Por qué: "Forma de pago convenida" es texto libre que describe
    # el acuerdo de pago específico (ej: "Cheque 30/60 días", "Transferencia")
    x_forma_pago_convenida = fields.Char(
        'Forma de pago convenida',
        help='Descripción de la forma de pago acordada con el cliente',
    )
