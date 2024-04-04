from uuid import UUID

from .schemas import SummaryTableDTO, LabSummaryDTO
from .repository import SummaryTableRepository
from .models import SummaryTableORM
from .repository import summary_table_repository


class SummaryTableService:
    
    def __init__(self, repo: SummaryTableRepository) -> None:
        self.repo = repo
        
    async def add_user_to_summary_table(self, user_id: UUID) -> SummaryTableORM:
        summaty_table = await self.repo.add_user_to_summary_table(user_id)
        return summaty_table
    
    async def get_summary_table(self) -> list[SummaryTableDTO]:
        summary_table_orm_list = await self.repo.get_summary_table()
        summary_table_dto_list: list[SummaryTableDTO] = []
        for row in summary_table_orm_list:
            summary_table_dto = SummaryTableDTO(
                user_name_surname=f'{row.user.name} {row.user.surname}',
                lab_summary_list=[
                    LabSummaryDTO(
                        name='Полимеризация стирола в массе',
                        status=row.styrol_polymerization_bulk_mark if row.styrol_polymerization_bulk_mark 
                            else row.styrol_polymerization_bulk_status
                    )
                ]
            )
            summary_table_dto_list.append(summary_table_dto)
        return summary_table_dto_list

summary_table_service = SummaryTableService(summary_table_repository)