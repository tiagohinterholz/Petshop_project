from marshmallow import Schema, fields

class ClientSchemaDTO(Schema):
    
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    cpf = fields.String(required=True, metadata={"unique": True})
    register_date = fields.Date(required=True)