from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class LabStatus(str, Enum):
    uncompleted = "uncompleted"
    unrated = "unrated"


class LabSummaryDTO(BaseModel):
    name: str
    status_or_mark: LabStatus | float
    
    model_config = ConfigDict(from_attributes=True)
    

class LabAfterChangeDTO(BaseModel):
    user_id: UUID
    styrol_polymerization_bulk: LabStatus | float
    
    model_config = ConfigDict(from_attributes=True)


class SummaryTableDTO(BaseModel):
    user_name_surname: str
    lab_summary_list: list[LabSummaryDTO]
    
    model_config = ConfigDict(from_attributes=True)
    