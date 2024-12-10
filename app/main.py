from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.core.models import db_helper, Base
from app.parser import scrape_and_populate

from app.api_v1 import router as router_v1

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        await scrape_and_populate()
    except Exception as e:
        print(f"An error occurred during data population: {e}")

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)