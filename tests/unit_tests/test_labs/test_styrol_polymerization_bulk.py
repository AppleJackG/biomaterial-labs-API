from typing import AsyncGenerator
from httpx import AsyncClient
import pytest_asyncio
from loguru import logger
from src.auth.models import User
from src.labs.styrol_polymerization_bulk.schemas import StyrolPolymerizationBulkDTO
from src.labs.styrol_polymerization_bulk.models import StyrolPolymerizationBulkORM
from src.database import session_factory


@pytest_asyncio.fixture(autouse=True)
async def empty_row(user: User) -> AsyncGenerator[StyrolPolymerizationBulkORM, None]:
    empty_row = StyrolPolymerizationBulkORM()
    empty_row.user_id = user.user_id
    empty_row.number = 1
    async with session_factory() as session:
        session.add(empty_row)
        await session.commit()
        await session.refresh(empty_row)
    yield
    async with session_factory() as session:
        await session.delete(empty_row)
        await session.commit()


@pytest_asyncio.fixture(scope="function")
async def get_sample_values() -> AsyncGenerator[dict[str, float | None], None]:
    sample_lab_values = {
        "number": 1,
        "load_monomer_g": 1.5,
        "load_monomer_mole": 2,
        "load_monomer_mole_g": 3,
        "load_initiator_g": 4,
        "load_initiator_mole": 10,
        "load_initiator_mole_g": None,
        "temperature": 200,
        "time": 0.5,
        "polymer_yield_g": 1,
        "polymer_yield_percent": 3,
        "polymerization_rate_percent": 0.5,
        "polymerization_rate_mole": 0.33,
        "polymer_characteristics_viscosity": 123.55,
        "polymer_characteristics_mol_mass": 13486957
    }
    sample_lab_values_dto = StyrolPolymerizationBulkDTO(**sample_lab_values)
    yield sample_lab_values_dto.model_dump()


async def test_create_empty_row(ac: AsyncClient, access_token: str):
    data = {
        "row_number": 5,
    }
    response = await ac.post(
        '/labs/styrol-polymerization-bulk/create-empty-row',
        params=data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    response_json: dict = response.json()
    logger.debug(response_json)
    assert response.status_code == 200
    assert response_json.keys() == StyrolPolymerizationBulkDTO.model_fields.keys()


async def test_update_table(
    ac: AsyncClient, 
    access_token: str, 
    get_sample_values: dict[str, float | None]
):
    data = [get_sample_values]
    response = await ac.patch(
        '/labs/styrol-polymerization-bulk/',
        json=data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json() == [get_sample_values]
    assert response.json()[0].keys() == StyrolPolymerizationBulkDTO.model_fields.keys()
    

async def test_get_table_as_student(ac: AsyncClient, access_token: str):
    response = await ac.get(
        '/labs/styrol-polymerization-bulk/get-as-student',
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()[0].keys() == StyrolPolymerizationBulkDTO.model_fields.keys()  
    assert len(response.json()) == 1
  
    
async def test_get_table_as_teacher(ac: AsyncClient, access_token_teacher: str, user: User):
    response = await ac.get(
        '/labs/styrol-polymerization-bulk/get-as-teacher',
        params={"user_id": user.user_id},
        headers={"Authorization": f"Bearer {access_token_teacher}"}
    )
    assert response.status_code == 200
    assert response.json()[0].keys() == StyrolPolymerizationBulkDTO.model_fields.keys()  
    assert len(response.json()) == 1
    