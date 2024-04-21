from uuid import UUID

from loguru import logger
from .repository import StyrolPolymerizationBulkRepository, styrol_polymerization_bulk_repository
from .schemas import StyrolPolymerizationBulkDTO
from ...auth.models import User



class StyrolPolymerizationService:
    def __init__(self, repo: StyrolPolymerizationBulkRepository) -> None:
        self.repo = repo
        
    async def create_empty_row(self, row_number: int, user: User) -> StyrolPolymerizationBulkDTO:
        empty_row_orm = await self.repo.create_empty_row(row_number, user.user_id)
        empty_row_dto = StyrolPolymerizationBulkDTO.model_validate(empty_row_orm, from_attributes=True)
        return empty_row_dto
    
    async def update_table(
        self,
        new_values: list[StyrolPolymerizationBulkDTO],
        user: User
    ) -> list[StyrolPolymerizationBulkDTO]:
        lab_orm = await self.repo.update_table(new_values, user.user_id)
        lab_dto: list[StyrolPolymerizationBulkDTO] = []
        for row in lab_orm:
            lab_dto.append(StyrolPolymerizationBulkDTO.model_validate(row, from_attributes=True))
        return lab_dto
    
    async def get_table(self, user_id: UUID) -> list[StyrolPolymerizationBulkDTO]:
        lab_orm = await self.repo.get_table(user_id)
        lab_dto: list[StyrolPolymerizationBulkDTO] = []
        for row in lab_orm:
            lab_dto.append(StyrolPolymerizationBulkDTO.model_validate(row, from_attributes=True))
        lab_dto.sort(key=lambda x: x.number)
        return lab_dto
    
    
styrol_polymerization_bulk_service = StyrolPolymerizationService(styrol_polymerization_bulk_repository)
