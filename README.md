# 📸 Pipegram (Flask) - API Não Oficial do Instagram

![Logo Pipegram](https://i.imgur.com/kKHUeGh.png)

**Pipegram** é uma API **não oficial** do Instagram desenvolvida para automatizar ações comuns em contas do Instagram, com suporte a **múltiplas sessões simultâneas**. Agora reescrita em Python/Flask usando a biblioteca [instagrapi](https://subzeroid.github.io/instagrapi/).

A documentação interativa está disponível em `/apidocs` quando o serviço estiver rodando.

## 🚀 Tecnologias

- **Python 3.11+**
- **Flask 3.0** com suporte assíncrono
- **[instagrapi](https://subzeroid.github.io/instagrapi/)** - Biblioteca moderna e poderosa para Instagram API
- **Docker & Docker Compose**
- **Swagger/Flasgger** para documentação
- **Pydantic** para validação de dados

## ✅ Funcionalidades

### 📌 Autenticação
- Login com username/password
- Suporte a 2FA
- Sessões persistentes
- Múltiplas contas simultâneas

### 📝 Postagens
- Upload de fotos para feed
- Upload de stories
- Suporte a legendas

### ✉️ Direct Messages
- Envio de mensagens de texto
- Envio de fotos por DM
- Listagem de conversas
- Histórico de mensagens

### 👤 Perfil
- Informações de usuários
- Stories de usuários
- Alteração de foto de perfil
- Edição de bio

## 🛠️ Instalação

### Pré-requisitos
- Docker e Docker Compose
- Make (opcional, para usar o Makefile)

### Configuração Rápida

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd Pipegram
```

2. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. **Inicie a API:**
```bash
# Com Makefile
make up

# Ou com Docker Compose
docker compose up -d
```

4. **Acesse a documentação:**
```
http://localhost:3000/apidocs
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
# Token de administração (obrigatório)
ADMIN_TOKEN=seu_token_aqui

# Porta da API (opcional, padrão: 3000)
PORT=3000
```

### Uso da API

1. **Configure o token de administração no Swagger UI**
2. **Faça login com suas credenciais do Instagram**
3. **Use os endpoints conforme necessário**

## 📚 Documentação da API

### Autenticação

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha",
  "proxy": "http://proxy:porta" // opcional
}
```

#### Verificar Status
```http
GET /auth/status?username=seu_usuario
Authorization: Bearer seu_token_admin
```

### Direct Messages

#### Enviar Mensagem
```http
POST /dm/send
Authorization: Bearer seu_token_admin
Content-Type: application/json

{
  "username": "conta_origem",
  "toUsername": "destinatario",
  "message": "Olá!"
}
```

#### Enviar Foto por DM
```http
POST /dm/send-photo
Authorization: Bearer seu_token_admin
Content-Type: application/json

{
  "username": "conta_origem",
  "toUsername": "destinatario",
  "base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
}
```

#### Listar Conversas
```http
GET /dm/inbox?username=conta_origem
Authorization: Bearer seu_token_admin
```

### Postagens

#### Upload de Foto
```http
POST /post/photo-feed
Authorization: Bearer seu_token_admin
Content-Type: application/json

{
  "username": "conta_origem",
  "caption": "Legenda da foto",
  "base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
}
```

## 🔒 Segurança

- **Token de Administração**: Todas as operações requerem autenticação
- **Sessões Isoladas**: Cada conta tem sua própria sessão
- **Validação de Dados**: Todos os inputs são validados com Pydantic
- **Tratamento de Erros**: Erros são tratados e retornados de forma segura

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro de Login**
   - Verifique se as credenciais estão corretas
   - Algumas contas podem requerer 2FA
   - Use proxy se necessário

2. **Erro de Sessão**
   - Faça login novamente
   - Verifique se a sessão não expirou

3. **Erro de Rate Limit**
   - Aguarde alguns minutos
   - Use proxy para evitar bloqueios

## 📄 Licença

Este projeto é para fins educacionais. Use com responsabilidade e respeite os Termos de Serviço do Instagram.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

- **Documentação**: `/apidocs` quando a API estiver rodando
- **Issues**: Abra uma issue no GitHub
- **Telegram**: [Canal de Suporte](https://t.me/instagrapi)

---

**⚠️ Aviso**: Esta API não é oficial e não tem afiliação com o Instagram/Meta. Use por sua conta e risco.
