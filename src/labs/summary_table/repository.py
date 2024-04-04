from uuid import UUID
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from .models import SummaryTableORM
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


summary_table_repository = SummaryTableRepository()