from marshmallow import Schema, fields, validate


class CreatePaymentSchema(Schema):
    amount = fields.Float(required=True)
    description = fields.Str(required=True, validate=validate.Length(max=255))
    narration = fields.Str(required=False, validate=validate.Length(max=255))
    method = fields.Str(required=False, validate=validate.Length(max=12))
    direction = fields.Str(required=False, validate=validate.Length(max=6))
    currency = fields.Str(required=False, validate=validate.Length(max=3))

