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

### Understanding the returns
#### Action
All methods that doesn't get information(e.g. start app/change ram/add mod) returns an `Action`. It has `.status` attribute, which is either "ok" when no issues happened, or "error" when something happened. It also contains `.message` attribute which is always returned when an error ocurrs, and is given on almost all actions.

#### Backup
Backup has a `.url` attribute that gives the application's backup link.
#### Logs
Logs has a `.small` attribute which returns the last ~1800 chars of your app logs, and a `.full` attribute that gives the complete logs
#### User
WIP
#### Application
WIP

### Creating a client
```python
import discloud
client = discloud.Client("API-Token")
```

### Userinfo
```python
user = await client.user_info()
print(f"ID: '{user.id}'")
plan = user.plan
print(f"Plan '{plan}'")
print(f"Expire date '{plan.expire_date}'")
print(f"Ends in '{plan.expires_in}'")
print(f"Used ram '{user.using_ram}'")
print(f"Total ram '{user.total_ram}'")
print(f"Locale '{user.locale}'")
```

### Application

#### Info
```python
bot = await client.app_info(target="APP_ID")
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
print(f"Online since '{bot.online_since}'")
print(f"Started at '{bot.start_date}'")
```

#### Logs
`Client.app_logs()` returns a Logs. The`.logs` attribute will give you the full logs content, `.small_logs` will give the last 1800 characters
```python
logs = await client.logs(target="APP_ID")

print(logs.full) # complete logs
print(logs.small) # around last 1800 characters of your logs
```

#### Start/Restart/Stop
`Client.start()`/`Client.restart()`/`Client.stop()` returns an `Action`.
```python
# note: don't expect to get the results there if you use inside of your bot since its going to get shutdown
start_result = await client.start(target="APP_ID")
restart_result = await client.restart(target="APP_ID")
stop_result = await client.stop(target="APP_ID")

print(start_result) # See if the start was successful
print(restart_result) # See if the restart was successful
print(stop_result) # See if the stop was successful
```

#### Commit
`Client.commit()` returns an `Action`.
```python
# note: this always restart your bot so you won't get a result if its inside of your bot
file = discloud.File("eggs.zip") # Must be .zip
result = await client.commit(app_id="APP_ID", file=file)

print(result.message) # See if the commit was successful
```

#### Backup
`Client.backup()` returns a Backup. The `.url` attribute will give you the link
```python
backup = await client.backup(target="APP_ID")
print(backup.url) # Get backup url
```

#### Update Ram
`Client.ram()` returns an `Action`.
```python
result = await client.ram(app_id="APP_ID", NEW_RAM)
print(result.message) # See if ram memory was updated
```

#### Upload
`Client.upload_app()` returns an `Action`.
Note: the .zip must have a `discloud.config` file, more info at [documentation](https://docs.discloudbot.com/v/en/suport/faq/discloud.config)
```python
result = await client.upload_app(file=discloud.File("my_bot.zip"))
print(result.message) # See if the app was successfully added
```


#### Delete
`Client.delete_app()` returns an `Action`.
```python
result = await client.delete_app(app_id="APP_ID")
print(result.message) # See if the app was successfully deleted
```

### Mods System
First you need to setup a specific client to manage bot mods or manage a bot as mod.
```python
import discloud

client = discloud.Client("API-Token")
mod_client = discloud.ModManager(client, "APP_ID")
```
Second, be aware of what mods can currently do, actually they can have one or more of these permissions:
"start_app", "stop_app", "restart_app", "logs_app", "commit_app", "edit_ram", "backup_app", "status_app"
#### Application Owners
To add a moderator to your app you must first have a `Gold Plan` or above.
##### Adding a moderator
`ModManager.add_mod()`
```python
permissions = ["start_app"]
await mod_client.add_mod(mod_id="MOD_ID", permissions)
```
##### Removing a moderator
`ModManager.remove_mod()`
```python
await mod_client.remove_mod(mod_id="MOD_ID")
```

##### Changing moderator permissions
`ModManager.edit_mod_perms()`
```python
new_permissions = ["start_app", "restart_app"] # note: this remove existing perms if they are not there
await mod_client.edit_mod_perms(mod_id="MOD_ID", new_permissions)
```

##### Getting all moderators
`ModManager.get_mods()`
```python
mods = await mod_client.get_mods()
print(mods) # 
```

#### Application moderators
For each command you can do you will need the respective permission as mentioned above
Commands: `ModManager.start()`, `ModManager.restart()`, `ModManager.stop()`, `ModManager.commit()`, `ModManager.backup()`, `ModManager.logs()`,  `ModManager.ram()`, `ModManager.status()`, 
