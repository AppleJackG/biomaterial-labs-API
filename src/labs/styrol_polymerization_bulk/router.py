from fastapi import APIRouter, Depends

from ...auth.models import User
from ...auth.service import user_service
from .schemas import StyrolPolymerizationBulkDTO
from .service import styrol_polymerization_bulk_service


router = APIRouter(
    prefix='/styrol-polymerization-bulk',
    tags=['Полимеризация стирола в блоке'],
)


@router.post('/create_empty_row')
async def create_empty_row(
    row_number: int,
    user: User = Depends(user_service.get_current_user)
) -> StyrolPolymerizationBulkDTO:
    lab_dto = await styrol_polymerization_bulk_service.create_empty_row(row_number, user)
    return lab_dto


@router.patch('/update')
async def update_table(
    new_values: list[StyrolPolymerizationBulkDTO],
    user: User = Depends(user_service.get_current_user)
) -> list[StyrolPolymerizationBulkDTO]:
    lab_dto = await styrol_polymerization_bulk_service.update_table(
        new_values,
        user
    )
    return lab_dto


@router.get('/get')
async def get_table(user: User = Depends(user_service.get_current_user)) -> list[StyrolPolymerizationBulkDTO]:
    lab_dto = await styrol_polymerization_bulk_service.get_table(user)
    return lab_dto
