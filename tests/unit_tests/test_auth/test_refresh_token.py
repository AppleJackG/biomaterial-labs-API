from httpx import AsyncClient
from src.config import settings


async def test_refresh_token(ac: AsyncClient, refresh_token):
    response = await ac.post('/auth/refresh', data={'refresh_token': refresh_token})
    assert response.status_code == 200
    assert response.json()['access_token'] is not None
    assert response.json()['refresh_token'] is not None
    assert response.json()['expires_in'] == settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    assert response.json()['token_type'] == 'Bearer'



async def test_refresh_token_fake_token(ac: AsyncClient):
    fake_refresh_token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6I'
        'kpXVCJ9.eyJzdWIiOiI0N2NjMTdmYy0wNGJkLTRjMzUtYTY'
        '5NC1iN2E5NWE3M2RjZTMiLCJyZWZyZXNoX2tleSI6Ijg2NjA'
        '1YzdlLTk4OGMtNDFhZi1hNTliLTg3NDhlZDBiOWVlMiIsImV'
        '4cCI6MTc5OTYyNzM0MiwiaWF0IjoxNzA4NjI2NzM3LCJhY2N'
        'lc3Nfa2V5IjoiODVhMmQ5OGMtODNkMC00ZmI4LWFlOTYtNW'
        'IwMDMyNTViYjZhIn0.YtWtSN7tZBG-OXg4wVUHQNX_4LVX6'
        'iK-Qn-FX2d4TlU')
    response = await ac.post('/auth/refresh', data={'refresh_token': fake_refresh_token})
    assert response.status_code == 403
    assert response.json()['detail'] == 'Invalid token error'