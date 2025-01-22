# migrations/runner.py
import os
import importlib
from typing import List

from datetime import datetime
from beanie import Document


class MigrationRecord(Document):
    name: str
    applied_at: datetime

    class Settings:
        name = "migration_records"


MIGRATIONS_DIR = "app/migrations"

async def get_applied_migrations() -> List[str]:
    records = await MigrationRecord.find_all().to_list()
    return [record.name for record in records]


async def apply_migration(migration_name: str):
    module = importlib.import_module(f"app.migrations.{migration_name}")
    await module.upgrade()
    migration_record = MigrationRecord(
        name=migration_name, applied_at=datetime.now())
    await migration_record.insert()


async def run_migrations():
    migration_files = sorted(
        f[:-3] for f in os.listdir(MIGRATIONS_DIR)
        if f.endswith(".py") and f != "__init__.py" and f != "runner.py"
    )
    applied = await get_applied_migrations()
    pending = [m for m in migration_files if m not in applied]

    for migration in pending:
        print(f"Applying migration: {migration}")
        await apply_migration(migration)
        print(f"Migration {migration} applied successfully.")
