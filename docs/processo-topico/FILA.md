# Fila de criação de tópicos

A tarefa diária (`scripts/tarefa_topico_diaria.ps1`) pega o **primeiro tópico com status
`pendente`**, pergunta ao Atila se pode gerar e, com o Sim, roda `/criar-topico <id>` no Claude
Code. Reordene as linhas pra mudar a prioridade. Status: `pendente`, `em andamento`, `feito`,
`parcial` (publicado, mas falta algo — ver "falta"), `pulado`.

| ordem | topico_id | curso | módulo / aula | título | status | falta |
|---|---|---|---|---|---|---|
| 1 | 34 | Redes (11) | M1 · NAT, Firewall e DNS | Firewall — bloqueio de entrada vs. saída | feito | |
| 2 | 22 | IA (5) | Aula 2 · Transformers por dentro | Self-Attention: Query, Key, Value | feito | |
| 3 | 70 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Como os 66 livros se formaram (Lc 24:44) ⚠️ cânon 66×73 — nota de neutralidade | feito | |
| 4 | 194 | Inglês (9) | M0 · Quando eu não entendo | "Sorry, I don't understand", "Can you repeat that?", "Can you speak more slowly?" | feito | |
| 5 | 35 | Redes (11) | M1 · NAT, Firewall e DNS | DNS e DDNS | pendente | |
| 6 | 23 | IA (5) | Aula 2 · Transformers por dentro | Causal Masking + Multi-Head Attention | pendente | |
| 7 | 71 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Antigo Testamento: criação, aliança, reino e exílio (Gn 12:1-3) | pendente | |
| 8 | 195 | Inglês (9) | M0 · Quando eu não entendo | "How do you say…?", "What does … mean?", "How do you spell…?" e o alfabeto | feito | |
| 9 | 36 | Redes (11) | M2 · Port Forwarding | Como funciona o redirecionamento de porta | pendente | |
| 10 | 24 | IA (5) | Aula 2 · Transformers por dentro | Dentro do bloco Transformer | pendente | |
| 11 | 72 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Novo Testamento: Cristo, igreja e consumação (Hb 1:1-2) | pendente | |
| 12 | 196 | Inglês (9) | M0 · Quando eu não entendo | Prática: pedir ajuda numa conversa curta | feito | |
| 13 | 37 | Redes (11) | M2 · Port Forwarding | Riscos de expor porta na internet | pendente | |
| 14 | 25 | IA (5) | Aula 2 · Transformers por dentro | Dos logits ao desempenho — KV Cache, Prefill/Decode | pendente | |
| 15 | 73 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Cristo em toda a Escritura (Lc 24:27) | pendente | |
| 16 | 197 | Inglês (9) | M0 · Entendendo o professor | As instruções de todo exercício: read, listen, write, answer, choose, match, repeat | feito | conferência humana: "Match the words and the pictures." é exemplo próprio e match = "ligar/combinar" não foi checado em dicionário (Oxford/Collins/M-W bloqueiam acesso automatizado); níveis CEFR dos 7 verbos não verificados |
| 17 | 170 | Vendas (13, privado) | M1 · O mercado digital | T1 Modelos de negócio online: curso, assinatura, serviço e afiliado | feito | áudio completo (26/26) em 2026-11-02; os outros 23 tópicos do curso 13 ainda estão vazios. O `_diagnostico_topicos.py` acusa "dossiê + auditoria: NÃO EXISTEM" porque procura `topico170-*`, e os arquivos estão em `fontes/vendas/t01-*` |
| 18 | 198 | Inglês (9) | M0 · Entendendo o professor | Confirmar o que entendeu: "You mean…? / Exactly" | feito | conferência humana: "Exactly." = "Exatamente." só tem o vídeo como fonte (dicionários bloqueiam o leitor automático); "You mean…?" sem fonte institucional (só vídeo; "Do you mean…?" tem o British Council) |
| 19 | 199 | Inglês (9) | M0 · Entendendo o professor | Juntando tudo: uma aula inteira em inglês simples | feito | síntese simulada (não é aula real); herda de T197/T198: "Match the words and the pictures." é exemplo próprio; "Exactly." e "You mean …?" com fonte só no vídeo |
| 20 | 200 | Inglês (9) | M1 · He/she/it + -s | He works, she lives: o -s da 3ª pessoa (e a grafia -es, -ies) | pendente | |
| 21 | 201 | Inglês (9) | M1 · He/she/it + -s | Doesn't: a negativa com he/she/it | pendente | |
| 22 | 202 | Inglês (9) | M1 · He/she/it + -s | Prática: he/she/it no dia a dia | pendente | |
| 23 | 203 | Inglês (9) | M1 · He/she/it + -s | Juntando tudo: I, you e he/she/it sem pista | pendente | |
| 24 | 204 | Inglês (9) | M1 · Fazendo perguntas | "Do you…? / Does she…?" e as respostas curtas | pendente | |
| 25 | 205 | Inglês (9) | M1 · Fazendo perguntas | Palavras de pergunta: what, where, who, when, how, how old | pendente | |
| 26 | 206 | Inglês (9) | M1 · Fazendo perguntas | Prática: perguntar e responder | pendente | |
| 27 | 207 | Inglês (9) | M1 · Fazendo perguntas | Juntando tudo: uma entrevista de apresentação | pendente | |
| 28 | 208 | Inglês (9) | M2 · Números | Números de 0 a 20 | pendente | |
| 29 | 209 | Inglês (9) | M2 · Números | De 20 a 1000: preços, idade e telefone | pendente | |
| 30 | 210 | Inglês (9) | M2 · Números | Prática: ditado de números | pendente | |
| 31 | 211 | Inglês (9) | M2 · Horas | "What time is it?": o'clock, half past, quarter past/to | pendente | |
| 32 | 212 | Inglês (9) | M2 · Horas | a.m./p.m. e morning, afternoon, evening, night | pendente | |
| 33 | 213 | Inglês (9) | M2 · Horas | Prática: horários do dia | pendente | |
| 34 | 214 | Inglês (9) | M2 · Dias, semanas, meses e datas | Dias da semana e meses do ano | pendente | |
| 35 | 215 | Inglês (9) | M2 · Dias, semanas, meses e datas | Números ordinais e datas (first… thirty-first) | pendente | |
| 36 | 216 | Inglês (9) | M2 · Dias, semanas, meses e datas | Preposições de tempo: at, in, on | pendente | |
| 37 | 304 | Eng. IA (16, privado) | F1 · Git por dentro | O que o Git guarda: repositório, commit e a pasta .git | feito | publicado em 2026-11-15 (15 slides, 5 imagens, 30 áudios) |
| 38 | 305 | Eng. IA (16, privado) | F1 · Git por dentro | As três áreas: pasta de trabalho, preparação e histórico | feito | publicado em 2026-11-16 (15 slides, 5 imagens, 26 áudios) |
| 39 | 306 | Eng. IA (16, privado) | F1 · Git por dentro | Prática: o repositório de treino e o histórico do NIA | pendente |  |
| 40 | 307 | Eng. IA (16, privado) | F2 · Branch, merge e worktree | Branch é uma etiqueta: switch, fast-forward e merge commit | pendente |  |
| 41 | 308 | Eng. IA (16, privado) | F2 · Branch, merge e worktree | Conflito: por que acontece e como resolver | pendente |  |
| 42 | 309 | Eng. IA (16, privado) | F2 · Branch, merge e worktree | Worktree: duas pastas, um repositório | pendente |  |
| 43 | 310 | Eng. IA (16, privado) | F3 · Remoto e GitHub | Remoto: origin, clone, fetch, pull e push | pendente |  |
| 44 | 311 | Eng. IA (16, privado) | F3 · Remoto e GitHub | Dois remotes e fork: o caso do PinkBella e da Vercel | pendente |  |
| 45 | 312 | Eng. IA (16, privado) | F3 · Remoto e GitHub | Prática: o que está só no seu computador | pendente |  |
| 46 | 313 | Eng. IA (16, privado) | F4 · Pull Request e revisão | Pull Request: o pedido para juntar uma branch | pendente |  |
| 47 | 314 | Eng. IA (16, privado) | F4 · Pull Request e revisão | Revisão: comentário, aprovação, squash e merge | pendente |  |
| 48 | 315 | Eng. IA (16, privado) | F4 · Pull Request e revisão | Prática: lendo o PR #265 do CMPort com gh | pendente |  |
| 49 | 316 | Eng. IA (16, privado) | F5 · Como ler um diff | Anatomia de um diff: hunk, + e - e contexto | pendente |  |
| 50 | 317 | Eng. IA (16, privado) | F5 · Como ler um diff | A lista de revisão: transação, corrida, segredo e efeito colateral | pendente |  |
| 51 | 318 | Eng. IA (16, privado) | F5 · Como ler um diff | Prática: revisar um diff real feito pela IA | pendente |  |
| 52 | 319 | Eng. IA (16, privado) | F6 · Testes | Por que testar: unitário, integração e a pirâmide | pendente |  |
| 53 | 320 | Eng. IA (16, privado) | F6 · Testes | pytest e vitest: ler e rodar uma suíte | pendente |  |
| 54 | 321 | Eng. IA (16, privado) | F6 · Testes | TDD do bug: o teste que falha primeiro | pendente |  |
| 55 | 322 | Eng. IA (16, privado) | F7 · CI/CD | Integração contínua: o que roda a cada PR | pendente |  |
| 56 | 323 | Eng. IA (16, privado) | F7 · CI/CD | Entrega contínua: homologação, produção e runner próprio | pendente |  |
| 57 | 324 | Eng. IA (16, privado) | F7 · CI/CD | Quando o CI quebra: ler o log e decidir | pendente |  |
| 58 | 325 | Eng. IA (16, privado) | F8 · Configuração, terminal e ágil | Arquivos de configuração: JSON, YAML, .env e os três níveis de settings | pendente |  |
| 59 | 326 | Eng. IA (16, privado) | F8 · Configuração, terminal e ágil | Terminal no Windows: PowerShell × Git Bash, PATH e venv | pendente |  |
| 60 | 327 | Eng. IA (16, privado) | F8 · Configuração, terminal e ágil | Ágil na prática: kanban, WIP e definição de pronto | pendente |  |

