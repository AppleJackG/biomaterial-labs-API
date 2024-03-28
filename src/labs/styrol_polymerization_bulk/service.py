from .repository import StyrolPolymerizationBulkRepository, styrol_polymerization_bulk_repository
from .schemas import StyrolPolymerizationBulkDTO
from ...auth.models import User



class StyrolPolymerizationService:
    def __init__(self, repo: StyrolPolymerizationBulkRepository) -> None:
        self.repo = repo
        
    async def update_styrol_polymerization_bulk(
        self,
        new_values: StyrolPolymerizationBulkDTO,
        user: User
    ) -> StyrolPolymerizationBulkDTO:
        lab_orm = await self.repo.update_lab(new_values, user.user_id)
        lab_dto = StyrolPolymerizationBulkDTO.model_validate(lab_orm, from_attributes=True)
        return lab_dto
    
    
styrol_polymerization_bulk_service = StyrolPolymerizationService(styrol_polymerization_bulk_repository)
