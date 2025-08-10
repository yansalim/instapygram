<p align="center">
  <img src="https://i.imgur.com/zbmYf2q.png" width="200" alt="Pipegram Logo" />
</p>

# Pipegram (Flask) 🚀

API REST não oficial do Instagram reescrita em Python com Flask.

Observação importante: esta API não usa a API oficial do Instagram. Utilize por sua conta e risco e respeite os termos de uso da plataforma.

## Principais mudanças

- Backend migrado de Node.js/Express para Python/Flask.
- Documentação via Swagger usando Flasgger disponível em `/apidocs`.
- Docker pronto para uso. Compose expõe a porta 3000.
- Sessões em JSON no diretório `sessions/` (montado via volume).

## Como rodar com Docker

1. Crie um arquivo `.env` na raiz com:

```
ADMIN_TOKEN=seu_token_admin
PORT=3000
```

2. Build e subida com docker-compose:

```
docker compose up --build -d
```

3. Acesse:

- API: `http://localhost:3000/`
- Swagger UI: `http://localhost:3000/apidocs`

Para ver logs:

```
docker compose logs -f api-instagram
```

O volume `./sessions` é montado em `/app/sessions` dentro do container.

## Endpoints (compatíveis com a versão Node)

- Auth
  - POST `/auth/login`
  - POST `/auth/resume`
  - POST `/auth/status`
  - POST `/auth/delete`
  - POST `/auth/import-session`

- Post (requer header Authorization: Bearer <ADMIN_TOKEN>)
  - POST `/post/photo-feed`
  - POST `/post/photo-story`

- DM (requer header Authorization: Bearer <ADMIN_TOKEN>)
  - POST `/dm/send`
  - POST `/dm/inbox`
  - POST `/dm/thread/{threadId}`

- Profile (requer header Authorization: Bearer <ADMIN_TOKEN>)
  - POST `/profile/update-bio`
  - POST `/profile/{targetUsername}`

- Stories (requer header Authorization: Bearer <ADMIN_TOKEN>)
  - POST `/stories`

## Notas sobre implementação Instagram

Esta migração inclui um adaptador `app/services/session_adapter.py` como placeholder. Você pode conectar uma biblioteca Python que forneça acesso ao Instagram privado e implementar os métodos do adaptador. Por padrão, as respostas são simuladas para manter a interface e os contratos da API enquanto você conecta a integração real.

## Desenvolvimento local (opcional)

Se desejar executar fora do Docker:

```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
set FLASK_APP=app
set ADMIN_TOKEN=seu_token_admin
flask run --host=0.0.0.0 --port=3000
```

Para produção no container, usamos gunicorn conforme `Dockerfile`.
