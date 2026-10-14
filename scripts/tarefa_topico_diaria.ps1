# Tarefa diária de criação de tópico (2026-10-03).
#
# 1. Pega o primeiro tópico "pendente" (ou "parcial") de docs/processo-topico/FILA.md
# 2. Pergunta ao Atila numa janela: "Posso gerar o tópico N ...?" (Sim / Não / Cancelar = pular)
# 3. Com o Sim, roda o Claude Code sozinho: claude -p "/criar-topico N"
# 4. Mostra um aviso no fim com o resumo (e guarda o log em logs\tarefa-topico\)
#
# Credenciais da produção: variáveis de ambiente do Windows NIA_EMAIL e NIA_SENHA (nunca em arquivo).
# Agendar: scripts\registrar_tarefa_topico.ps1

$ErrorActionPreference = "Stop"
$Raiz = Split-Path -Parent $PSScriptRoot
Set-Location $Raiz
Add-Type -AssemblyName System.Windows.Forms

$Fila = Join-Path $Raiz "docs\processo-topico\FILA.md"
$Linha = Get-Content $Fila -Encoding UTF8 | Where-Object { $_ -match '^\|\s*\d+\s*\|\s*\d+\s*\|' -and $_ -match '\|\s*(pendente|parcial)\s*\|' } | Select-Object -First 1
if (-not $Linha) {
    [System.Windows.Forms.MessageBox]::Show("A fila de tópicos está vazia. Nada pra gerar hoje.", "NIA - Tarefa diária") | Out-Null
    exit 0
}
$Cols = ($Linha -split '\|') | ForEach-Object { $_.Trim() }
# | ordem | topico_id | curso | módulo / aula | título | status | falta |
$TopicoId = $Cols[2]; $Curso = $Cols[3]; $Aula = $Cols[4]; $Titulo = $Cols[5]; $Status = $Cols[6]

if (-not $env:NIA_EMAIL -or -not $env:NIA_SENHA) {
    [System.Windows.Forms.MessageBox]::Show("Faltam as variáveis NIA_EMAIL e NIA_SENHA no Windows. Sem elas o tópico não pode ser publicado.", "NIA - Tarefa diária") | Out-Null
    exit 1
}

$Texto = "Posso gerar o tópico $TopicoId '$Titulo'?`n`nCurso: $Curso`nMódulo / aula: $Aula`nStatus na fila: $Status`n`nSim = gerar agora   ·   Não = hoje não   ·   Cancelar = pular este tópico"
$Resp = [System.Windows.Forms.MessageBox]::Show($Texto, "NIA - Tarefa diária", "YesNoCancel", "Question")
if ($Resp -eq "No") { exit 0 }
if ($Resp -eq "Cancel") {
    (Get-Content $Fila -Encoding UTF8) | ForEach-Object { if ($_ -eq $Linha) { $_ -replace '\|\s*(pendente|parcial)\s*\|', '| pulado |' } else { $_ } } | Set-Content $Fila -Encoding UTF8
    exit 0
}

$Logs = Join-Path $Raiz "logs\tarefa-topico"
New-Item -ItemType Directory -Force $Logs | Out-Null
$Log = Join-Path $Logs ("topico{0}-{1}.log" -f $TopicoId, (Get-Date -Format "yyyyMMdd-HHmm"))

# Ferramentas liberadas pra execução sozinha (sem perguntar): editar arquivos, rodar scripts,
# buscar fontes na web, ler/gravar o banco do catálogo visual. Nada de push/deploy (regra do comando).
$Permitidas = "Read Edit Write Glob Grep Bash PowerShell WebSearch WebFetch ArtifactData Skill"
& claude -p "/criar-topico $TopicoId" --permission-mode acceptEdits --allowedTools $Permitidas --output-format text 2>&1 |
    Tee-Object -FilePath $Log | Out-Null

$Resumo = (Get-Content $Log -Encoding UTF8 -Tail 25) -join "`n"
[System.Windows.Forms.MessageBox]::Show("Terminou o tópico $TopicoId.`n`n$Resumo`n`nLog completo: $Log", "NIA - Tarefa diária") | Out-Null
