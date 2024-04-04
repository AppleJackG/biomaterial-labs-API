import asyncio
from .auth.service import user_service
from .auth.schemas import UserCreate
from .auth.models import User
from .labs.styrol_polymerization_bulk.models import StyrolPolymerizationBulkORM


new_user = UserCreate(
    username='AppleJack',
    name='Михаил',
    surname='Козлов',
    role='student',
    password='qwertyASD1'
)


async def add_new_user(new_user: UserCreate):
    user = await user_service.add_new_user(new_user)
    return user


if __name__ == '__main__':
    asyncio.run(add_new_user(new_user)) 
