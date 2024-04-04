from pydantic import BaseModel, ConfigDict


class LabSummaryDTO(BaseModel):
    name: str
    status: bool | float


class SummaryTableDTO(BaseModel):
    user_name_surname: str
    lab_summary_list: list[LabSummaryDTO]
    
    model_config = ConfigDict(from_attributes=True)
    
    
