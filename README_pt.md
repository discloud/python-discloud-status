## Instalacao
```
pip install discloud
```
## Uso
### Iniciar o client
```python
import discloud
discloud_client = discloud.Client("Token", language="pt")
```

### Buscar informações do usuário
```python
user = discloud_client.fetch_user_info()
print(f"ID: '{user.id}'")
plan = user.plan
print(f"Plano '{plan}'")
print(f"Data de término '{plan.expire_date}'")
print(f"Termina em '{plan.expires_in}'")
```

### Buscar informações do bot
```python
bot = await discloud_client.fetch_bot(bot_id=469310554108854274)
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
logs = await discloud_client.fetch_logs(bot_id=ID_DO_BOT)
# você pode usar também
logs = await bot.fetch_logs()

print(logs.url) # url do logs completo

print(str(logs))
# ou
print(logs.text)
```

### Restart
```python
result = await discloud_client.restart_bot(bot_id=ID_DO_BOT)
# voce pode usar tambem
result = await bot.restart()
print(result) # voce vai saber se ele foi reiniciado ou não
```

### Commit
```python
file = discloud.File("arquivo.zip") # precisa ser em zip
await discloud_client.commit(bot_id=ID_DO_BOT, file=file, restart=True)
# ou tambem
r = await bot.commit(file=file, restart=False)
print(r) # saber se o commit foi um sucesso 
```