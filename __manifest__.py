{
    "name": "Ceralfa Layout ARCA",
    "version": "19.0.2.0.0",
    "category": "Accounting/Localizations",
    "summary": "Layout de documento ARCA argentino para Settings > Document Layout",
    "description": """
        Registra el layout "ARCA" en Settings > Document Layout.
        Header con datos fiscales argentinos (CUIT, IIBB, Cond. IVA, Inicio Act.)
        + mejoras visuales al contenido de factura l10n_ar.
    """,
    "author": "Guvens Consultora",
    "license": "LGPL-3",
    # Por qué: l10n_ar para CUIT/IIBB/IVA condition en header.
    # No depende de l10n_ar_afipws_fe — QR/CAE los maneja a2systems en su template.
    "depends": [
        "account",
        "l10n_ar",
    ],
    "data": [
        "views/external_layout_arca.xml",
        "views/report_l10n_ar_override.xml",
        "data/report_layout.xml",
    ],
    "installable": True,
    "auto_install": False,
}
