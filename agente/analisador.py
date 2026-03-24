from enum import Enum
from typing import Tuple, List
import json
import os


class SentimentType(Enum):
    VERY_POSITIVE = "muito_positivo"
    POSITIVE = "positivo"
    NEUTRAL = "neutro"
    NEGATIVE = "negativo"
    VERY_NEGATIVE = "muito_negativo"


class AnalisadorSentimentos:
    def __init__(self):
        self.carregar_dados()

    def carregar_dados(self):
        try:
            caminho = 'dados/palavras_chave.json'
            if os.path.exists(caminho):
                with open(caminho, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.palavras_positivas = set(dados.get('positivas', []))
                    self.palavras_negativas = set(dados.get('negativas', []))
            else:
                self._usar_palavras_padrao()
        except Exception as e:
            print(f"⚠️ Erro ao carregar dados: {e}")
            self._usar_palavras_padrao()

    def _usar_palavras_padrao(self):
        self.palavras_positivas = {
            'amei', 'adorei', 'perfeito', 'incrível', 'fantástico',
            'lindo', 'melhor', 'sensacional', 'maravilhoso', 'excelente',
            'show', 'top', 'legal', 'bom', 'gostei', 'feliz', 'alegre'
        }
        self.palavras_negativas = {
            'ruim', 'péssimo', 'terrível', 'chato', 'fraco',
            'decepção', 'odeio', 'detesto', 'lixo', 'trash'
        }

    def calcular_sentimento(self, texto: str) -> Tuple[SentimentType, float]:
        texto_lower = texto.lower()
        score = 0
        palavras_totais = len(texto.split())

        for palavra in self.palavras_positivas:
            if palavra in texto_lower:
                score += 1

        for palavra in self.palavras_negativas:
            if palavra in texto_lower:
                score -= 1

        score_norm = max(-1, min(1, score / max(1, palavras_totais / 3)))

        if score_norm >= 0.6:
            tipo = SentimentType.VERY_POSITIVE
        elif score_norm >= 0.2:
            tipo = SentimentType.POSITIVE
        elif score_norm >= -0.2:
            tipo = SentimentType.NEUTRAL
        elif score_norm >= -0.6:
            tipo = SentimentType.NEGATIVE
        else:
            tipo = SentimentType.VERY_NEGATIVE

        return tipo, score_norm

    def extrair_palavras_chave(self, texto: str) -> List[str]:
        palavras = texto.lower().split()
        return [p for p in palavras if len(p) > 3][:5]

    def detectar_tipo(self, texto: str) -> str:
        if '?' in texto:
            return "pergunta"
        elif any(x in texto.lower() for x in ['kkk', 'haha', 'muito engraçado']):
            return "piada"
        else:
            return "outro"
