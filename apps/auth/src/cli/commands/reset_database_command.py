import asyncio
import click
import logging
import alembic.command

from contextlib import asynccontextmanager

import httpx

import hydra
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from src import database

from src.config import AppConfig, DatabaseConfig
from src.constants import Constants
from src.crawler import load_repository_urls
from src.models import ModelType

logger = logging.getLogger(__name__)

async def _reset_db(db_config: DatabaseConfig):
    engine = database.create_engine_from_conf(db_config)

    with engine.connect() as connection:
        connection.execute(
            text(
                """
                   DROP TABLE IF EXISTS
                       log,
                    CASCADE;
                        
                """
            )
        )

        config = database.create_alembic_config(engine)

        alembic.command.stamp(config, "base", purge=True)
        alembic.command.upgrade(config, "head")

    engine = database.create_async_engine_from_conf(db_config)

    # To populate db after shutdown
    urls = load_repository_urls()

    async with httpx.AsyncClient(
        timeout=Constants.HTTPX_TIMEOUT,
        transport=httpx.AsyncHTTPTransport(
            retries=Constants.HTTPX_RETRIES,
        )
    ) as client:
        tasks = [_import_repository(engine, client, model, url) for model, url in urls.items()]
        await asyncio.gather(*tasks)


async def _import_repository(engine: AsyncEngine, client: https.AsyncClient, model: str, url: str):
    match model:
        case ModelType.LOG.value:
            async for log in load_logs(client, url):
                async with _create_service(engine) as service:
                    service.save_log(log)


@asynccontextmanager
async def _create_service(engine: AsyncEngine):
    async with service.from_engine(engine) as service:
        yield service

@click.command()
@click.option("--sources-file", help="Sources file to populate database after migration")
@hydra.main(
    version_base=None,
    config_path=Constants.CONFIG_PATH,
    config_name=Constants.CONFIG_NAME,
)
def start_server_command(config: AppConfig):
    _cleanup_coroutines = []

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(_reset_db(config.db))
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()