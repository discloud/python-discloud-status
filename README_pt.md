## Instalando
```
pip install discloud
```
## Instalando o código para devs
Nota: precisa do https://git-scm.com 
```
pip install git+https://github.com/discloud/python-discloud-status@dev
```
## Uso
### Iniciando
Antes de tudo, você precisa obter seu API-Token da Discloud. Você pode criar um novo digitando `.api` no [Servidor da Discloud](https://discord.gg/discloud).
Se você estiver com problemas para obter seu API-Token, você pode enviar uma DM para o bot de Tickets da Discloud (DisCloud ModMail#6424) no servidor. Os apoiadores estarão felizes em ajudá-lo
```python
import discloud
discloud_client = discloud.Client("Token", language="pt")
```

### Informações do usuário
```python
user = await discloud_client.fetch_user_info()
print(f"ID: '{user.id}'")
plan = user.plan
print(f"Plano '{plan}'")
print(f"Data de término '{plan.expire_date}'")
print(f"Termina em '{plan.expires_in}'")
```

### Informações do bot
```python
bot = await discloud_client.fetch_bot(bot_id=BOT_ID)
print(f"ID '{bot.id}'")
print(f"Status '{bot.status}'")
print(f"CPU '{bot.cpu}'")
print(f"Memória '{bot.memory}'")
print(f"Mem disponível '{bot.memory.available}'")
print(f"Mem usada '{bot.memory.using}'")
print(f"Ultimo reinício '{bot.last_restart}'")
```

### Logs
```python
logs = await discloud_client.fetch_logs(bot_id=BOT_ID)
# ou
logs = await bot.fetch_logs()
print(logs.url) # ".url" para um link com os logs completos
print(logs.text) # ".text" para os últimos 1800 caractéres do seus logs
```

### Restart
Para saber se o restart com bem-sucedido, acesse o atributo `.message` de uma Action. 
```python
result = await discloud_client.restart_bot(bot_id=BOT_ID)
# ou
result = await bot.restart()
print(result.message) # Confirma se o restart foi bem-sucedido
```

### Commit
`*.commit()` aceita o kwarg `restart`. Defina-o como True para reiniciar o bot após o commit, False para não reiniciar após o commit.
```python
file = discloud.File("eggs.zip") # Deve ser um .zip
result = await discloud_client.commit(bot_id=BOT_ID, file=file, restart=True)
# or
result = await bot.commit(file=file, restart=True)
print(result.message) # Confirma se o commit foi bem-sucedido
```
