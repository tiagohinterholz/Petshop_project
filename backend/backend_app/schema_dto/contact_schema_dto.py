from marshmallow import Schema, fields

class ContactSchemaDTO(Schema):
    
    id = fields.Int(dump_only=True)
    client_id = fields.Integer(required=True)
    type_contact = fields.Str(required=True)
    value_contact = fields.String(required=True)