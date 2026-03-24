import json
import random
import os


class GeradorRespostas:
    def __init__(self):
        self.carregar_templates()

    def carregar_templates(self):
        try:
            caminho = 'dados/templates.json'
            if os.path.exists(caminho):
                with open(caminho, 'r', encoding='utf-8') as f:
                    self.templates = json.load(f)
            else:
                self.templates = self._templates_padrao()
        except Exception:
            self.templates = self._templates_padrao()

    def _templates_padrao(self) -> dict:
        return {
            "pergunta": [
                "🤔 Ótima pergunta! Vou responder nos próximos vídeos!",
                "💡 Que dúvida interessante! Muito bom!",
                "👉 Entendi sua pergunta! Obrigado por perguntar!",
                "🧠 Excelente questionamento! Vou considerar!"
            ],
            "piada": [
                "😂 Sua criatividade é top demais!",
                "🤣 Morri aqui! Muito bom!",
                "😅 Kkkkk sua energia é contagiante!",
                "😆 Você é engraçado demais!"
            ],
            "outro": [
                "🙏 Obrigado pelo comentário! Fico feliz!",
                "😊 Muito obrigado por acompanhar!",
                "❤️ Valeu mesmo! Significa muito!",
                "👏 Seu apoio é incrível! Obrigado!"
            ]
        }

    def gerar_resposta(self, tipo: str, autor: str) -> str:
        if tipo in self.templates:
            resposta = random.choice(self.templates[tipo])
        else:
            resposta = random.choice(self.templates["outro"])

        return resposta.replace("[AUTOR]", f"@{autor}")

    def validar_comprimento(self, texto: str, max_chars: int = 200) -> str:
        if len(texto) > max_chars:
            return texto[:max_chars - 3] + "..."
        return texto
