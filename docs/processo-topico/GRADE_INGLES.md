# Grade do Inglês (curso 9): do zero ao B1, com mapa de evolução

**Status:** APROVADA pelo Atila (2026-10-07). **Fase 1 criada na produção** (script
`backend/_criar_grade_ingles_fase1.py`): M0 (módulo id 51, tópicos 194–199), M1 Aulas 2–3 (módulo 34,
tópicos 200–207) e M2 (módulo id 52, tópicos 208–216) = 23 tópicos vazios, todos na `FILA.md`.
**Numeração no app:** o banco não aceita módulo 0, então M0 = "Módulo 1", M1 Fundamentos = "Módulo 2",
M2 = "Módulo 3", e assim por diante (Mn = Módulo n+1). Em aberto: onde o M-V (treino) aparece
(um módulo no fim ou uma aula de treino depois de cada módulo); os módulos M3 em diante são criados aos poucos.
Pedido de origem: `curso de obreiro/anotação.md` (2026-10-07). Regras de escrita: [ingles.md](ingles.md).

## Princípios (do pedido do Atila)

1. **Primeiro entender a aula, depois conversar.** Antes de qualquer conversa em inglês: saber
   dizer "não entendi", pedir pra repetir, perguntar "como se fala isso?" e "o que é isso?".
   É o **Módulo 0**. O próprio CEFR descreve o A1 assim: o aluno consegue interagir *"provided the
   other person is prepared to repeat or rephrase things at a slower rate of speech and help me
   formulate what I'm trying to say"* (fonte 1).
2. **Base sólida em temas do dia a dia:** números, horas, dias, semana, mês, rotina, situações.
   As 4 habilidades em todo módulo: **ouvir** (ditado, áudio en-US), **ler**, **escrever**
   (perguntas abertas) e **falar** (repetição em voz alta; depois, conversa com IA).
3. **Muito exercício.** Toda aula termina com "Prática" e "Juntando tudo". Além disso há um
   **módulo só de treino de vocabulário** (M-V), com uma aula por módulo da base.
4. **Lista fechada acumulada.** Cada tópico tem a lista fechada de palavras do dossiê
   (`fontes/ingles/`). A soma das listas dos tópicos concluídos é **"o que eu já sei"**. Ela
   alimenta a prática de conversa com IA (só com palavras conhecidas, a IA corrigindo) e o
   contador do mapa de evolução.
5. **Sem pular degrau.** Nenhuma pergunta usa gramática ou palavra que ainda não foi ensinada
   (lição do T4/T27).

## Visão geral

| Nível | Módulo | Aulas | Tópicos |
|---|---|---|---|
| A1 | **M0** Sobrevivência na aula | 2 | 6 |
| A1 | **M1** Fundamentos (já existe: "Fundamentos I") | 3 | 12 (4 prontos) |
| A1 | **M2** Números, horas e calendário | 3 | 9 |
| A1 | **M3** Meu dia, minha família | 3 | 9 |
| A1 | **M4** Onde estou: casa e cidade | 2 | 6 |
| A1 | **M5** Agora e o que eu sei fazer | 2 | 6 |
| A2 | **M6** O passado: contar o que aconteceu | 4 | 12 |
| A2 | **M7** Situações do dia a dia | 4 | 12 |
| A2 | **M8** Futuro e planos | 2 | 6 |
| A2 | **M9** Comparar, descrever e opinar | 2 | 6 |
| B1 | **M10** Experiências e novidades | 2 | 6 |
| B1 | **M11** Regras, conselhos e hipóteses | 3 | 9 |
| B1 | **M12** Contar, resumir e argumentar | 3 | 9 |
| todos | **M-V** Treino de vocabulário | 13 | 13 |
| opcional | **M-T** Inglês para tecnologia (guardado: T8) | 1+ | depois do A2 |
| | **Total** | | **~121 tópicos** (117 novos) |

