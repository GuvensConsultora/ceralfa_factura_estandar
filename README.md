# Ceralfa Factura Estándar ARCA

## Bloque 1: Introducción

### Qué hace Odoo nativamente

Odoo 19 con localización argentina (`l10n_ar`) incluye un reporte de factura estándar que muestra datos fiscales argentinos (CUIT, letra, CAE, QR AFIP). Sin embargo, el template por defecto tiene problemas de CSS que rompen el formato visual, especialmente al generar PDF.

### Limitación

El reporte estándar de Odoo no siempre se renderiza correctamente: estilos rotos, elementos desalineados y falta de control sobre qué clientes usan qué formato de factura.

### Qué resuelve este módulo

Agrega un **template de factura limpio con formato ARCA** que se activa **por contacto**. El usuario decide qué clientes reciben facturas con el formato ARCA y cuáles siguen con el formato estándar de Odoo.

- Template QWeb standalone (no hereda del template roto)
- Activación individual por contacto (checkbox)
- Soporte multimoneda con conversión a pesos
- QR AFIP + CAE integrados

---

## Bloque 2: Funcionamiento para el usuario final

### Flujo de uso

```
1. Ir al contacto del cliente
2. Activar checkbox "Modelo Factura ARCA"
3. Crear factura para ese cliente
4. Al imprimir → sale con formato ARCA limpio
```

### Qué cambia en la factura impresa

| Sección | Contenido |
|---------|-----------|
| **Header** | Logo empresa + Letra grande (A/B/C) con código AFIP + Tipo documento (FACTURA / NOTA DE CRÉDITO / NOTA DE DÉBITO) |
| **Datos empresa** | Razón social, dirección, teléfono, web, email, condición IVA, CUIT, IIBB, inicio actividades |
| **Datos cliente** | Nombre, dirección, condición IVA, CUIT |
| **Detalle factura** | Fecha vencimiento, plazo de pago, origen, referencia |
| **Líneas** | Descripción, cantidad, precio unitario, % IVA, importe |
| **Totales** | Subtotal + desglose de impuestos + Total |
| **Multimoneda** (si aplica) | Moneda, tipo de cambio, sección "Impuestos AR" con conversión a pesos |
| **Pie** | Términos y condiciones, total en letras, QR AFIP, CAE y vencimiento |

### Tipos de comprobante soportados

| Tipo | Cuándo se muestra |
|------|-------------------|
| FACTURA | Factura de cliente (`out_invoice`) |
| NOTA DE CRÉDITO | Nota de crédito (`out_refund`) |
| NOTA DE DÉBITO | Nota de débito (factura con `debit_origin_id`) |

---

## Bloque 3: Parametrización

### Paso 1 — Activar el reporte en un contacto

1. Ir a **Contactos** (menú principal)
2. Abrir la ficha del cliente
3. Ir a la pestaña **Contabilidad**
4. Buscar el grupo **"Factura ARCA"**
5. Activar el checkbox **"Modelo Factura ARCA"**
6. Guardar

![Ruta: Contactos → Cliente → Pestaña Contabilidad → Factura ARCA](ruta_contacto.png)

```
Contactos
  └── [Cliente]
        └── Pestaña: Contabilidad
              └── Grupo: Factura ARCA
                    └── ☑ Modelo Factura ARCA
```

### Paso 2 — Imprimir factura con formato ARCA

1. Ir a **Contabilidad → Clientes → Facturas**
2. Abrir o crear una factura para el cliente configurado
3. Confirmar la factura
4. Click en **Imprimir → Facturas**
5. El sistema detecta automáticamente que el contacto tiene el flag y usa el template ARCA

```
Contabilidad
  └── Clientes
        └── Facturas
              └── [Factura confirmada]
                    └── Imprimir → Facturas → (sale formato ARCA)
```

### Paso 3 — Desactivar para un contacto

Para volver al formato estándar de Odoo:

1. Ir al contacto
2. Pestaña **Contabilidad**
3. Desactivar checkbox **"Modelo Factura ARCA"**
4. Las próximas impresiones usan el template estándar

### Paso 4 — Configurar datos bancarios (CBU) en la factura

Por defecto Odoo NO muestra los CBU de la empresa en el PDF de la factura. Este módulo agrega una sección "Datos bancarios" debajo de los totales, pero solo muestra las cuentas bancarias que el usuario elija.

1. Ir a **Contactos** → abrir la **empresa propia** (My Company)
2. Ir a la pestaña **Contabilidad** → sección **Cuentas bancarias**
3. Abrir cada cuenta bancaria que se quiera mostrar en la factura
4. Activar el checkbox **"Mostrar en factura"**
5. Guardar

