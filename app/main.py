import asyncio
from contextlib import asynccontextmanager
import uvicorn
import logging
from fastapi import FastAPI
from app.core.config import settings
from app.core.models import db_helper, Base
from app.parser import scrape_and_populate
from app.api_v1 import router as router_v1

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def periodic_scrape_and_populate():
    while True:
        try:
            logger.info("Running scrape_and_populate to update the schedule...")
            await scrape_and_populate()
            logger.info("Schedule updated successfully.")
        except Exception as e:
            logger.error(f"An error occurred during data population: {e}", exc_info=True)
        await asyncio.sleep(settings.fetch_updates_interval)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    task = asyncio.create_task(periodic_scrape_and_populate())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Background task cancelled.")

app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)