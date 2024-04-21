from httpx import AsyncClient
from loguru import logger
from src.auth.models import User
from src.labs.styrol_polymerization_bulk.schemas import StyrolPolymerizationBulkDTO


async def test_create_empty_row(ac: AsyncClient, user: User, access_token: str):
    data = {
        "row_number": 1,
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
    