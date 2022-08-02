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
### Get Started
First of all, you need to get your Discloud API-Token. You can create a new one by typing `.api` in the [Discloud Server](https://discord.gg/discloud).
If you're in trouble on getting your Discloud API-Token, you can DM the Ticket bot (DisCloud ModMail#6424) in the server. The supporters will be glad on helping you

### Creating a client
```python
import discloud
discloud_client = discloud.Client("API-Token")
```

### User info
```python
user = await discloud_client.fetch_user_info()
print(f"ID: '{user.id}'")
plan = user.plan
print(f"Plan '{plan}'")
print(f"Expire date '{plan.expire_date}'")
print(f"Ends in '{plan.expires_in}'")
```

### Bot info
```python
bot = await discloud_client.fetch_bot(bot_id=BOT_ID)
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
logs = await discloud_client.fetch_logs(bot_id=BOT_ID)
# or
logs = await bot.fetch_logs()

print(logs.url) # ".url" for a link with full logs
print(logs.text) # ".text" for the last 1800 characters of your logs
```

### Restart
`Bot.restart()`/`Client.restart_bot()` returns an Action, wich contains a `.message` attr so you can know if the reset was successful by printing it
```python
result = await discloud_client.restart_bot(bot_id=BOT_ID)
# or
result = await bot.restart()

print(result.message) # See if the restart was successful
```

### Commit
`Bot.commit()`/`Client.commit()` returns an Action. Print the `.message` of it to know if the commit was successful. <br />
`*.commit()` accepts the `restart` kwarg. Set it to True to restart the bot after a commit, False to not.
```python
file = discloud.File("eggs.zip") # Must be .zip
result = await discloud_client.commit(bot_id=BOT_ID, file=file, restart=True)
# or
result = await bot.commit(file=file, restart=True)

print(result.message) # See if the commit was successful
```
