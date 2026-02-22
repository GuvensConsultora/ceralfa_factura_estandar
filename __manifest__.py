{
    "name": "Ceralfa Factura Estándar ARCA",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Reporte de factura estándar ARCA argentino",
    "description": """
        Reporte de factura limpio con formato ARCA estándar argentino.
        Se activa por contacto mediante checkbox en res.partner.
    """,
    "author": "Guvens Consultora",
    "license": "LGPL-3",
    "depends": [
        "account",
        "l10n_ar",
        "l10n_ar_afipws_fe",
    ],
    "data": [
        "views/res_partner_views.xml",
        "report/report_invoice_arca.xml",
    ],
    "installable": True,
    "auto_install": False,
}
