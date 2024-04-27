from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ...auth.models import User
from ...auth.service import user_service
from .schemas import StyrolPolymerizationBulkDTO
from .service import styrol_polymerization_bulk_service


router = APIRouter(
    prefix='/styrol-polymerization-bulk',
    tags=['Полимеризация стирола в блоке'],
)


@router.post('/create-empty-row')
async def create_empty_row(
    row_number: int,
    user: User = Depends(user_service.get_current_user)
) -> StyrolPolymerizationBulkDTO:
    lab_dto = await styrol_polymerization_bulk_service.create_empty_row(row_number, user)
    return lab_dto


@router.patch('/')
async def update_table(
    new_values: list[StyrolPolymerizationBulkDTO],
    user: User = Depends(user_service.get_current_user)
) -> list[StyrolPolymerizationBulkDTO]:
    lab_dto = await styrol_polymerization_bulk_service.update_table(
        new_values,
        user
    )
    return lab_dto


@router.delete('/')
async def delete_row(
    row_number: int, 
    user: User = Depends(user_service.get_current_user)
) -> JSONResponse:
    await styrol_polymerization_bulk_service.delete_row(row_number, user)
    return JSONResponse({'message': 'successful delete'})


@router.get('/get-as-student')
async def get_table_as_student(user: User = Depends(user_service.get_current_user)) -> list[StyrolPolymerizationBulkDTO]:
    lab_dto = await styrol_polymerization_bulk_service.get_table(user.user_id)
    return lab_dto


@router.get('/get-as-teacher', dependencies=[Depends(user_service.get_current_user_teacher)])
async def get_table_as_teacher(user_id: UUID) -> list[StyrolPolymerizationBulkDTO]:
    lab_dto = await styrol_polymerization_bulk_service.get_table(user_id)
    return lab_dto