Ritmo de referência: 1 tópico por dia útil ≈ 6 meses. O A1 inteiro (M0–M5 + treino) tem
~54 tópicos ≈ 2,5 meses.

## Grade detalhada

Padrão de aula (o mesmo da Aula 1, que funcionou): tópicos de explicação → **Prática** →
**Juntando tudo** (síntese sem pista). Títulos provisórios: o dossiê de cada tópico ajusta.

### A1: Base

**M0. Sobrevivência na aula**
*"Eu consigo pedir ajuda em inglês quando não entendo."*
- Aula 1. Quando eu não entendo
  1. "Sorry, I don't understand" · "Can you repeat that, please?" · "More slowly, please"
  2. "How do you say … in English?" · "What does … mean?" · "How do you spell …?" (+ o alfabeto)
  3. Prática: pedir ajuda numa conversa curta
- Aula 2. Entendendo o professor (e a IA)
  4. As instruções que aparecem em todo exercício: read, listen, write, answer, choose, match, repeat
  5. Confirmar o que entendeu: a técnica **"You mean…? / Exactly"** (vem do T7 guardado)
  6. Juntando tudo: uma "aula" inteira em inglês simples, entendendo tudo

> Observação: essas frases entram como **bloco fixo** (*chunk*), sem explicar a gramática por
> trás ("can", "does"). A gramática vem depois, no lugar dela.

**M1. Fundamentos** (módulo existente "Fundamentos I", id 34)
*"Eu consigo me apresentar e falar de mim no presente."*
- Aula 1. To be & verbos normais: **T9, T10, T11, T27 ✅ prontos**
- Aula 2. He/she/it + -s
  1. He works, she lives: o -s da 3ª pessoa (e a grafia: -es, -ies)
  2. Doesn't: a negativa com he/she/it
  3. Prática · 4. Juntando tudo
- Aula 3. Fazendo perguntas
  1. "Do you…? / Does she…?" e as respostas curtas
  2. Palavras de pergunta: what, where, who, when, how, how old
  3. Prática · 4. Juntando tudo: uma entrevista de apresentação

**M2. Números, horas e calendário**
*"Eu consigo falar números, horas e datas, e entender quando alguém fala."*
- Aula 1. Números
  1. 0 a 20 · 2. 20 a 1000 (preços, idade, telefone) · 3. Prática com ditado de números
- Aula 2. Horas
  4. "What time is it?": o'clock, half past, quarter past/to · 5. a.m./p.m., morning/afternoon/evening/night · 6. Prática
- Aula 3. Dias, semanas, meses e datas
  7. Dias da semana e meses · 8. Números ordinais e datas (first, second… thirty-first) · 9. Preposições de tempo **at / in / on**

**M3. Meu dia, minha família**
*"Eu consigo descrever minha rotina e as pessoas da minha casa."*
- Aula 1. Rotina
  1. Verbos da rotina (wake up, get up, have breakfast, go to work…) · 2. Com que frequência: always, usually, sometimes, never · 3. Juntando tudo: "my day"
- Aula 2. Pessoas
  4. Família e amigos · 5. Possessivos: my/your/his/her e o **'s** ("Atila's car") · 6. Prática
- Aula 3. Gostos
  7. Like / love / hate + substantivo · 8. Comida e bebida do dia a dia · 9. Juntando tudo

**M4. Onde estou: casa e cidade**
*"Eu consigo dizer onde as coisas estão e pedir uma direção simples."*
- Aula 1. Casa
  1. **There is / there are** · 2. Preposições de lugar: in, on, at, under, next to · 3. Prática
- Aula 2. Cidade
  4. Lugares da cidade (bank, pharmacy, supermarket…) · 5. Pedir e entender uma direção · 6. Juntando tudo

**M5. Agora e o que eu sei fazer**
*"Eu consigo dizer o que está acontecendo agora e o que eu sei (ou não) fazer."*
- Aula 1. Agora
  1. Presente contínuo: "I'm working" · 2. Presente simples × contínuo · 3. Prática
