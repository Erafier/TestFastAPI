import datetime
import logging
from typing import Dict, List, Optional

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from models import Models, ModelInPydantic
from schemas import Item

app = FastAPI(title='Insurance calculator')

logging.basicConfig(level=logging.INFO)


@app.get("/prices/calculate")
async def calculate_insurance(
        actual_price: float,
        cargo_type: str,
        date: Optional[datetime.date] = datetime.date.today()
):
    try:
        model = await Models.get(date=date, cargo_type=cargo_type)
    except DoesNotExist:
        return f'Для даты {date} не указан тариф на товар {cargo_type}'
    return {
        "insurance_cost": actual_price * model.rate,
    }


@app.get("/prices")
async def show_prices():
    return await ModelInPydantic.from_queryset(Models.all())


@app.post('/prices')
async def add_prices(records: Dict[str, List[Item]]):
    for date, record in records.items():
        for item in record:
            await Models.create(date=date, **item.dict())
    return records


@app.get("/prices/{date}")
async def show_prices_by_date(
        date: datetime.date,
        cargo_type: Optional[str] = None
):
    prices = Models.filter(date=date)
    if cargo_type:
        await prices.filter(cargo_type=cargo_type)
    return await ModelInPydantic.from_queryset(prices)


register_tortoise(
    app,
    db_url="sqlite://database/db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
