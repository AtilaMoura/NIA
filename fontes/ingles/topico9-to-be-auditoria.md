# Auditoria — REVISÃO do T9 "To be: I am, you are, he/she/it is"

Conteúdo final: `backend/_criar_topico9_ingles.py` → `_topico9_ingles_final.json` (21 slides, 7 imagens
— 4 mantidas + 3 novas —, 3 fluxos, 9 checkpoints / 13 perguntas). Dossiê: `topico9-to-be.md`.
Versão anterior: `backend/_backup_topico9_2026-10-06.json`. 2026-10-06.

## 1. Lista fechada (checagem automática palavra por palavra)
Script: todo inglês do tópico (termos, `exemplo_en`, colunas, `frase_audio`, opções, enunciados entre
aspas, respostas-modelo — 60 trechos) comparado com a lista do dossiê. Fora da lista: só "to be"
(o nome do verbo) e um trecho em português dentro de enunciado. **0 palavra inglesa fora da lista** ✔.

## 2. Afirmação → fonte → status

| Seção | Afirmação | Fonte | Status |
|---|---|---|---|
| Por que começar | to be = ser e estar; usos (nome, origem, profissão, estado, lugar) | 1 (British Council: exemplos de cada uso) | ✔ |
| I am / you are / he is | formas e contrações | 1 | ✔ |
| Negativa | I'm not, isn't, aren't; "She isn't a student", "We aren't hungry" | 1 | ✔ |
| Negativa | "amn't" não é usado no nível básico | dossiê ("fora do nível A1") | ✔ (dito como "use I'm not") |
| Pergunta | inversão sem palavra auxiliar; "Are you tired? / Is she…?" | 1 | ✔ |
| Respostas curtas | Yes, I am / No, I'm not / Yes, she is / No, she isn't | 1 | ✔ |
| Respostas curtas | sem contração na afirmativa ("Yes, he is", não "Yes, he's") | 2 (Lingolia) | ✔ |
| Idade | "I have 22 years" ✗ × "I am 22 years old" ✓, erro comum de falante de português | 4 | ✔ |
| Fome | "to be hungry" (não "have") | 1 ("We aren't hungry") | ✔ |
| "It's cold today" | precisa do "it" (português diz só "está frio") | observação didática sobre o exemplo | ✔ |
| Diagnóstico | frases reais do dia 0 ("My name is Atila", "I live in Brazil", "I work in technology") | 5 (`dia-00.md`) | ✔ |

## 3. Erros pegos nesta revisão (corrigidos)
- **"It's raining"** (versão anterior): presente contínuo, ainda não ensinado → trocado por "It's cold today".
- **"your"** em exemplos novos ("Is he your brother?", "Are they your friends?"): possessivo é de aula
  futura → trocado por "Is he a teacher?" / "Are they friends?".
- Selo "12 checkpoints" → "13 perguntas" (são 9 checkpoints, 13 perguntas).

## 4. Continuidade (o que o T9 NÃO ensina)
- Nenhum verbo de ação em exemplo novo; "live"/"work" só nas frases reais do diagnóstico, citadas
  como assunto do próximo tópico. Sem do/does/don't, sem -s de 3ª pessoa, sem -ing.

## 5. Respostas salvas do Atila
- As 6 perguntas da versão anterior (ck1_1, ck2_1, ck3_1, ck4_1, ck5_1, ck6_1) ficaram **idênticas**
  (conferido por script) → respostas em `TopicoResposta` continuam válidas. Perguntas novas: ck2_2,
  ck7_1, ck7_2, ck8_1, ck8_2, ck9_1, ck6_2.

## 6. Rascunhos (Gemini/Groq) — o que NÃO entrou

Gemini (`gemini-2.5-flash`): 39 palavras fora da lista fechada (doctor, office, kitchen, "asked" no passado, "It's 3 o'clock"…) — nada entrou; versão final escrita do dossiê. Groq: não tinha terminado na publicação.

## 7. Pedagogia e estrutura
- Novo: negativa completa, respostas curtas, idade, Reflexão "💭 Pra pensar" + Resumo, 2 abertas
  (ck4_1, ck6_2), associar (ck2_2), tf (ck5_1, ck7_2). `validar_topico()` vazio; 0 `None`
  (caderno-escolar); ids únicos.
- Imagens: 4 mantidas (capa, estudante, developer, encaixe — já no estilo flat escuro latão; o
  texto em inglês nelas é intencional e correto, preferência do Atila de 2026-09-17).

**Pendências: 0.** Áudio: 16 narrações em PT (6 reescritas), 16/16 conferidos, pasta nova audio/curso9 criada com scp -r.
