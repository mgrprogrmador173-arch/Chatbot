# 🎬 Bot de Automação de Comentários TikTok

Um agente inteligente que responde automaticamente aos comentários em vídeos do TikTok usando análise de sentimentos e respostas personalizadas.

## ✨ Recursos

- 🤖 Análise automática de sentimentos
- 🎯 Detecção de tipo de comentário
- 💬 Respostas personalizadas
- 🔄 Execução automática via GitHub Actions
- 📊 Logs detalhados
- 🛡️ Modo teste seguro

## 🚀 Setup em 5 minutos

### 1) Adicionar Secrets
No repositório: **Settings > Secrets and variables > Actions**

- `TIKTOK_ACCESS_TOKEN=seu_token_aqui`
- `TIKTOK_CHANNEL_ID=seu_id_aqui`
- `TIKTOK_REFRESH_TOKEN=seu_refresh_token_aqui`
- `MODO_TESTE=True` (mudar para `False` quando estiver pronto)

### 2) Obter credenciais
1. Acesse: <https://developer.tiktok.com>
2. Crie uma aplicação.
3. Solicite acesso à API de comentários.
4. Gere os tokens.

### 3) Pronto
O bot executará automaticamente a cada 6 horas via GitHub Actions.

## 📊 Monitoramento

Vá para **Actions** no repositório para ver os logs de execução.

## 🧪 Modo Teste

Por padrão, o bot está em `MODO_TESTE=True`, o que significa que ele analisará comentários, mas **não publicará respostas** no TikTok.

Para ativar publicação real, altere em Secrets: `MODO_TESTE=False`.

## 📁 Estrutura

```text
tiktok-bot/
├── .github/workflows/deploy.yml
├── agente/
│   ├── analisador.py
│   └── gerador.py
├── integracao/
│   └── tiktok_api.py
├── dados/
│   ├── templates.json
│   └── palavras_chave.json
├── main.py
├── config.py
└── requirements.txt
```

## 🆘 Problemas?

- Token expirado: regenere em <https://developer.tiktok.com>
- Não funciona: verifique se os Secrets estão corretos
- Ver logs: vá em **Actions** e clique no workflow

---

Feito com ❤️ para creators do TikTok.
