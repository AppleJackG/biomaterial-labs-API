from typing import Generic, Type, TypeVar
from uuid import UUID, uuid4
from sqlalchemy import select, update, insert, delete
from pydantic import BaseModel

from ..database import Base, session_factory


ModelType = TypeVar("ModelType", bound=Base)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class GenericLabTableRepository(Generic[ModelType, UpdateSchemaType]):
    
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model
        
    async def create_empty_row(self, row_number: int, user_id: UUID) -> ModelType:
        stmt = (
            insert(self.model)
            .values(user_id=user_id, number=row_number)
            .returning(self.model)
        )
        async with session_factory() as session:
            result = await session.execute(stmt)
            empty_row_orm = result.scalar_one()
            await session.commit()
        return empty_row_orm
  
    async def update_table(self, new_values: list[UpdateSchemaType], user_id: UUID) -> list[ModelType]:
        lab_orm: list[ModelType] = []
        async with session_factory() as session:
            for row in new_values:
                stmt = (
                    update(self.model)
                    .where(self.model.user_id == user_id)
                    .where(self.model.number == row.number)
                    .values(row.model_dump(exclude_unset=True))
                    .returning(self.model)
                )
                result = await session.execute(stmt)
                lab_row = result.scalar_one()
                lab_orm.append(lab_row)
            await session.commit()
        return lab_orm
    
    async def get_table(self, user_id: UUID) -> list[ModelType]:
        async with session_factory() as session:
            query = select(self.model).where(self.model.user_id == user_id)
            result = await session.execute(query)
            lab_orm = result.scalars()
        return lab_orm
    
    async def delete_row(self, row_number: int, user_id: UUID) -> None:
        stmt = (
            delete(self.model)
            .where(self.model.user_id == user_id)
            .where(self.model.number == row_number)
        )
        async with session_factory() as session:
            await session.execute(stmt)
            await session.commit()
        return None
