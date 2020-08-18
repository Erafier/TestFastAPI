from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Models(models.Model):
    """
    Test Model
    """
    id = fields.IntField(pk=True)
    #: asd
    date = fields.DateField()
    cargo_type = fields.CharField(max_length=50)
    rate = fields.FloatField()

    class Meta:
        unique_together = ('date', 'cargo_type')


ModelPydantic = pydantic_model_creator(Models, name='Model')
ModelInPydantic = pydantic_model_creator(Models, name='ModelIn', exclude_readonly=True)
