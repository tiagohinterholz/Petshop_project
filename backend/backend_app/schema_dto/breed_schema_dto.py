from marshmallow import Schema, fields, ValidationError, validates

class BreedSchemaDTO(Schema):
    
    id = fields.Int(dump_only=True)
    description = fields.String(required=True)
    
    @validates('description')
    def validate_description(self, value):
        if not value.strip():  # Remove espaços e verifica se está vazio
            raise ValidationError("A descrição da raça não pode estar vazia.")