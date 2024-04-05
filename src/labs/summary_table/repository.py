from uuid import UUID
from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload
from .models import SummaryTableORM, LabNamesEn
from ...database import session_factory


class SummaryTableRepository:
    
    async def add_user_to_summary_table(self, user_id: UUID) -> SummaryTableORM:
        stmt = (
            insert(SummaryTableORM)
            .values(user_id=user_id)
            .returning(SummaryTableORM)
        )
        async with session_factory() as session:
            result = await session.execute(stmt)
            summary_table_orm = result.scalar_one()
            await session.commit()
        return summary_table_orm
    
    async def get_summary_table(self) -> list[SummaryTableORM]:
        stmt = (
            select(SummaryTableORM)
            .options(
                selectinload(SummaryTableORM.user)
            )
        )
        async with session_factory() as session:
            result = await session.execute(stmt)
            summary_table_orm = result.scalars()
        return summary_table_orm

    async def get_lab_status(self, user_id: UUID) -> SummaryTableORM:
        stmt = (
            select(SummaryTableORM)
            .where(SummaryTableORM.user_id == user_id)
        )
        async with session_factory() as session:
            result = await session.execute(stmt)
            summary_table_orm = result.scalar_one()
        return summary_table_orm

    async def change_lab_status(self, user_id: UUID, lab_name: str, lab_status: str) -> None:
        stmt = (
            update(SummaryTableORM)
            .where(SummaryTableORM.user_id == user_id)
            .values({lab_name: lab_status})
        )
        async with session_factory() as session:
            await session.execute(stmt)
            await session.commit()
        return
    

summary_table_repository = SummaryTableRepository()