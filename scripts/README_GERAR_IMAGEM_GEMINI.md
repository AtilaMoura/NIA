# Gerar Imagem Gemini

## Como usar

### 1. Criar a lista de imagens

Crie um arquivo JSON com as imagens que quer gerar:

```json
[
  {
    "descricao": "Generate an image. Documentary-style editorial photography, warm golden-hour natural light, church volunteers arranging chairs inside a modest church hall...",
    "modulo": "modulo1",
    "aula": "aula1",
    "topico": "topico1",
    "arquivo": "voluntarios-equipe.png"
  },
  {
    "descricao": "Generate an image. A pastor preaching from a simple wooden pulpit...",
    "modulo": "modulo1",
    "aula": "aula1",
    "topico": "topico2",
    "arquivo": "pregador.png"
  }
]
```

- `descricao`: o que voce quer que o Gemini gere (em ingles)
- `modulo`, `aula`, `topico`: onde a imagem sera salva
- `arquivo`: nome do arquivo da imagem

### 2. Rodar o script

```bash
python scripts/gerar_imagem_gemini.py scripts/imagens_para_gerar.json
```

### 3. Resultado

As imagens sao salvas em:
```
imagem/{modulo}/{aula}/{topico}/{arquivo}
```

Exemplo: `imagem/modulo1/aula1/topico1/voluntarios-equipe.png`

## Notas

- Imagens que ja existem sao puladas automaticamente
- O script reutiliza a mesma conversa do Gemini (acumula as imagens)
- Pode levar ~30-60 segundos por imagem
