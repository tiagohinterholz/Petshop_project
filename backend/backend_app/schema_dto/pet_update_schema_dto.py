from marshmallow import Schema, fields

class PetUpdateSchemaDTO(Schema):
    
    breed_id = fields.Integer(required=False)
    birth_date = fields.Date(required=False)
    name = fields.String(required=False)
    client_id = fields.Integer(required=False)