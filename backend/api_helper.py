import json
from TikTokApi import TikTokApi
import os
from dotenv import load_dotenv


load_dotenv()
ms_token = os.getenv("MS_TOKEN")



async def myTikTokSatus():
    async with TikTokApi(no_browser=True) as api:
        user = await api.user("gingerflwrs").info()

        videos = await api.user("gingerflwrs").videos(count=10000000)

        return {
            "username": user["userInfo"]["user"]["uniqueId"],
            "nickname": user["userInfo"]["user"]["nickname"],
            "videoCount": user["userInfo"]["stats"]["videoCount"],
            "heartCount": user["userInfo"]["stats"]["heartCount"],
            "friendCount": user["userInfo"]["stats"]["friendCount"],
            "followerCount": user["userInfo"]["stats"]["followerCount"],
            "followingCount": user["userInfo"]["stats"]["followingCount"],
            "avatar": user["userInfo"]["user"]["avatarThumb"],
            "description": user["userInfo"]["user"]["signature"],
            "videos": [video.as_dict if hasattr(video, "as_dict") else dict(video) for video in videos]
        }

