# Templates Directory

This directory contains document templates for PDF generation.

## Template Structure

Templates are JSON files that define the layout and structure of documents.

### Example Template

```json
{
  "name": "credit_note",
  "title": "Credit Note",
  "fields": [
    {
      "name": "document_number",
      "label": "Document Number",
      "required": true
    },
    {
      "name": "client_name",
      "label": "Client Name",
      "required": true
    },
    {
      "name": "amount",
      "label": "Amount",
      "required": true,
      "type": "currency"
    }
  ]
}
```

## Available Templates

- `credit_note.json` - Template for credit notes (to be created)
- `commission_acknowledgement.json` - Template for commission acknowledgements (to be created)
