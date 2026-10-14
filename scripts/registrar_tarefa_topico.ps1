# Registra a tarefa diária de criação de tópico no Agendador de Tarefas do Windows (2026-10-03).
# Roda só com o Atila logado (a janela de pergunta e o navegador das imagens precisam da sessão dele).
# Uso:  powershell -ExecutionPolicy Bypass -File scripts\registrar_tarefa_topico.ps1 -Hora "09:00"

param([string]$Hora = "09:00")

$Script = Join-Path $PSScriptRoot "tarefa_topico_diaria.ps1"
$Acao = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$Script`"" -WorkingDirectory (Split-Path -Parent $PSScriptRoot)
$Gatilho = New-ScheduledTaskTrigger -Daily -At $Hora
$Config = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 4) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "NIA - Criar topico diario" -Action $Acao -Trigger $Gatilho -Settings $Config -Description "Pergunta se pode gerar o próximo tópico da fila e roda o Claude Code (/criar-topico)." -Force
Write-Output "Tarefa registrada: todo dia às $Hora (se o PC estiver desligado, roda quando ligar)."
