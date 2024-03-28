from typing import Generic, Type, TypeVar
from uuid import UUID
from sqlalchemy import update
from pydantic import BaseModel

from ..database import Base, session_factory


ModelType = TypeVar("ModelType", bound=Base)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class GenericLabRepository(Generic[ModelType, UpdateSchemaType]):
    
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model
     
    async def update_lab(self, new_values: UpdateSchemaType, user_id: UUID) -> ModelType:
        stmt = (
            update(self.model)
            .where(self.model.user_id == user_id)
            .values(new_values.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        async with session_factory() as session:
            result = await session.execute(stmt)
            lab = result.scalar_one()
            await session.commit()
        return lab
