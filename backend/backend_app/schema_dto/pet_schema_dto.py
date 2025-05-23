from marshmallow import Schema, fields

class PetSchemaDTO(Schema):
    
    id = fields.Int(dump_only=True)
    client_id = fields.Integer(required=True)
    breed_id = fields.Integer(required=True)
    birth_date = fields.Date(required=True)
    name = fields.String(required=True)