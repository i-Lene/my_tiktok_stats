import json
from TikTokApi import TikTokApi
import os
from dotenv import load_dotenv


load_dotenv()
ms_token = os.getenv("MS_TOKEN")


async def myTikTokSatus():
    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=3,
            browser='chromium',
            headless=True
        )

        user = api.user("gingerflwrs")
        user_data = await user.info()

        videos = []
        
        print('aqui')

        async for video in user.videos(count=100000):
            videos.append(video.as_dict)

    status_dict = {
        "username": user_data["userInfo"]["user"]["uniqueId"],
        "nickname": user_data["userInfo"]["user"]["nickname"],
        "videoCount": user_data["userInfo"]["stats"]["videoCount"],
        "heartCount": user_data["userInfo"]["stats"]["heartCount"],
        "friendCount": user_data["userInfo"]["stats"]["friendCount"],
        "followerCount": user_data["userInfo"]["stats"]["followerCount"],
        "followingCount": user_data["userInfo"]["stats"]["followingCount"],
        "avatar": user_data["userInfo"]["user"]["avatarLarger"],
        "description": user_data["userInfo"]["user"]["signature"],
        "videos": videos
    }

    return status_dict
