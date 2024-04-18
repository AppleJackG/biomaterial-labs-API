import asyncio
import os
from ..auth.service import user_service
from ..labs.summary_table.service import summary_table_service
from ..auth.schemas import UserCreate, UserSchema, RolesEnum

from ..auth.models import User
from ..labs.styrol_polymerization_bulk.models import StyrolPolymerizationBulkORM


super_user = UserCreate(
    username='AppleJack',
    name='Михаил',
    surname='Козлов',
    role=RolesEnum.student,
    password=os.getenv('SUPERUSER_PASSWORD')
)


async def create_superuser(new_user: UserCreate) -> UserSchema:
    user = await user_service.add_new_user(new_user)
    # await summary_table_service.add_user_to_summary_table(user.user_id
    await user_service.create_superuser(user.username)
    return user


# async def create_superuser(username: str) -> UserSchema:
#     user = await user_service.create_superuser(username)
#     return user


if __name__ == '__main__':
    # asyncio.run(add_new_user(apple_jack))
    asyncio.run(create_superuser(super_user))
