# Instruções para usar o Swagger UI

## 🔧 Configuração da Autenticação

### Problema Resolvido ✅
O Swagger UI agora está configurado para automaticamente adicionar o prefixo "Bearer " ao token de autenticação.

### Como usar:

1. **Acesse o Swagger UI:**
   ```
   http://localhost:3000/apidocs
   ```

2. **Configure a autenticação:**
   - Clique no botão "Authorize" (🔒) no topo da página
   - No campo de autenticação, digite apenas o token: `token`
   - **NÃO** adicione "Bearer " - o Swagger fará isso automaticamente
   - Clique em "Authorize"

3. **Teste as requisições:**
   - Agora todas as requisições protegidas incluirão automaticamente o header:
   ```
   Authorization: Bearer token
   ```

## 📝 Exemplo Prático

### Antes (❌ Problema):
- Usuário digitava: `Bearer token`
- Swagger enviava: `Authorization: Bearer Bearer token` (duplicado)

### Agora (✅ Solução):
- Usuário digita: `token`
- Swagger envia: `Authorization: Bearer token` (correto)

## 🔍 Verificação

Para verificar se está funcionando:

1. Abra o Swagger UI
2. Configure a autenticação com `token`
3. Teste uma requisição (ex: GET /dm/inbox)
4. No console do navegador (F12), verifique se o header está sendo enviado como:
   ```
   Authorization: Bearer token
   ```

## 🛠️ Configurações Técnicas

### Arquivos modificados:
- `app/__init__.py` - Configuração do Swagger
- `app/templates/swagger-ui.html` - Template personalizado
- `app/middleware.py` - Middleware de autenticação (já estava correto)

### Funcionalidades adicionadas:
- `requestInterceptor` - Adiciona automaticamente "Bearer " ao token
- `onComplete` - Adiciona dicas visuais para o usuário
- Configuração `http` scheme para Bearer tokens

## 🚀 Como testar

1. **Inicie a aplicação:**
   ```bash
   docker compose up --build -d
   ```

2. **Acesse o Swagger:**
   ```
   http://localhost:3000/apidocs
   ```

3. **Configure autenticação:**
   - Clique em "Authorize"
   - Digite: `token`
   - Clique "Authorize"

4. **Teste uma requisição:**
   - Vá para `/dm/inbox`
   - Clique "Try it out"
   - Adicione o parâmetro `username`
   - Clique "Execute"

A requisição deve funcionar sem erro 401! 🎉
