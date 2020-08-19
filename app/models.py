from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Rates(models.Model):
    """
    Model for storing data on insurance rate
    """
    id = fields.IntField(pk=True)
    date = fields.DateField()
    cargo_type = fields.CharField(max_length=50)
    rate = fields.FloatField()

    class Meta:
        unique_together = ('date', 'cargo_type')


RatesPydantic = pydantic_model_creator(Rates, name='Model')
RatesInPydantic = pydantic_model_creator(Rates, name='ModelIn', exclude_readonly=True)
