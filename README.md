## Installing
```
pip install discloud
```
## Dev installing
Note: need https://git-scm.com to download
```
pip install git+https://github.com/discloud/python-discloud-status@dev
```

## Usage
### Create client instance
```python
import discloud
discloud_client = discloud.Client("Token")
```

### Fetch user info
```python
user = discloud_client.fetch_user_info()
print(f"ID: '{user.id}'")
plan = user.plan
print(f"Plan '{plan}'")
print(f"Expire date '{plan.expire_date}'")
print(f"Ends in '{plan.expires_in}'")
```

### Fetch bot info
```python
bot = await discloud_client.fetch_bot(bot_id=469310554108854274)
print(f"ID '{bot.id}'")
print(f"Status '{bot.status}'")
print(f"CPU '{bot.cpu}'")
print(f"Memóry '{bot.memory}'")
print(f"Memory available '{bot.memory.available}'")
print(f"Using memory '{bot.memory.using}'")
print(f"Last restart '{bot.last_restart}'")
```

### Logs
```python
logs = await discloud_client.fetch_logs(bot_id=ID_DO_BOT)
# or
logs = await bot.fetch_logs()

print(logs.url) # url for full logs

print(str(logs))
# or
print(logs.text) # for last 1800 chars
```

### Restart
```python
result = await discloud_client.restart_bot(bot_id=BOT_ID)
# or
result = await bot.restart()
print(result) # you will know if it was restarted
```

### Commit
```python
file = discloud.File("file.zip") # precisa ser em zip
await discloud_client.commit(bot_id=BOT_ID, file=file, restart=True)
# or
r = await bot.commit(file=file, restart=False)
print(r) # know if commit was successful
```