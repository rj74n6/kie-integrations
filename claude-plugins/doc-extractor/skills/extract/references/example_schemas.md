# Example Schemas

Common JSON schemas for different document types. Use these as starting points.

## Invoice

```json
{
  "vendor_name": "string",
  "vendor_address": "string",
  "invoice_number": "string",
  "invoice_date": "date (MM/DD/YYYY)",
  "due_date": "date (MM/DD/YYYY)",
  "line_items": [{"description": "string", "quantity": "number", "unit_price": "number", "amount": "number"}],
  "subtotal": "number",
  "tax": "number",
  "total_amount": "number",
  "payment_terms": "string"
}
```

## Receipt

```json
{
  "store_name": "string",
  "store_address": "string",
  "date": "date (MM/DD/YYYY)",
  "time": "string",
  "items": [{"name": "string", "quantity": "number", "price": "number"}],
  "subtotal": "number",
  "tax": "number",
  "total": "number",
  "payment_method": "string"
}
```

## W-2 Tax Form

```json
{
  "employer_name": "string",
  "employer_ein": "string",
  "employee_name": "string",
  "employee_ssn_last4": "string (last 4 digits only)",
  "wages_tips_compensation": "number",
  "federal_tax_withheld": "number",
  "social_security_wages": "number",
  "social_security_tax_withheld": "number",
  "medicare_wages": "number",
  "medicare_tax_withheld": "number",
  "state": "string",
  "state_wages": "number",
  "state_tax_withheld": "number",
  "tax_year": "number"
}
```

## Bill of Lading

```json
{
  "bol_number": "string",
  "date": "date (MM/DD/YYYY)",
  "shipper_name": "string",
  "shipper_address": "string",
  "consignee_name": "string",
  "consignee_address": "string",
  "carrier_name": "string",
  "items": [{"description": "string", "weight": "string", "quantity": "number", "freight_class": "string"}],
  "special_instructions": "string",
  "total_weight": "string"
}
```

## Purchase Order

```json
{
  "po_number": "string",
  "date": "date (MM/DD/YYYY)",
  "buyer_name": "string",
  "vendor_name": "string",
  "ship_to_address": "string",
  "line_items": [{"item_number": "string", "description": "string", "quantity": "number", "unit_price": "number", "total": "number"}],
  "total_amount": "number",
  "delivery_date": "date (MM/DD/YYYY)",
  "payment_terms": "string"
}
```
