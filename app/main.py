import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from app.models import RatesPydantic, RatesInPydantic, Rates
from app.schemas import Item

app = FastAPI(title='Insurance calculator')


@app.get("/insurance")
async def calculate_insurance(
        declared_value: float,
        cargo_type: str,
        date: Optional[datetime.date] = datetime.date.today()
):
    try:
        model = await Rates.get(date=date, cargo_type=cargo_type)
    except DoesNotExist:
        return f'Для даты {date} не указан тариф на товар {cargo_type}'
    return {
        "insurance_cost": declared_value * model.rate,
    }


@app.get("/prices")
async def show_prices():
    return await RatesInPydantic.from_queryset(Rates.all())


@app.post('/prices')
async def add_prices(records: Dict[str, List[Item]]):
    for date, record in records.items():
        for item in record:
            await Rates.create(date=date, **item.dict())
    return records


@app.get("/prices/{date}")
async def show_prices_by_date(
        date: datetime.date,
        cargo_type: Optional[str] = None
):
    prices = Rates.filter(date=date)
    if cargo_type:
        price = await prices.get(cargo_type=cargo_type)
        return price
    return await RatesInPydantic.from_queryset(prices)


register_tortoise(
    app,
    db_url="sqlite://../database/db.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", port=7777, reload=True)
