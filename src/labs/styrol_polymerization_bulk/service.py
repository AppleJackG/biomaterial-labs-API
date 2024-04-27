from .repository import StyrolPolymerizationBulkRepository, styrol_polymerization_bulk_repository
from ..generic_lab_table_service import GenericLabTableService
from .schemas import StyrolPolymerizationBulkDTO



class StyrolPolymerizationService(GenericLabTableService[StyrolPolymerizationBulkDTO, StyrolPolymerizationBulkRepository]):
    pass
    
    
styrol_polymerization_bulk_service = StyrolPolymerizationService(
    schema=StyrolPolymerizationBulkDTO,
    repo=styrol_polymerization_bulk_repository
)
