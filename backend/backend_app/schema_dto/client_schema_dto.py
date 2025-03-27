from marshmallow import Schema, fields

class ClientSchemaDTO(Schema):
    
    id = fields.Int(dump_only=True)
    name = fields.String(dump_only=True)
    user_id = fields.Int(required=True)
    register_date = fields.Date(dump_only=True)