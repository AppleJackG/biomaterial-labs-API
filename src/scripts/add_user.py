import asyncio
from ..auth.service import user_service
from ..labs.summary_table.service import summary_table_service
from ..auth.schemas import UserCreate, UserSchema

from ..auth.models import User
from ..labs.styrol_polymerization_bulk.models import StyrolPolymerizationBulkORM


new_user = UserCreate(
    username='aple',
    name='Михаил',
    surname='Козлов',
    role='student',
    password='qwertyASD1'
)


async def add_new_user(new_user: UserCreate) -> UserSchema:
    user = await user_service.add_new_user(new_user)
    await summary_table_service.add_user_to_summary_table(user.user_id)
    return user


if __name__ == '__main__':
    asyncio.run(add_new_user(new_user)) 
