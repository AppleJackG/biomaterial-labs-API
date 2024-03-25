# Biomaterial Labs API

Перед запуском поставить в `.env` режим `MODE=PROD` и настроить `CORS_ORIGINS`.

# Запуск контейнера

```console
docker compose -f docker-compose.prod.yml up --build
```
Дождаться запуска контейнера и перейти на http://localhost:3556/docs.


# Авторизация

После логина на `/auth/login` возвращается JSON вида
```
{
    'access_token': 'длинная строка',
    'refresh_token': 'длинная строка',
    'token_type': 'Bearer',
    'expires_in': int  # кол-во секунд, через которое истечет access token
}
```
Оба токена нужно сохранить. Далее, чтобы попасть на защищенный эндпоинт, необходимо в запросе указать заголовок
`Authorization` со значением `'Bearer <access_token>'` (именно слово Bearer пробел access_token).

Действие access токена истекает через *n* минут, после этого нужно обратиться на `/auth/refresh` для получения новой пары 
access и refresh токенов. В этот эндпоинт в заголовке `refresh-token` нужно передать полученный ранее при логине refresh_token. 

Форма для логина как и раньше, т. е. `x-www-form-urlencoded`.