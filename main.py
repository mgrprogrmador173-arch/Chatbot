#!/usr/bin/env python3
import argparse
import logging
import os
import sys
from datetime import datetime

from config import *
from agente.analisador import AnalisadorSentimentos
from agente.gerador import GeradorRespostas
from integracao.tiktok_api import APITikTok

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BotTikTok:
    def __init__(self):
        logger.info("=" * 50)
        logger.info("🤖 Inicializando Bot TikTok...")
        logger.info("=" * 50)

        self.api = APITikTok(TIKTOK_ACCESS_TOKEN, TIKTOK_CHANNEL_ID)
        self.analisador = AnalisadorSentimentos()
        self.gerador = GeradorRespostas()

        self.comentarios_respondidos = set()
        logger.info("✓ Bot iniciado com sucesso!")

    def processar_video(self, video_id: str):
        logger.info(f"\n📺 Processando vídeo: {video_id}")

        comentarios = self.api.obter_comentarios(video_id)

        if not comentarios:
            logger.info("ℹ️  Nenhum comentário novo encontrado")
            return

        logger.info(f"📝 Encontrados {len(comentarios)} comentários")

        for comentario in comentarios:
            self.processar_comentario(comentario)

    def processar_comentario(self, comentario: dict):
        id_comentario = comentario.get('id')
        texto = comentario.get('text', '')
        autor = comentario.get('author_name', 'Usuário')

        if id_comentario in self.comentarios_respondidos:
            return

        logger.info(f"\n💬 Novo comentário de @{autor}")
        logger.info(f"   📄 Texto: {texto[:60]}...")

        sentimento, score = self.analisador.calcular_sentimento(texto)
        logger.info(f"   😊 Sentimento: {sentimento.value} (score: {score:.2f})")

        tipo = self.analisador.detectar_tipo(texto)
        logger.info(f"   🏷️  Tipo: {tipo}")

        resposta = self.gerador.gerar_resposta(tipo, autor)
        resposta = self.gerador.validar_comprimento(resposta)

        logger.info(f"   💬 Resposta: {resposta}")

        if AUTO_PUBLICAR and not MODO_TESTE:
            sucesso = self.api.publicar_resposta(id_comentario, resposta)
            if sucesso:
                logger.info("   ✅ Resposta publicada!")
                self.comentarios_respondidos.add(id_comentario)
        elif MODO_TESTE:
            logger.info("   [TESTE] Resposta não será publicada no TikTok")
            self.comentarios_respondidos.add(id_comentario)

    def executar_ciclo(self):
        try:
            logger.info(f"\n{'=' * 50}")
            logger.info(f"🔄 Iniciando ciclo em {datetime.now().strftime('%H:%M:%S')}")
            logger.info(f"{'=' * 50}")

            videos = self.api.obter_videos_recentes(limite=3)

            if not videos:
                logger.warning("⚠️  Nenhum vídeo encontrado")
                return

            for video in videos:
                self.processar_video(video['id'])

            logger.info("\n✅ Ciclo concluído com sucesso!\n")

        except Exception as e:
            logger.error(f"❌ Erro no ciclo: {e}", exc_info=True)


def main():
    parser = argparse.ArgumentParser(description='Bot TikTok Automação')
    parser.add_argument('--ciclo-unico', action='store_true',
                        help='Executar apenas um ciclo e sair')
    args = parser.parse_args()

    print("""
    ╔════════════════════════════════════════════╗
    ║   🎬 AGENTE DE AUTOMAÇÃO TIKTOK 🤖        ║
    ║                                            ║
    ║   Respondendo comentários automaticamente! ║
    ╚════════════════════════════════════════════╝
    """)

    bot = BotTikTok()

    try:
        if args.ciclo_unico:
            logger.info("🚀 Executando ciclo único...")
            bot.executar_ciclo()
            logger.info("✓ Finalizando...")
        else:
            logger.info("🚀 Iniciando execução contínua...")
            if MODO_TESTE:
                logger.info("⚠️  MODO TESTE ATIVADO")

            import schedule
            import time

            schedule.every(INTERVALO_VERIFICACAO).seconds.do(bot.executar_ciclo)

            logger.info(f"⏰ Bot verificará comentários a cada {INTERVALO_VERIFICACAO}s")

            while True:
                schedule.run_pending()
                time.sleep(10)

    except KeyboardInterrupt:
        logger.info("\n⏹️  Bot interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
