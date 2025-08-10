## Instalando
```
pip install discloud
```
## Instalando o código para devs
Nota: precisa do https://git-scm.com 
```
pip install git+https://github.com/discloud/python-discloud-status@dev
```
## Como usar
### Iniciando
Antes de tudo, você precisa obter seu API-Token da Discloud. Você pode criar um novo digitando `.api` no [Servidor da Discloud](https://discord.discloudbot.com).
Se você estiver com problemas para obter seu API-Token, você pode enviar uma DM para o bot de Tickets da Discloud (DisCloud ModMail#6424) no servidor. Os apoiadores estarão felizes em ajudá-lo

### Entendendo os retornos
#### Action
Todos os métodos que não obtêm informações (por exemplo, iniciar aplicativo/mudar RAM/adicionar mod) retornam uma Ação. Ela possui o atributo `.status`, que é "ok" quando não há problemas, ou "error" quando algo acontece. Também contém o atributo `.message`, que é sempre retornado quando ocorre um erro e é fornecido em quase todas as actions.
#### Backup
O Backup possui um atributo `.url` que fornece o link de backup do aplicativo.
#### Logs
Logs possui um atributo `.small` que retorna os últimos ~1800 caracteres dos logs do seu aplicativo, e um atributo `.full` que fornece os logs completos.
#### User
WIP
#### Application
WIP

### Criando um client
```python
import discloud
client = discloud.Client("API-Token")
```

### Informações do usuário
```python
user = await client.user_info()
print(f"ID: '{user.id}'")
plan = user.plan
print(f"Plano '{plan}'")
print(f"Data de expiração '{plan.expire_date}'")
print(f"Expira em '{plan.expires_in}'")
print(f"RAM usada '{user.using_ram}'")
print(f"RAM total '{user.total_ram}'")
print(f"Localidade '{user.locale}'")
```

### Application

#### Informações
```python
bot = await client.app_info(target="APP_ID")
print(f"ID '{bot.id}'")
print(f"Avatar '{bot.avatarURL}'")
print(f"Nome '{bot.name}'")
print(f"Online '{bot.online}'")
print(f"Arquivo principal '{bot.mainFile}'")
print(f"Linguagem '{bot.lang}'")
print(f"Auto deploy '{bot.autoDeployGit}'")
print(f"Auto restart '{bot.autoRestart}'")
```

#### Status
```python
bot = await client.app_status(target="APP_ID")
print(f"ID '{bot.id}'")
print(f"Status '{bot.status}'")
print(f"CPU '{bot.cpu}'")
print(f"Memória '{bot.memory}'")
print(f"Memória disponível '{bot.memory.available}'")
print(f"Memória em uso '{bot.memory.using}'")
print(f"Mem usada '{bot.memory.using}'")
print(f"SSD '{bot.ssd}'")
print(f"Download '{bot.net_info.download}'")
print(f"Upload '{bot.net_info.upload}'")
print(f"Online desde '{bot.online_since}'")
print(f"Iniciado em '{bot.start_date}'")
```

#### Logs
`Client.app_logs()` retorna um objeto Logs. O atributo `.logs` fornecerá o conteúdo completo dos logs, e `.small_logs` fornecerá os últimos ~1800 caracteres.
```python
logs = await client.logs(target="APP_ID")

print(logs.full) # logs completos
print(logs.small) # cerca dos últimos 1800 caracteres dos seus logs
```

#### Iniciar/Reiniciar/Parar
`Client.start()`/`Client.restart()`/`Client.stop()` retorna uma `Action`.
Para saber se o restart com bem-sucedido, acesse o atributo `.message` de uma Action. 
```python
# nota: não espere obter os resultados aqui se você usar dentro do seu bot, pois ele será desligado
start_result = await client.start(target="APP_ID")
restart_result = await client.restart(target="APP_ID")
stop_result = await client.stop(target="APP_ID")

print(start_result) # Veja se o início foi bem-sucedido
print(restart_result) # Veja se a reinicialização foi bem-sucedida
print(stop_result) # Veja se a parada foi bem-sucedida
```

#### Commit
`Client.commit()` retorna uma `Action`
```python
# nota: isso sempre reinicia seu bot, então você não obterá um resultado se estiver dentro do seu bot
file = discloud.File("eggs.zip") # Deve ser .zip
result = await client.commit(app_id="APP_ID", file=file)

print(result.message) # Veja se o commit foi bem-sucedido
```

#### Backup
`Client.backup()` retorna um objeto Backup. O atributo `.url` fornecerá o link.
```python
backup = await client.backup(target="APP_ID")
print(backup.url) # Obter URL do backup
```

#### Atualizar RAM
`Client.ram()` retorna uma `Action`
```python
result = await client.ram(app_id="APP_ID", NEW_RAM)
print(result.message) # Veja se a memória RAM foi atualizada
```

#### Upload
`Client.upload_app()` retorna uma `Action`.
```python
# Nota: o arquivo .zip deve ter um arquivo discloud.config. Mais informações em documentação.
result = await client.upload_app(file=discloud.File("my_bot.zip"))
print(result.message) # Veja se o aplicativo foi adicionado com sucesso
```

#### Excluir
`Client.delete_app()` retorna uma `Action`.
```python
result = await client.delete_app(app_id="APP_ID")
print(result.message) # Veja se o aplicativo foi excluído com sucesso
```

### Sistema de Mods
Primeiro, você precisa configurar um cliente específico para gerenciar mods de bot ou gerenciar um bot como mod.
```python
import discloud

client = discloud.Client("API-Token")
mod_client = discloud.ModManager(client, "APP_ID")
```
Segundo, esteja ciente do que os mods podem fazer atualmente. Na verdade, eles podem ter uma ou mais das seguintes permissões:
"start_app", "stop_app", "restart_app", "logs_app", "commit_app", "edit_ram", "backup_app", "status_app"

#### Assinantes
Para adicionar um moderador ao seu aplicativo, você deve primeiro ter um Plano Gold ou superior.

##### Adicionando um Moderador
`ModManager.add_mod()`
```python
permissions = ["start_app"]
await mod_client.add_mod(mod_id="MOD_ID", permissions)
```
##### Removendo um Moderador
`ModManager.remove_mod()`
```python
await mod_client.remove_mod(mod_id="MOD_ID")
```
##### Alterando Permissões de Moderador
`ModManager.edit_mod_perms()`
```python
new_permissions = ["start_app", "restart_app"] # nota: isso remove as permissões existentes se elas não estiverem aqui
await mod_client.edit_mod_perms(mod_id="MOD_ID", new_permissions)
```
##### Obtendo Todos os Moderadores
`ModManager.get_mods()`
```python
mods = await mod_client.get_mods()
print(mods)
```
##### Moderadores de Aplicativos
Para cada comando que você pode executar, você precisará da respectiva permissão, conforme mencionado acima.
Comandos: `ModManager.start()`, `ModManager.restart()`, `ModManager.stop()`, `ModManager.commit()`, `ModManager.backup()`, `ModManager.logs()`, `ModManager.ram()`, `ModManager.status()`.