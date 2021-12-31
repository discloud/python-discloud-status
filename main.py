import discloud

discloud_client = discloud.UserClient("token", language="pt")
from discloud.discloud import Plan
print(Plan("", {"plan": "Gold"}))


async def main():
    # get user info
    disclouduser = await discloud_client.fetch_user_info()

    user_id = disclouduser.id
    plan = disclouduser.plan
    print(str(plan))  # "DiamondLite"

    # plan.expires_in = TimedeltaObject
    # plan.expires_in.day = int(days)
    # plan.expires_timestamp = EndTimeUnixTimestamp/DatetimeObject


    ### get bot info
    bot_info = await discloud_client.fetch_bot(bot_id=123)
    ## handle data
    # bot id
    bot_info.id
    # bot cpu
    bot_info.cpu
    # bot memory
    bot_info.memory
    # bot last restart
    #bot_info.last_restart = TimedeltaObject
    #str(bot_info.last_restart) = "int"+"unit" # e.g. 1 hour
    #bot_info.last_restart.timestamp = TimeUnixTimestamp/DatetimeObject

    ### restart bot
    await discloud_client.restart_bot(bot_id=123)

    await bot_info.restart()






#import datetime
#text = "2021-12-08T17:10:22dsadasdasdasdsad"
#d = datetime.datetime.strptime(text[:19], "%Y-%m-%dT%H:%M:%S")
#d.replace(tzinfo=None).astimezone(datetime.timezone.utc)
#print(d)
