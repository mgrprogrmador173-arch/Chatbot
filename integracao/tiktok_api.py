import requests
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class APITikTok:
    def __init__(self, access_token: str, channel_id: str):
        self.access_token = access_token
        self.channel_id = channel_id
        self.base_url = "https://open.tiktokapis.com/v1"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        self.simulado = not access_token

    def obter_videos_recentes(self, limite: int = 5) -> List[Dict]:
        if self.simulado:
            logger.info("📺 [SIMULADO] Retornando vídeos de teste")
            return [{"id": "video_test_001", "title": "Vídeo de Teste"}]

        try:
            endpoint = f"{self.base_url}/video/list"
            params = {"fields": "id,title", "max_count": limite}

            resposta = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            resposta.raise_for_status()
            return resposta.json().get('data', [])
        except Exception as e:
            logger.error(f"❌ Erro ao obter vídeos: {e}")
            return []

    def obter_comentarios(self, video_id: str) -> List[Dict]:
        if self.simulado:
            logger.info(f"💬 [SIMULADO] Retornando comentários para {video_id}")
            return [
                {
                    "id": "comment_001",
                    "text": "Amei muito! Excelente conteúdo! 🔥",
                    "author_name": "usuario_teste_1"
                },
                {
                    "id": "comment_002",
                    "text": "Como você faz para editar assim?",
                    "author_name": "usuario_teste_2"
                }
            ]

        try:
            endpoint = f"{self.base_url}/comment/list"
            params = {
                "video_id": video_id,
                "fields": "id,text,author_name",
                "max_count": 20
            }

            resposta = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            resposta.raise_for_status()
            return resposta.json().get('data', [])
        except Exception as e:
            logger.error(f"❌ Erro ao obter comentários: {e}")
            return []

    def publicar_resposta(self, comentario_id: str, texto: str) -> bool:
        if self.simulado:
            logger.info(f"✅ [SIMULADO] Resposta publicada: {texto}")
            return True

        try:
            endpoint = f"{self.base_url}/comment/reply"
            payload = {"comment_id": comentario_id, "content": texto}

            resposta = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            resposta.raise_for_status()
            logger.info(f"✓ Resposta publicada para {comentario_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao publicar: {e}")
            return False
