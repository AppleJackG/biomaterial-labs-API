from uuid import UUID
from fastapi import APIRouter

from .schemas import SummaryTableDTO
from .service import summary_table_service



router = APIRouter(
    prefix='/summary-table',
    tags=['Summary table'],
)


@router.post('')
async def add_user_to_summary_table(user_id: UUID):
    summary_table = await summary_table_service.add_user_to_summary_table(user_id)
    return summary_table


@router.get('')
async def get_summary_table() -> list[SummaryTableDTO]:
    summary_table = await summary_table_service.get_summary_table()
    return summary_table