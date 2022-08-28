## Installing
```
pip install discloud
```
## Dev installing
Note: need https://git-scm.com to download
```
pip install git+https://github.com/discloud/python-discloud-status@master
```

## Usage
### Get Started
First of all, you need to get your Discloud API-Token. You can create a new one by typing `.api` in the [Discloud Server](https://discord.gg/discloud).
If you're in trouble on getting your Discloud API-Token, you can DM the Ticket bot (DisCloud ModMail#6424) in the server. The supporters will be glad on helping you

Note: currently this uses the new API version which is available for few users.

### Creating a client
```python
import discloud
client = discloud.Client("API-Token")
```

### Userinfo
```python
user = await discloud_client.user_info()
print(f"ID: '{user.id}'")
plan = user.plan
print(f"Plan '{plan}'")
print(f"Expire date '{plan.expire_date}'")
print(f"Ends in '{plan.expires_in}'")
print(f"Used ram '{user.using_ram}'")
print(f"Total ram '{user.total_ram}'")
print(f"Locale '{user.locale}'"
```

### Application
#### Info
```python
bot = await client.app_info(app_id="APP_ID")
print(f"ID '{bot.id}'")
print(f"Status '{bot.status}'")
print(f"CPU '{bot.cpu}'")
print(f"Memory '{bot.memory}'")
print(f"Memory available '{bot.memory.available}'")
print(f"Using memory '{bot.memory.using}'")
print(f"Mem usada '{bot.memory.using}'")
print(f"SSD '{bot.ssd}'")
print(f"Download '{bot.net_info.download}'")
print(f"Upload '{bot.net_info.upload}'")
print(f"Last restart '{bot.last_restart}'")
```

#### Logs
`Client.app_logs()` returns a Logs. The`.logs` attribute will give you the full logs content, `.small_logs` will give the last 1800 characters
```python
logs = await client.app_logs(app_id="APP_ID")

print(logs.logs) # complete logs
print(logs.small_logs) # around last 1800 characters of your logs
```

#### Start/Restart/Stop
`Client.start_app()`/`Client.restart_app()`/`Client.stop_app()` returns an Action, which contains `.status` attribute so you can know if it was successful and `.message` attr 
so you can know what happened if `.status` is an error
```python
# note: don't expect to get the results there if you use inside of your bot since its going to get shutdown
start_result = await client.start_app(app_id="APP_ID")
restart_result = await client.restart_app(app_id="APP_ID")
stop_result = await client.stop_app(app_id="APP_ID")

print(start_result) # See if the start was successful
print(restart_result) # See if the restart was successful
print(stop_result) # See if the stop was successful
```

#### Commit
`Client.commit()` returns an Action. The `.status` is "ok" if no issues and the message will say that it was successful, otherwise the `.message` will give the detailed error
```python
# note: this always restart your bot so you won't get a result if its inside of your bot
file = discloud.File("eggs.zip") # Must be .zip
result = await client.commit(app_id="APP_ID", file=file)

print(result.message) # See if the commit was successful
```

#### Backup
`Client.backup()` returns a Backup. The `.url` attribute will give you the link
```python
backup = await client.backup(app_id="APP_ID")
print(backup.url) # See if the commit was successful
```

#### Update Ram
`Client.ram()` returns an Action. The `.status` is "ok" if no issues and the message will say that it was successful, otherwise the `.message` will give the detailed error
```python
result = await client.ram(app_id="APP_ID", NEW_RAM)
print(result.message) # See if ram memory was updated
```

#### Upload
WIP


#### Delete
`Client.delete_app()` returns an Action. The `.status` is "ok" if no issues and the message will say that it was successful, otherwise the `.message` will give the detailed error
```python
result = await client.delete_app(app_id="APP_ID")
print(result.message) # See if the app was successfully deleted
```

#### Mods system
WIP

