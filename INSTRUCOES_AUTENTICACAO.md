# 🔐 Instruções de Autenticação no Swagger UI

## ✅ Problema Corrigido

O erro "Unknown security definition type http" foi corrigido. Agora o Swagger UI está configurado corretamente para aceitar tokens de autenticação.

## 🚀 Como Usar

### 1. Acesse o Swagger UI
```
http://localhost:3000/apidocs/
```

### 2. Configure a Autenticação
1. **Clique no botão "Authorize"** (🔒) no canto superior direito
2. **Aparecerá um popup** com o campo de autenticação
3. **Digite**: `Bearer token` (incluindo a palavra "Bearer")
4. **Clique em "Authorize"**
5. **Clique em "Close"** para fechar o popup

### 3. Teste as Requisições
Agora todas as requisições protegidas incluirão o header:
```
Authorization: Bearer token
```

## 📝 Exemplo Prático

### Teste a requisição que estava falhando:

1. **Vá para**: `GET /dm/inbox`
2. **Clique**: "Try it out"
3. **Adicione o parâmetro**: `username = yansalim.ai`
4. **Clique**: "Execute"

**Resultado esperado**: ✅ Sucesso (sem erro 401)

## 🔍 Verificação

Para verificar se está funcionando:

1. Abra o Swagger UI
2. Configure a autenticação com `Bearer token`
3. Teste uma requisição
4. No console do navegador (F12), verifique se o header está sendo enviado como:
   ```
   Authorization: Bearer token
   ```

## ⚠️ Importante

- **Digite exatamente**: `Bearer token` (com espaço entre "Bearer" e "token")
- **Não esqueça** de clicar em "Authorize" e depois "Close"
- **O token está configurado** no arquivo `.env` como `ADMIN_TOKEN=token`

## 🛠️ Configuração Técnica

**Arquivo**: `app/__init__.py`

```python
"securityDefinitions": {
    "bearerAuth": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header",
        "description": "Authentication token to access protected routes. Use: Bearer token"
    }
}
```

## 🎉 Status Final

- ✅ Aplicação rodando: `http://localhost:3000/`
- ✅ Swagger UI funcionando: `http://localhost:3000/apidocs/`
- ✅ Autenticação corrigida
- ✅ Campo de autenticação aparecendo corretamente
- ✅ Todas as requisições enviam `Authorization: Bearer token`

---

**Agora o Swagger UI está funcionando corretamente! 🎉**
