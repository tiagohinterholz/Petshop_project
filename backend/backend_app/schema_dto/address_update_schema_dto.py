from marshmallow import Schema, fields

class AddressUpdateSchemaDTO(Schema):
    
    client_id = fields.Integer(required=False)
    street = fields.String(required=False)
    city = fields.String(required=False)
    neighborhood = fields.String(required=False)
    complement = fields.String(required=False)