## Já feitos (processo novo)
| topico_id | curso | título | data |
|---|---|---|---|
| 31 | Redes | Portas TCP/UDP (554, 1935, 80, 443) | 2026-10-01 |
| 66 | Obreiro I | Inspiração: a Escritura soprada por Deus · **prova 38 no padrão novo (18/6, 60%) em 2026-10-07** | 2026-10-01 |
| 32 | Redes | TCP vs UDP aplicado a vídeo (1º via /criar-topico) | 2026-10-03 |
| 67 | Obreiro I | Confiabilidade da Palavra (Sl 19:7-11) | 2026-10-05 |
| 21 | IA | Positional Encoding | 2026-10-05 |
| 68 | Obreiro I | Suficiência das Escrituras (2Pe 1:19-21) | 2026-10-05 |
| 33 | Redes | NAT (Network Address Translation) — áudio terminado depois · **prova 37 no padrão novo (18/6, 70%) em 2026-10-07** | 2026-10-05 |
| 69 | Obreiro I | A Palavra acima da tradição (Mc 7:6-13) — fecha a Aula 60 | 2026-10-06 |
| 34 | Redes | Firewall — bloqueio de entrada vs. saída (16 slides, 8 imagens, 32 áudios) | 2026-10-11 |
| 22 | IA | Self-Attention: Query, Key, Value (17 slides, 8 imagens, 35 áudios) | 2026-10-12 |
| 70 | Obreiro I | Como os 66 livros se formaram (Lc 24:44) — abre a Aula 58 (17 slides, 8 imagens, 36 áudios); leitura do teólogo/pastor recomendada | 2026-10-13 |
| 194 | Inglês | "Sorry, I don't understand", "Can you repeat that?", "Can you speak more slowly?" — 1º tópico do curso (M0); título ajustado: nenhuma fonte ensina "More slowly, please" solto (16 slides, 7 imagens, 15 áudios) | 2026-10-14 |
| 195 | Inglês | "How do you say…?", "What does … mean?", "How do you spell…?" e o alfabeto — 2º tópico do M0 (17 slides, 7 imagens, 15 perguntas, 16 áudios); conferir de ouvido os 🔊 dos cards de letra ("Letter X") no navegador | 2026-10-28 |
| 196 | Inglês | Prática: pedir ajuda numa conversa curta — fecha a Aula 1 do M0 (16 slides, 7 imagens, 14 perguntas, 12 áudios; sem palavra nova, só diálogos com a lista fechada T194+T195) | 2026-10-31 |
| 197 | Inglês | As instruções de todo exercício: read, listen, write, answer, choose, match, repeat — abre a Aula 2 do M0 (16 slides, 7 imagens, 14 perguntas, 15 áudios); fontes lidas: ELTeach, Cambridge Young Learners (Starters/Movers), British Council A1; "match" sem instrução literal nas fontes → ver coluna "falta" | 2026-10-31 |
| 198 | Inglês | Confirmar o que entendeu: "You mean…?" / "Exactly" — 2º tópico da Aula 2 do M0 (16 slides, 7 imagens, 13 perguntas, 14 áudios); fontes lidas: British Council *Checking understanding* (A1) e vídeo Teacher Abelhinha (T7 guardado) | 2026-11-02 |
| 170 | Vendas | Modelos de negócio online — áudio concluído (26/26 blocos; 2026-11-02) | 2026-11-02 |
| 199 | Inglês | Juntando tudo: uma aula inteira em inglês simples — fecha a Aula 2 e o M0 inteiro (16 slides, 7 imagens, 13 perguntas, 14 áudios); aula simulada em 4 cenas só com a lista fechada T194–T198; frase do módulo "Eu consigo pedir ajuda em inglês quando não entendo." | 2026-11-03 |
| 171 | Vendas | Assinatura × venda única: recorrência, churn e LTV — T2 do curso 13, fecha a Aula 1 do M1 (16 slides, 9 imagens sketchnote, 13 perguntas, 35 áudios); fontes lidas: Sebrae PE (e-book de retenção), Sebrae/PR, Conta Azul, Omie, Serasa, Salesforce, Mercado Pago Developers, FTC × Amazon, CDC/Decreto 7.962; números do exercício SIMULADOS; nenhum número de taxa/renda; Emaús só no que é verdade hoje (pagamento não construído, preço não decidido) | 2026-11-03 |
| 172 | Vendas | Funil de venda: da atenção à permanência — T3 do curso 13, abre a Aula 2 do M1 (14 slides, 8 imagens sketchnote, 12 perguntas, 27 áudios); fontes lidas: Sebrae ×4 (PDF E-commerce, Sebrae SC, Comunidade Sebrae PR ×2, e-book Sebrae PE), Baymard, LGPD arts. 5º/6º/8º; números de conversão do exercício SIMULADOS; Emaús só no que é verdade hoje (página de visitante + "Criar conta grátis" existem; assinatura é só plano). McKinsey não lida → fora; tipos de fonte 5 de 8 | 2026-11-03 |
| 173 | Vendas | Público e persona: quem assina o Emaús — T4 do curso 13, fecha a Aula 2 e o Módulo 1 (13 slides, 7 imagens sketchnote, 12 perguntas, 23 áudios); fontes lidas: Sebrae PE (guia de persona), Sebrae MG, Meta ×3 (anúncio 2021, blog de desenvolvedores, política de atributos pessoais 2024), LGPD arts. 5º II e 11; persona do Emaús = HIPÓTESE (sem dados de assinantes); convicção religiosa = dado sensível e a Meta proíbe afirmar/sugerir atributos → nada de segmentar por religião. A conferir por humano: lista de alunos × LGPD art. 11 §1º (advogado); regras de públicos personalizados da Meta (Módulo 4) | 2026-11-03 |
| 200 | 217 | Obreiro ACP (15) | M1 · A Bíblia: o que é e como está organizada | O que é a Bíblia e quem a escreveu | feito | revisão do pastor/Adriano depois: posição da ACP sobre a Bíblia (Declaração de Fé pendente); número "cerca de 40 autores" fora por falta de fonte lida · revisado em 2026-11-10 (NIA-T-021) |
| 201 | 218 | Obreiro ACP (15) | M1 · A Bíblia: o que é e como está organizada | Antigo e Novo Testamento: os 66 livros em um mapa | feito | revisão do pastor/Adriano depois: nomes dos grupos (Lei, História, Poesia e sabedoria, Profetas maiores/menores, Evangelhos, Cartas de Paulo, Outras cartas) e a frase sobre a Bíblia católica · **revisado 2026-11-10 (NIA-T-019)**: 4 erros corrigidos e republicado; decidir se At 17:11 fica aqui ou só na Aula 1.2 |
| 202 | 219 | Obreiro ACP (15) | M1 · A Bíblia: o que é e como está organizada | Como achar qualquer versículo (livro, capítulo, versículo) | feito | revisão do pastor/Adriano depois: tabela de abreviaturas adotada (Bibliaon; outras Bíblias usam outras) · revisado em 2026-11-10 (NIA-T-021) |
| 203 | 220 | Obreiro ACP (15) | M1 · Como ler e entender a Palavra | Ler o texto no seu contexto | feito | revisão do pastor/Adriano depois: ênfase em Jr 29:11 (promessa aos exilados que mostra o coração de Deus) |
| 204 | 221 | Obreiro ACP (15) | M1 · Como ler e entender a Palavra | Observar, entender, aplicar | feito | |
| 205 | 222 | Obreiro ACP (15) | M1 · Como ler e entender a Palavra | Erros comuns de quem está começando | pendente | |
| 206 | 223 | Obreiro ACP (15) | M1 · O que a ACP crê: o essencial da fé | Um só Deus: Pai, Filho e Espírito Santo | pendente | |
| 207 | 224 | Obreiro ACP (15) | M1 · O que a ACP crê: o essencial da fé | Jesus: cruz e ressurreição | pendente | |
| 208 | 225 | Obreiro ACP (15) | M1 · O que a ACP crê: o essencial da fé | Salvação pela graça, arrependimento e novo nascimento | pendente | |
| 209 | 226 | Obreiro ACP (15) | M1 · O que a ACP crê: o essencial da fé | Batismo nas águas | pendente | |
| 210 | 227 | Obreiro ACP (15) | M1 · O que a ACP crê: o essencial da fé | Batismo no Espírito Santo: imersão, línguas e poder para servir | pendente | |
| 211 | 228 | Obreiro ACP (15) | M2 · A origem do serviço | A necessidade que gerou o diaconato | pendente | |
| 212 | 229 | Obreiro ACP (15) | M2 · A origem do serviço | Ministério da Palavra e ministério do serviço | pendente | |
| 213 | 230 | Obreiro ACP (15) | M2 · A origem do serviço | O diácono como apoio e escudo do pastor | pendente | |
| 214 | 231 | Obreiro ACP (15) | M2 · A origem do serviço | Servir com alegria e sem aparecer | pendente | |
| 215 | 232 | Obreiro ACP (15) | M2 · O perfil do diácono | Caráter: sério, sem duplicidade, sem ganância | pendente | |
| 216 | 233 | Obreiro ACP (15) | M2 · O perfil do diácono | Vida espiritual: mistério da fé com consciência limpa | pendente | |
| 217 | 234 | Obreiro ACP (15) | M2 · O perfil do diácono | Casa em ordem | pendente | |
| 218 | 235 | Obreiro ACP (15) | M2 · O perfil do diácono | O que a ACP exige para entrar no ministério | pendente | |
| 219 | 236 | Obreiro ACP (15) | M2 · Chamado e sacerdócio de todos | Todo crente é sacerdote | pendente | |
| 220 | 237 | Obreiro ACP (15) | M2 · Chamado e sacerdócio de todos | Chamado, dons e função no corpo | pendente | |
| 221 | 238 | Obreiro ACP (15) | M2 · Chamado e sacerdócio de todos | Do altar vem a direção: o lugar do pastor e o lugar do obreiro | pendente | |
| 222 | 239 | Obreiro ACP (15) | M3 · Conhecendo a ACP | Para que a igreja existe | pendente | |
| 223 | 240 | Obreiro ACP (15) | M3 · Conhecendo a ACP | O ministério: Pastor, Evangelista, Missionário, Presbítero e Diácono | pendente | |
| 224 | 241 | Obreiro ACP (15) | M3 · Conhecendo a ACP | A assembleia, a diretoria e os membros | pendente | |
| 225 | 242 | Obreiro ACP (15) | M3 · Conhecendo a ACP | Deveres e direitos do membro | pendente | |
| 226 | 243 | Obreiro ACP (15) | M3 · Autoridade, submissão e correção | Autoridade que vem de Deus | pendente | |
| 227 | 244 | Obreiro ACP (15) | M3 · Autoridade, submissão e correção | Submeter-se sem bajular | pendente | |
| 228 | 245 | Obreiro ACP (15) | M3 · Autoridade, submissão e correção | Ouvir repreensão | pendente | |
| 229 | 246 | Obreiro ACP (15) | M3 · Autoridade, submissão e correção | Murmuração e divisão | pendente | |
| 230 | 247 | Obreiro ACP (15) | M3 · Disciplina e perda de cargo | A disciplina na Bíblia | pendente | |
| 231 | 248 | Obreiro ACP (15) | M3 · Disciplina e perda de cargo | As penas da ACP e o direito de defesa | pendente | |
| 232 | 249 | Obreiro ACP (15) | M3 · Disciplina e perda de cargo | Quando eu sou tirado de um cargo: como reagir | pendente | |
| 233 | 250 | Obreiro ACP (15) | M3 · Atas, reuniões e sigilo | O que é uma ata e por que registrar | pendente | |
| 234 | 251 | Obreiro ACP (15) | M3 · Atas, reuniões e sigilo | Participar das reuniões e da assembleia | pendente | |
| 235 | 252 | Obreiro ACP (15) | M3 · Atas, reuniões e sigilo | Sigilo sobre a igreja e sobre os irmãos | pendente | |
| 236 | 253 | Obreiro ACP (15) | M4 · Compromisso com o culto: as ausências | Por que congregar | pendente | |
| 237 | 254 | Obreiro ACP (15) | M4 · Compromisso com o culto: as ausências | Faltas do membro e do obreiro | pendente | |
| 238 | 255 | Obreiro ACP (15) | M4 · Compromisso com o culto: as ausências | Escalado e não veio, ou veio e "sentou": avisar e substituir | pendente | |
| 239 | 256 | Obreiro ACP (15) | M4 · Compromisso com o culto: as ausências | Cuidar de quem faltou | pendente | |
| 240 | 257 | Obreiro ACP (15) | M4 · Recepção: do estacionamento ao banco | Acolher como Cristo acolheu | pendente | |
| 241 | 258 | Obreiro ACP (15) | M4 · Recepção: do estacionamento ao banco | Estacionamento: ajudar, cumprimentar, "seja bem-vindo, fique à vontade" | pendente | |
| 242 | 259 | Obreiro ACP (15) | M4 · Recepção: do estacionamento ao banco | Não deixar visita perdida no meio da igreja | pendente | |
| 243 | 260 | Obreiro ACP (15) | M4 · Recepção: do estacionamento ao banco | Apresentação dos visitantes: o aperto de mão | pendente | |
| 244 | 261 | Obreiro ACP (15) | M4 · Atenção, vigilância e segurança | Vigiar o rebanho | pendente | |
| 245 | 262 | Obreiro ACP (15) | M4 · Atenção, vigilância e segurança | Nunca sozinho com quem não conhece: chamar outro obreiro | pendente | |
| 246 | 263 | Obreiro ACP (15) | M4 · Atenção, vigilância e segurança | Perguntar a quem está no estacionamento se está bem | pendente | |
| 247 | 264 | Obreiro ACP (15) | M4 · Atenção, vigilância e segurança | Cuidado com crianças, adolescentes e o patrimônio da igreja | pendente | |
| 248 | 265 | Obreiro ACP (15) | M4 · A direção do culto | Decência e ordem: o dirigente e o pastor no altar | pendente | |
| 249 | 266 | Obreiro ACP (15) | M4 · A direção do culto | Tempo de oportunidade: 5 minutos | pendente | |
| 250 | 267 | Obreiro ACP (15) | M4 · A direção do culto | Objetivo da oração: enfermo, Palavra e dízimo | pendente | |
| 251 | 268 | Obreiro ACP (15) | M4 · A direção do culto | Santa Ceia: preparo e reverência | pendente | |
| 252 | 269 | Obreiro ACP (15) | M4 · Dízimos e ofertas no culto | O que a Bíblia ensina sobre dízimo e oferta | pendente | |
| 253 | 270 | Obreiro ACP (15) | M4 · Dízimos e ofertas no culto | Recolher com honestidade, conferir em dupla | pendente | |
| 254 | 271 | Obreiro ACP (15) | M4 · Dízimos e ofertas no culto | Para onde vai o dinheiro: a contabilidade da igreja | pendente | |
| 255 | 272 | Obreiro ACP (15) | M5 · Orar por pessoas com autoridade | Por que orar pelos outros | pendente | |
| 256 | 273 | Obreiro ACP (15) | M5 · Orar por pessoas com autoridade | A autoridade que Jesus deu | pendente | |
| 257 | 274 | Obreiro ACP (15) | M5 · Orar por pessoas com autoridade | Repreender o maligno e expulsar demônios: como se faz na Bíblia | pendente | |
| 258 | 275 | Obreiro ACP (15) | M5 · Orar por pessoas com autoridade | Limites: direção do pastor e encaminhar a médico e profissional | pendente | |
| 259 | 276 | Obreiro ACP (15) | M5 · Vida de oração e jejum do obreiro | Orar como Jesus ensinou | pendente | |
| 260 | 277 | Obreiro ACP (15) | M5 · Vida de oração e jejum do obreiro | Tempo a sós com Deus | pendente | |
| 261 | 278 | Obreiro ACP (15) | M5 · Vida de oração e jejum do obreiro | Jejum: o que é e como fazer | pendente | |
| 262 | 279 | Obreiro ACP (15) | M5 · Vida de oração e jejum do obreiro | Fazer a obra de Deus sem perder o Deus da obra | pendente | |
| 263 | 280 | Obreiro ACP (15) | M5 · Visitação e cuidado com os necessitados | Visitar enfermos, idosos e hospitais | pendente | |
| 264 | 281 | Obreiro ACP (15) | M5 · Visitação e cuidado com os necessitados | Cestas básicas e amparo a viúvas e órfãos | pendente | |
| 265 | 282 | Obreiro ACP (15) | M5 · Visitação e cuidado com os necessitados | Visitar com discrição e oração | pendente | |
| 266 | 283 | Obreiro ACP (15) | M5 · Visitação e cuidado com os necessitados | Quando encaminhar: os limites do obreiro | pendente | |
| 267 | 284 | Obreiro ACP (15) | M6 · Casamento | O marido: amar e cuidar da esposa | pendente | |
| 268 | 285 | Obreiro ACP (15) | M6 · Casamento | A esposa: respeitar e ajudar o marido | pendente | |
| 269 | 286 | Obreiro ACP (15) | M6 · Casamento | Quando o casamento está em crise | pendente | |
| 270 | 287 | Obreiro ACP (15) | M6 · Casamento | O solteiro: esperar sem parar a vida, com sabedoria | pendente | |
| 271 | 288 | Obreiro ACP (15) | M6 · Os filhos | Criar os filhos na Palavra | pendente | |
| 272 | 289 | Obreiro ACP (15) | M6 · Os filhos | Disciplina com amor | pendente | |
| 273 | 290 | Obreiro ACP (15) | M6 · Os filhos | O obreiro que serve na igreja e não perde os filhos | pendente | |
| 274 | 291 | Obreiro ACP (15) | M6 · As finanças do obreiro | Quem manda no meu dinheiro | pendente | |
| 275 | 292 | Obreiro ACP (15) | M6 · As finanças do obreiro | Dízimo, oferta e voto: o que cada um é | pendente | |
| 276 | 293 | Obreiro ACP (15) | M6 · As finanças do obreiro | Dívidas e contas em ordem | pendente | |
| 277 | 294 | Obreiro ACP (15) | M6 · As finanças do obreiro | Contentamento e generosidade | pendente | |
| 278 | 295 | Obreiro ACP (15) | M6 · Testemunho fora do templo | Sal e luz | pendente | |
| 279 | 296 | Obreiro ACP (15) | M6 · Testemunho fora do templo | No trabalho e na rua | pendente | |
| 280 | 297 | Obreiro ACP (15) | M6 · Testemunho fora do templo | Na fala e nas redes sociais | pendente | |
| 281 | 298 | Obreiro ACP (15) | M7 · O que as igrejas enfrentam hoje | Cansaço, ativismo e orgulho | pendente | |
| 282 | 299 | Obreiro ACP (15) | M7 · O que as igrejas enfrentam hoje | Grupos de WhatsApp, fofoca e divisão | pendente | |
| 283 | 300 | Obreiro ACP (15) | M7 · O que as igrejas enfrentam hoje | Doutrinas da moda e falsos ensinos | pendente | |
| 284 | 301 | Obreiro ACP (15) | M7 · O que as igrejas enfrentam hoje | Saúde mental, tristeza e quando buscar ajuda | pendente | |
| 285 | 302 | Obreiro ACP (15) | M7 · Perseverar e crescer | Perseverar até o fim | pendente | |
| 286 | 303 | Obreiro ACP (15) | M7 · Perseverar e crescer | Meu plano de serviço e quem me acompanha | pendente | |
