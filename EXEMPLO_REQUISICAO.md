# Exemplo de Requisição Correta

## Problema Identificado
A requisição estava retornando erro 401 "Missing authentication token" porque o header de autorização não estava sendo enviado no formato correto.

## Formato Incorreto ❌
```bash
curl -X GET "http://localhost:3000/dm/inbox?username=yansalim.ai" \
  -H "accept: application/json" \
  -H "Authorization: token"
```

## Formato Correto ✅
```bash
curl -X GET "http://localhost:3000/dm/inbox?username=yansalim.ai" \
  -H "accept: application/json" \
  -H "Authorization: Bearer token"
```

## Diferença Importante
- **Incorreto**: `Authorization: token`
- **Correto**: `Authorization: Bearer token`

O middleware de autenticação espera que o token seja precedido pela palavra "Bearer " (com espaço).

## Outros Exemplos de Requisições

### 1. Enviar DM
```bash
curl -X POST "http://localhost:3000/dm/send" \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seu_usuario",
    "toUsername": "destinatario",
    "message": "Olá! Como você está?"
  }'
```

### 2. Obter informações do perfil
```bash
curl -X GET "http://localhost:3000/profile/info/usuario" \
  -H "Authorization: Bearer token"
```

### 3. Fazer login
```bash
curl -X POST "http://localhost:3000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seu_usuario",
    "password": "sua_senha"
  }'
```

## Configuração do Token
O token está configurado no arquivo `.env`:
```
ADMIN_TOKEN=token
```

Se você quiser alterar o token, edite o arquivo `.env` e reinicie a aplicação.