- Aula 2. Habilidade e pedido
  4. Can / can't (habilidade) · 5. "Can you…? / Could you…?" (pedido educado) · 6. Juntando tudo

### A2: Usuário básico

**M6. O passado: contar o que aconteceu**
*"Eu consigo contar o que fiz ontem."*
- Aula 1. Was / were · Aula 2. Passado regular (-ed) e a pronúncia do -ed ·
  Aula 3. Passado irregular (os 30 mais usados) + did/didn't/"Did you…?" ·
  Aula 4. **Prática de escuta: "Falando sobre o meu dia"** (o vídeo do T7 guardado, aqui no lugar certo) + passado contínuo

**M7. Situações do dia a dia** (temas da lista A2 Key, fonte 2)
*"Eu consigo me virar numa loja, num restaurante, numa viagem e no médico."*
- Aula 1. Compras: contável/incontável, how much / how many, preços, roupas ·
  Aula 2. Restaurante e comida: pedir, "I'd like…", a conta ·
  Aula 3. Viagem e transporte: passagem, horário, hotel ·
  Aula 4. Saúde e serviços: o corpo, sintomas, farmácia, banco

**M8. Futuro e planos**
*"Eu consigo falar dos meus planos e combinar um encontro."*
- Aula 1. Going to (planos) × will (decisão na hora, previsão) ·
  Aula 2. Presente contínuo pra compromisso marcado + convidar, aceitar e recusar

**M9. Comparar, descrever e opinar**
*"Eu consigo comparar coisas e dar uma opinião simples."*
- Aula 1. Comparativo e superlativo · Aula 2. Adjetivos -ed × -ing (bored/boring), sentimentos, "I think…"

### B1: Usuário independente

**M10. Experiências e novidades**
*"Eu consigo falar do que já fiz na vida."*
- Aula 1. Present perfect: ever / never, "Have you ever…?" ·
  Aula 2. Just / yet / already / still, e present perfect × passado simples

**M11. Regras, conselhos e hipóteses**
*"Eu consigo dar conselho, falar de regra e imaginar situações."*
- Aula 1. Must / have to / should / can (permissão e obrigação) ·
  Aula 2. Condicionais 0, 1 e 2 ("If it rains…", "If I had…") ·
  Aula 3. Used to (hábitos do passado) e os phrasal verbs mais comuns

**M12. Contar, resumir e argumentar**
*"Eu consigo contar uma história, repassar o que alguém disse e defender uma ideia."*
- Aula 1. Discurso indireto ("He said that…") · Aula 2. Voz passiva ·
  Aula 3. Ligar ideias (although, despite, because, so) + escrever um e-mail/mensagem completo

### M-V. Treino de vocabulário (módulo só de exercícios)
Uma aula por módulo da base (M0 a M12), **sem teoria nova**: só exercício (lacuna, associar,
ditado, ouvir e escolher, escrever a frase) com as palavras da lista fechada daquele módulo.
Libera quando o módulo correspondente termina. É o lugar de **revisitar** palavra antiga.

### Guardados (curso 14). Onde cada um entra
| Guardado | Entra em | Quando |
|---|---|---|
| T7 "Falando sobre o meu dia" | M6 Aula 4 (escuta do passado) + técnica "You mean…?" no M0 | ao chegar no M6 |
| T8 "Inglês para prompts" | M-T opcional | depois do A2 (M9) |
| T6 "My Way" | Atila decide (essa ou outra música) | sem data |

## Mapa de evolução

Cada módulo tem uma frase **"Eu consigo…"** (as frases em itálico acima), alinhada às faixas do CEFR:

| Nível | O que o CEFR diz (fonte 1, resumido) | Módulos |
|---|---|---|
| A1 | Entender palavras familiares faladas devagar; responder perguntas simples se a pessoa repetir; falar de onde mora e de quem conhece; preencher um formulário | M0–M5 |
| A2 | Entender o essencial de mensagens curtas (compras, trabalho, região); trocas sociais curtas; descrever família, rotina, trabalho atual; escrever bilhete e mensagem curta | M6–M9 |
| B1 | Entender o principal de fala clara sobre trabalho e lazer; se virar em viagem; conversar sem preparo sobre temas familiares; contar experiências; escrever texto simples e ligado | M10–M12 |

