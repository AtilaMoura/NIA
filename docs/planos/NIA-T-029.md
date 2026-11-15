# NIA-T-029 — Bloco `codigo` no renderizador de tópicos

Pedido do Atila em 2026-11-14 (curso privado "Engenharia de Software com IA", NIA-T-028). Status: **PROPOSTA**.
Hoje o Emaús não tem como mostrar comando de terminal: a alternativa seria `box`, sem fonte monoespaçada, sem quebra
fiel e sem botão Copiar.

## Formato do bloco (dentro de `conteudo.blocos`)
```json
{"tipo": "codigo", "linguagem": "powershell", "titulo": "Criar o repositório de treino",
 "texto": "mkdir C:\\Users\\amand\\treino-git\ncd C:\\Users\\amand\\treino-git\ngit init -b main",
 "nota": "Digite um comando por vez e leia a resposta do Git."}
```
- `texto` obrigatório (até 5 000 caracteres), quebras de linha preservadas, nada de HTML (o Jinja já escapa).
- `linguagem` opcional: `powershell | bash | python | json | yaml | diff | texto`; só vira o rótulo do bloco (sem colorir
  sintaxe nesta versão, para não trazer biblioteca nova).
- `titulo` e `nota` opcionais. Sem `narracao`/`audio_url`: o áudio não lê comando.

## O que muda (só acrescenta; nenhum bloco existente muda)
1. `backend/app/renderer/templates/topico.html.j2`
   - macro `render_codigo(bloco)`: cabeçalho com `titulo` e o rótulo da `linguagem`, `<pre><code>` com o texto, botão
     "📋 Copiar" e a `nota` embaixo;
   - `elif bloco.tipo == 'codigo'` no `render_bloco`;
   - CSS com as variáveis do tema (claro e escuro), `overflow-x: auto` dentro da caixa (não estoura no celular),
     `white-space: pre`;
   - JS de copiar: o mesmo padrão do `.prompt-copy-btn`, numa função para `.codigo-copy-btn`; se o navegador negar
     a área de transferência, seleciona o texto e avisa "use Ctrl+C".
2. `backend/app/renderer/validate.py`: bloco `codigo` sem `texto` ou com `linguagem` fora da lista vira problema.
3. `docs/schema/schema-conteudo-topico.md`: linha nova na tabela de blocos.
4. `backend/app/agents/perfis.py`, só no `PERFIL_TECH`: uma linha dizendo que comando e trecho de código vão no bloco
   `codigo` (campos acima). Os outros perfis não mudam.
5. Testes em `backend/tests/test_bloco_codigo.py`: renderiza o bloco (texto escapado, quebras preservadas, botão
   presente), `<script>` dentro do texto sai escapado, validação acusa `texto` vazio e `linguagem` inválida, e um tópico
   sem bloco `codigo` renderiza igual a antes.

## Como testar
Local: `docker compose up`, criar um tópico de teste com um bloco `codigo`, `GET /topicos/{id}/render?theme=<tema>` nos
temas claro e escuro, no celular (largura 375px), e clicar em Copiar.

## Produção
É mudança em `backend/app`: **o deploy é do Atila** (DEPLOY.md). Sem migração de banco (o conteúdo é JSON). Enquanto não
subir, nenhum tópico com bloco `codigo` é publicado.

## Executor
Subagente implementador; eu audito o diff e rodo os testes. Commit só com o OK do Atila.
