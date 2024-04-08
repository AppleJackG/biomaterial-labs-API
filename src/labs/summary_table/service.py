from uuid import UUID
from fastapi import HTTPException
from fastapi import status

from .schemas import SummaryTableDTO, LabSummaryDTO, LabStatus, LabAfterChangeDTO
from .repository import SummaryTableRepository
from .models import SummaryTableORM, LabNamesEnRu, LabNamesEn
from .repository import summary_table_repository

from loguru import logger

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
            
            lab_summary_list: list[LabSummaryDTO] = []
            for lab_name in LabNamesEnRu:
                lab_summary = LabSummaryDTO(
                    name=lab_name.value,
                    status_or_mark=getattr(row, lab_name.name)
                )
                lab_summary_list.append(lab_summary)
                
            summary_table_dto = SummaryTableDTO(
                user_name_surname=f'{row.user.name} {row.user.surname}',
                lab_summary_list=lab_summary_list
            )
            
            summary_table_dto_list.append(summary_table_dto)
        return summary_table_dto_list

    async def change_lab_status(self, user_id: UUID, lab_name: LabNamesEn) -> LabStatus:
        summary_table_orm = await self.repo.get_summary_table_for_user(user_id)
        current_status: str = getattr(summary_table_orm, lab_name.value)
        logger.debug(current_status)
        logger.debug(self.is_float(current_status))
        if self.is_float(current_status):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Работа уже оценена'
            )
        elif current_status == LabStatus.uncompleted:
            new_status = LabStatus.unrated
        else:
            new_status = LabStatus.uncompleted
        summary_table_orm = await self.repo.change_lab_status(user_id, lab_name.value, new_status.value)
        changed_lab = LabAfterChangeDTO.model_validate(summary_table_orm, from_attributes=True)
        return changed_lab

    async def grade_work(self, user_id: UUID, lab_name: LabNamesEn, mark: float) -> LabAfterChangeDTO:
        summary_table_orm = await self.repo.grade_work(user_id, lab_name.value, mark)
        changed_lab = LabAfterChangeDTO.model_validate(summary_table_orm, from_attributes=True)
        return changed_lab
    
    @staticmethod
    def is_float(value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False
    

summary_table_service = SummaryTableService(summary_table_repository)