O mapa mostra, por módulo: tópicos concluídos, provas aprovadas, a frase "Eu consigo…" marcada
quando o módulo fecha e o **contador de palavras conhecidas** (soma das listas fechadas). Onde ele
mora (página do aluno no Emaús ou página visual à parte) se decide depois de aprovar a grade.

## O que vem depois desta grade (não faz parte dela)
- **Prática de conversa com IA** limitada ao "que eu já sei" (princípio 4). Precisa das listas
  fechadas: dá pra começar já no fim do M1.
- **Provas:** seguem o `PROVA.md` (a escrever). No Inglês, a prova cobra as 4 habilidades.

## Fontes

| # | Fonte | O que sustenta |
|---|---|---|
| 1 | Council of Europe / Europass, *CEFR Self-assessment grid* (A1–C2). https://europass.europa.eu/system/files/2020-05/CEFR%20self-assessment%20grid%20EN.pdf | Faixas A1/A2/B1 por habilidade; o A1 "repeat or rephrase" (justifica o M0); mapa de evolução |
| 2 | Cambridge English, *A2 Key Vocabulary List* (versão de agosto de 2025). https://www.cambridgeenglish.org/images/506886-a2-key-2020-vocabulary-list.pdf | Appendix 1: números até 1000, ordinais até 31st, dias, meses, estações, países/nacionalidades (M2). Appendix 2: listas por tema (Time, Family and Friends, Food and Drink, Shopping, Travel and Transport, Health, Services, House and Home, Places: Town and City, Work and Jobs…), base do M3, M4 e M7 |
| 3 | British Council LearnEnglish, gramática A1-A2. https://learnenglish.britishcouncil.org/free-resources/grammar/a1-a2 | No A1-A2: to be, present simple, question forms, there is/are, prepositions of place e time, possessive 's, articles, countable/uncountable, comparatives, past continuous × past simple, -ed/-ing |
| 4 | British Council LearnEnglish, gramática B1-B2. https://learnenglish.britishcouncil.org/free-resources/grammar/b1-b2 | No B1-B2: present perfect (just/yet/already), future forms (will/going to/present continuous), modals of permission/obligation, conditionals 0/1/2, used to, passives, reported speech, phrasal verbs, although/despite |
| 5 | British Council TeachingEnglish, *Useful learner phrases*. https://africa.teachingenglish.org.uk/classroom/activities/useful-learner-phrases | Frases do M0: "Can you repeat that?", "How do you say … in English?", "I'm sorry, I don't understand.", "What does … mean?", "How do I spell …?" |
| 6 | Dossiês do curso (`fontes/ingles/topico9…27`) | O que a Aula 1 já ensinou e o que ficou proibido (he/she/it + -s, doesn't, "Do you…?", -ing, números, horas, dias) → ordem do M1 Aulas 2–3 e do M2 |

**A conferir no dossiê de cada tópico (não verificado aqui):** o nível exato de present continuous,
can, going to e past simple no English Grammar Profile (Cambridge). As fontes 3 e 4 só confirmam a
faixa (A1-A2 ou B1-B2) dos itens listados acima. A ordem dentro da faixa é decisão didática minha,
pra o Atila aprovar.

## Depois de aprovar
1. Criar no curso 9 os módulos/aulas/tópicos vazios (M0, M1 Aulas 2–3 e M2 primeiro; o resto aos poucos).
2. M0 vem **antes** do M1 na ordem do curso (module_index), mesmo sendo criado depois.
3. Colocar os tópicos na `FILA.md`, intercalados com os outros cursos.
4. Abrir a pasta `fontes/ingles/` pra cada tópico novo, seguindo o `ingles.md`.
