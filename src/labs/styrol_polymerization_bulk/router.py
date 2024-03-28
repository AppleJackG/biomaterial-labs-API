from fastapi import APIRouter, Depends

from ...auth.models import User
from ...auth.service import user_service
from .schemas import StyrolPolymerizationBulkDTO
from .service import styrol_polymerization_bulk_service


router = APIRouter(
    prefix='/styrol-polymerization-bulk',
    tags=['Полимеризация стирола в блоке'],
)


@router.patch('/update')
async def update_styrol_polymerization_bulk(
    new_values: StyrolPolymerizationBulkDTO,
    user: User = Depends(user_service.get_current_user)
) -> StyrolPolymerizationBulkDTO:
    lab_dto = await styrol_polymerization_bulk_service.update_styrol_polymerization_bulk(
        new_values,
        user
    )
    return lab_dto


#TODO добавить роут для добавления ряда в таблице
# по факту, когда пользователь создает пустой ряд на сайте, должен создаться пустой ряд в таблице