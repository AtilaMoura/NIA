1. Checagem visual do frontend do aluno — já estava pronta pra ser feita, zero dependência de nada discutido aqui. vamos validar que monta algo robusto que inicialmente somente eu vou gerar curso com o front separado por nicho, se for melhor já criar multi-tenant não tem problema vamos fazer, mas tenho o proposito de validar o curso então a ideia é montar duas frente de validação uma é oque eu estodo que é tecnologia IA, analise de dados, ciencia de dados programação e outros, e outra frent é para os irmãos na igreja sobre a biblia fiel a Biblie vidade Jesus Obreiro como Dever do Diacono Vida de Paulo e muito mais vou liberar para testa e ver a validação.

2. Decisão do bloco D (produto único com nichos vs. plataforma multi-tenant) — precisa vir cedo porque muda como o login/admin devem ser desenhados a seguir. Fazer login "genérico" e descobrir depois que precisa ser multi-tenant é retrabalho; fazer login multi-tenant sem precisar é complexidade desperdiçada.
   Acredito que o melhor é multi-tenant, mas posso fazer o único com nichos também se eu quiser certo.

3. Login real + painel admin mínimo — moldados pela resposta do passo 2.

4. Bloco C (blocos + render em componentes) — só depois disso, porque reabre a página de lição que hoje você trata como fechada.
   vamos nos preparar para o melhor mas aplica o mvp

5. Bloco A (LessonAsset) — pode entrar em qualquer ponto depois de 3, é barato e não compete por atenção.
   acredito que temos que ter o plano robusto, e o mpv de ponta a ponta para implementar tudo que precisamos ate para da prazo para primeiro lançamento.

6. Blocos B e E — backlog, sem data, revisitar quando houver volume real de cursos/usuários que justifique o custo. OK