```
Contactos
  └── [Mi Empresa]
        └── Pestaña: Contabilidad
              └── Cuentas bancarias
                    └── [Cuenta bancaria]
                          └── ☑ Mostrar en factura
```

**Resultado**: En el PDF de la factura aparece una tabla debajo de los totales con columnas: Banco, CBU y Nro. Cuenta — solo para las cuentas marcadas.

### Notas de configuración

- **No requiere configuración global**: se activa contacto por contacto
- **No afecta facturas existentes**: el formato se determina al momento de imprimir, no al crear la factura
- **Compatible con multimoneda**: si la factura está en USD (u otra moneda), el reporte muestra una sección extra "Impuestos AR" con los importes convertidos a pesos usando el tipo de cambio de la factura
- **CBU selectivo**: solo las cuentas bancarias de la empresa con "Mostrar en factura" activo aparecen en el PDF. Si ninguna cuenta está marcada, la sección no se muestra

---

## Bloque 4: Referencia técnica

### Arquitectura

```
ceralfa_factura_estandar/
├── __manifest__.py                    # Metadata, dependencias
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── res_partner.py                 # Campo x_modelo_factura_arca (Boolean)
│   ├── res_partner_bank.py            # Campo show_on_invoice (Boolean)
│   └── account_move.py                # Override _get_name_invoice_report()
├── views/
│   ├── res_partner_views.xml          # Checkbox en pestaña Contabilidad del contacto
│   ├── res_partner_bank_views.xml     # Checkbox "Mostrar en factura" en cuentas bancarias
│   └── report_l10n_ar_override.xml    # Mejoras visuales + sección CBU en factura
└── report/
    └── report_invoice_arca.xml        # Template QWeb standalone
```

### Modelos

| Modelo | Tipo | Campo/Método | Descripción |
|--------|------|-------------|-------------|
| `res.partner` | Herencia | `x_modelo_factura_arca` (Boolean) | Flag para activar reporte ARCA |
| `res.partner.bank` | Herencia | `show_on_invoice` (Boolean) | Controla qué cuentas bancarias aparecen en el PDF |
| `account.move` | Herencia | `_get_name_invoice_report()` | Retorna template ARCA si el partner tiene el flag |

### Método `_get_name_invoice_report()`

```python
def _get_name_invoice_report(self):
    self.ensure_one()
    if self.partner_id.x_modelo_factura_arca:
        return "ceralfa_factura_estandar.report_invoice_arca_document"
    return super()._get_name_invoice_report()
```

Odoo llama este método para decidir qué template QWeb renderizar. Si el contacto tiene el flag → template ARCA. Si no → template estándar (vía `super()`).

### Vista heredada

Hereda `account.view_partner_property_form` (pestaña Contabilidad del contacto) vía xpath. Agrega el grupo "Factura ARCA" después del primer group de la pestaña accounting.

### Template QWeb

Dos templates en `report_invoice_arca.xml`:

| Template ID | Función |
|-------------|---------|
| `report_invoice_arca` | Wrapper: itera `docs` y llama al template documento |
| `report_invoice_arca_document` | Documento: renderiza una factura individual |

El template es **standalone** (no hereda del template estándar de Odoo). Usa `web.external_layout` para header/footer de la empresa.

### Campos de la factura usados en el template

| Campo | Sección | Uso |
|-------|---------|-----|
| `company_id.logo` | Header | Logo empresa |
| `l10n_latam_document_type_id.l10n_ar_letter` | Header | Letra grande (A/B/C) |
| `l10n_latam_document_type_id.code` | Header | Código AFIP |
| `move_type` / `debit_origin_id` | Header | Determina tipo documento |
| `name`, `invoice_date` | Header | Número y fecha |
| `partner_id.*` | Cliente | Datos del cliente |
| `invoice_line_ids` | Líneas | Detalle de productos |
| `tax_totals` | Totales | Desglose de impuestos (API Odoo 19) |
| `amount_untaxed`, `amount_total` | Totales | Subtotal y total |
| `currency_id`, `invoice_currency_rate` | Multimoneda | Moneda y tipo de cambio |
| `qr_code` / `texto_modificado_qr` | Pie | QR AFIP |
| `afip_auth_code` / `afip_cae` | Pie | CAE |

### Dependencias

```
ceralfa_factura_estandar
  ├── account          # Modelo account.move
  ├── l10n_ar          # Localización argentina (CUIT, letra, tipos comprobante)
  └── l10n_ar_afipws_fe  # Factura electrónica AFIP (CAE, QR, invoice_currency_rate)
```

### Seguridad

No define reglas propias. Usa los permisos estándar de Odoo:
- Ver/editar contactos: grupos de `base` y `account`
- Imprimir facturas: `account.group_account_invoice`
