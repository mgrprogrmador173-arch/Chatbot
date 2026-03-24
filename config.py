import os
from dotenv import load_dotenv

load_dotenv()


TIKTOK_ACCESS_TOKEN = os.getenv('TIKTOK_ACCESS_TOKEN', '')
TIKTOK_CHANNEL_ID = os.getenv('TIKTOK_CHANNEL_ID', '')
TIKTOK_REFRESH_TOKEN = os.getenv('TIKTOK_REFRESH_TOKEN', '')


INTERVALO_VERIFICACAO = 300
LIMITE_CARACTERES_RESPOSTA = 200
AUTO_PUBLICAR = os.getenv('AUTO_PUBLICAR', 'False') == 'True'


RESPONDER_APENAS_PERGUNTAS = False
FILTRO_SPAM = True
SCORE_MINIMO_CONFIANCA = 0.5


LOG_LEVEL = "INFO"
LOG_FILE = "logs/agente.log"


DEBUG = os.getenv('DEBUG', 'False') == 'True'
MODO_TESTE = os.getenv('MODO_TESTE', 'True') == 'True'


print(f"""
╔════════════════════════════════════════╗
║   Configurações Carregadas             ║
║   MODO_TESTE: {MODO_TESTE}             ║
║   AUTO_PUBLICAR: {AUTO_PUBLICAR}       ║
╚════════════════════════════════════════╝
""")
