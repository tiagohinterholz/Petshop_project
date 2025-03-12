from marshmallow import Schema, fields

class AddressSchemaDTO(Schema):
    
    client_id = fields.Integer(required=True)
    street = fields.String(required=True)
    city = fields.String(required=True)
    neighborhood = fields.String(required=True)
    complement = fields.String(load_default=None)