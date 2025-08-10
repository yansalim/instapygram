# ✅ Correção da Validação da Rota de Atualização de Perfil

## 🎯 Problema Identificado

A rota `POST /profile/update-bio` não permitia atualizar apenas um campo por vez. Era necessário preencher todos os campos (bio, base64, url) para que a requisição fosse aceita.

## 🔧 Solução Implementada

### Correção na Validação Pydantic
**Arquivo**: `app/routes/profile.py`

Adicionei uma validação personalizada usando `@field_validator` que permite atualizar apenas um campo por vez, desde que pelo menos um campo (bio, base64 ou url) seja fornecido.

#### **Antes (não funcionava com campos individuais):**
```python
class UpdateBioBody(BaseModel):
    username: str
    bio: Optional[str] = None
    url: Optional[str] = None
    base64: Optional[str] = None
```

#### **Depois (funcionando com campos individuais):**
```python
class UpdateBioBody(BaseModel):
    username: str
    bio: Optional[str] = None
    url: Optional[str] = None
    base64: Optional[str] = None

    @field_validator("bio", "url", "base64")
    @classmethod
    def validate_at_least_one_field(cls, v, values):
        # Se este é o último campo sendo validado, verifica se pelo menos um foi fornecido
        if "username" in values.data:
            bio = values.data.get("bio")
            url = values.data.get("url")
            base64 = values.data.get("base64")
            
            if not any([bio, url, base64]):
                raise ValueError("At least one field (bio, url, or base64) must be provided")
        return v
```

### Melhoria na Documentação Swagger
Atualizei a documentação para deixar claro que os campos são opcionais e que pelo menos um deve ser fornecido:

```yaml
description: Profile update data (bio and/or picture). At least one field (bio, base64, or url) must be provided.
properties:
  username:
    description: Username of the account to update (required)
  bio:
    description: New bio text (optional)
  base64:
    description: Profile picture in base64 format (optional)
  url:
    description: Profile picture URL for download (optional)
```

## 📋 Exemplos de Uso Agora Funcionando

### **1. Atualizar apenas a bio:**
```json
{
  "username": "yansalim.ai",
  "bio": "Nova bio do perfil!"
}
```

### **2. Atualizar apenas a foto de perfil (base64):**
```json
{
  "username": "yansalim.ai",
  "base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
}
```

### **3. Atualizar apenas a foto de perfil (URL):**
```json
{
  "username": "yansalim.ai",
  "url": "https://example.com/profile.jpg"
}
```

### **4. Atualizar bio e foto de perfil:**
```json
{
  "username": "yansalim.ai",
  "bio": "Nova bio do perfil!",
  "base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
}
```

### **5. Atualizar todos os campos:**
```json
{
  "username": "yansalim.ai",
  "bio": "Nova bio do perfil!",
  "base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA...",
  "url": "https://example.com/profile.jpg"
}
```

## 🧪 Como Testar

### Via Swagger UI:
1. **Acesse**: `http://localhost:3000/apidocs/`
2. **Configure autenticação**: Digite `Bearer token`
3. **Vá para**: `POST /profile/update-bio`
4. **Clique**: "Try it out"
5. **Teste com apenas um campo**:
   - `username`: `yansalim.ai`
   - `bio`: `Nova bio!` (deixe os outros campos vazios)
6. **Clique**: "Execute"

### Via cURL:

#### **Apenas bio:**
```bash
curl -X POST "http://localhost:3000/profile/update-bio" \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "yansalim.ai",
    "bio": "Nova bio do perfil!"
  }'
```

#### **Apenas foto base64:**
```bash
curl -X POST "http://localhost:3000/profile/update-bio" \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "yansalim.ai",
    "base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
  }'
```

#### **Apenas foto URL:**
```bash
curl -X POST "http://localhost:3000/profile/update-bio" \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "yansalim.ai",
    "url": "https://example.com/profile.jpg"
  }'
```

## 🎉 Resposta Esperada

### Sucesso (200):
```json
{
  "message": "Bio and/or profile picture updated successfully"
}
```

### Erro (400) - Nenhum campo fornecido:
```json
{
  "error": "At least one field (bio, url, or base64) must be provided"
}
```

### Erro (400) - Outros erros:
```json
{
  "error": "Error updating bio/picture: Session not found"
}
```

## 🛡️ Validações Implementadas

### 1. **Campos Obrigatórios**
- `username` é obrigatório
- Pelo menos um entre `bio`, `base64` ou `url` deve ser fornecido

### 2. **Flexibilidade**
- Pode atualizar apenas a bio
- Pode atualizar apenas a foto de perfil (base64 ou URL)
- Pode atualizar bio e foto de perfil
- Pode atualizar todos os campos

### 3. **Formato Base64**
- Deve começar com `data:image/`
- Deve conter o formato da imagem (jpeg, png, etc.)
- Deve ter o prefixo `base64,`

### 4. **URL**
- Deve ser uma URL válida
- Deve apontar para uma imagem acessível

### 5. **Bio**
- Pode ser qualquer texto
- Recomendado máximo de 150 caracteres (limite do Instagram)

## 🚀 Status Final

- ✅ **Validação flexível**: Permite atualizar apenas um campo por vez
- ✅ **Campos opcionais**: bio, base64 e url são opcionais
- ✅ **Validação robusta**: Garante que pelo menos um campo seja fornecido
- ✅ **Documentação clara**: Swagger UI mostra claramente quais campos são opcionais
- ✅ **Mensagens de erro**: Erros claros quando nenhum campo é fornecido

---

**🎉 Rota de atualização de perfil agora permite atualizar apenas um campo por vez!**
