from typing import Generic, TypeVar, Type
from uuid import UUID
from pydantic import BaseModel

from ..auth.models import User
from.generic_lab_table_repository import GenericLabTableRepository


SchemaType = TypeVar("SchemaType", bound=BaseModel)
RepoType = TypeVar("RepoType", bound=GenericLabTableRepository)


class GenericLabTableService(Generic[SchemaType, RepoType]):
    
    def __init__(self, *, schema: Type[SchemaType], repo: Type[RepoType]) -> None:
        self.repo = repo
        self.schema = schema
        
    async def create_empty_row(self, row_number: int, user: User) -> SchemaType:
        empty_row_orm = await self.repo.create_empty_row(row_number, user.user_id)
        empty_row_dto = self.schema.model_validate(empty_row_orm, from_attributes=True)
        return empty_row_dto
    
    async def update_table(
        self,
        new_values: list[SchemaType],
        user: User
    ) -> list[SchemaType]:
        lab_orm = await self.repo.update_table(new_values, user.user_id)
        lab_dto: list[SchemaType] = []
        for row in lab_orm:
            lab_dto.append(self.schema.model_validate(row, from_attributes=True))
        return lab_dto
    
    async def get_table(self, user_id: UUID) -> list[SchemaType]:
        lab_orm = await self.repo.get_table(user_id)
        lab_dto: list[SchemaType] = []
        for row in lab_orm:
            lab_dto.append(self.schema.model_validate(row, from_attributes=True))
        lab_dto.sort(key=lambda x: x.number)
        return lab_dto
    
    async def delete_row(self, row_number: int, user: User) -> None:
        await self.repo.delete_row(row_number, user.user_id)
        return None
    