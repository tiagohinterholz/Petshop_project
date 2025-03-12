from marshmallow import Schema, fields

class BreedSchemaDTO(Schema):
    
    description = fields.String(required=True)
    