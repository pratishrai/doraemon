import logging
from sqlalchemy.schema import CreateTable
import sqlalchemy as sa
from databases import Database


logging.basicConfig(level=logging.INFO)


meta = sa.MetaData()


Guild = sa.Table(
    "guilds",
    meta,
    sa.Column("id", sa.BigInteger, primary_key=True),
    sa.Column("guild", sa.BigInteger, nullable=False),
    sa.Column("store_logs", sa.Boolean, server_default='1')
)

tables = [Guild]

engine = None

async def prepare_engine():
    global engine
    if engine is None:
        engine = Database('db creds')
        await engine.connect()
    return engine


async def prepare_tables():
    engine = await prepare_engine()
    for table in tables:
        table_name = table.name
        query = f"""
SELECT * FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = N'{table_name}'"""
        resp = await engine.fetch_one(query)
        create_expr = CreateTable(table)
        if resp is None:
            logging.info(f"Table {table_name} does not exist; creating...")
            await engine.execute(create_expr)
        else:
            logging.info(f"Table {table_name} already exists.")


async def make_guild_profile(guild_list, slef_id):
    engine = await prepare_engine()
    create_query_value = []
    for guild in guild_list:
        exists_query = Guild.select().where(Guild.c.guild == guild.id)
        res = await engine.fetch_one(exists_query)
        if res is None:
            create_query_value.append(
                {"guild": guild.id}
            )
            logging.info(f"creating profile for guild {guild.name}")
    if len(create_query_value) > 0:
        create_query = Guild.insert()
        await engine.execute(create_query, values=create_query_value)
