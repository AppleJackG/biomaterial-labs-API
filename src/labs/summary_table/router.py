from uuid import UUID
from fastapi import APIRouter, Depends

from .schemas import LabStatus, SummaryTableDTO
from .service import summary_table_service
from .models import LabNamesEn
from ...auth.service import user_service
from ...auth.models import User


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


@router.patch('/change-lab-status')
async def change_lab_status(lab_name: LabNamesEn, user: User = Depends(user_service.get_current_user)) -> LabStatus:
    new_status = await summary_table_service.change_lab_status(user.user_id, lab_name)
    return new_status
