import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from api_helper import myTikTokSatus
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv

currentDateAndTime = datetime.now()
currentTime = currentDateAndTime.strftime("%Y-%m-%d %H:%M:%S")

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TikTokDB(Base):
    __tablename__ = "tiktok_user_data"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    nickname = Column(String,  nullable=True)
    videoCount = Column(Integer, nullable=True)
    heartCount = Column(Integer, nullable=True)
    friendCount = Column(Integer, nullable=True)
    followerCount = Column(Integer, nullable=True)
    followingCount = Column(Integer, nullable=True)
    avatar = Column(String, nullable=True)
    description = Column(String, nullable=True)
    createdAt = Column(String, default=currentTime, nullable=True)


class UserVideosDB(Base):
    __tablename__ = "user_videos_data"
    id = Column(Integer, primary_key=True, index=True)
    videoName = Column(String, nullable=True)
    viewCount = Column(Integer, nullable=True)
    likeCount = Column(Integer, nullable=True)
    shareCount = Column(Integer, nullable=True)
    collectCount = Column(Integer, nullable=True)
    createdAt = Column(String, default=currentTime, nullable=True)


Base.metadata.create_all(bind=engine)


class Entry(BaseModel):
    username: str = None
    nickname: str = None
    videoCount: int = None
    heartCount: int = None
    friendCount: int = None
    followerCount: int = None
    followingCount: int = None
    avatar: str = None
    description: str = None
    createdAt: str = currentTime


class UserVideos(BaseModel):
    videoName: str = None
    viewCount: int = None
    likeCount: int = None
    shareCount: int = None
    collectCount: int = None
    createdAt: str = currentTime


app = FastAPI(debug=True)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add_tiktok_data", response_model=Entry)
def add_entry(entry: Entry, db: Session = Depends(get_db)):
    db_tiktok = TikTokDB(username=entry.username,
                         nickname=entry.nickname,
                         videoCount=entry.videoCount,
                         heartCount=entry.heartCount,
                         friendCount=entry.friendCount, followerCount=entry.followerCount,
                         followingCount=entry.followingCount,
                         avatar=entry.avatar,
                         description=entry.description,
                         createdAt=currentTime
                         )
    db.add(db_tiktok)
    db.commit()
    db.refresh(db_tiktok)
    return Entry(name=db_tiktok.username,
                 nickname=db_tiktok.nickname,
                 videoCount=db_tiktok.videoCount,
                 heartCount=db_tiktok.heartCount,
                 friendCount=db_tiktok.friendCount,
                 followerCount=db_tiktok.followerCount,
                 followingCount=db_tiktok.followingCount, avatar=db_tiktok.avatar,
                 description=db_tiktok.description,
                 createdAt=db_tiktok.createdAt
                 )


@app.get("/get_tiktok_data", response_model=List[Entry])
def get_tiktok_data(db: Session = Depends(get_db)):
    data = db.query(TikTokDB).all()
    return [
        Entry(
            username=item.username,
            nickname=item.nickname,
            videoCount=item.videoCount,
            heartCount=item.heartCount,
            friendCount=item.friendCount,
            followerCount=item.followerCount,
            followingCount=item.followingCount,
            avatar=item.avatar,
            description=item.description,
            createdAt=item.createdAt
        )
        for item in data
    ]


@app.post("/add_user_videos", response_model=UserVideos)
def add_user_videos(user_videos: UserVideos, db: Session = Depends(get_db)):
    db_video = UserVideosDB(videoName=user_videos.videoName,
                            viewCount=user_videos.viewCount,
                            likeCount=user_videos.likeCount,
                            shareCount=user_videos.shareCount,
                            createdAt=currentTime
                            )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return UserVideos(videoName=db_video.videoName,
                      viewCount=db_video.viewCount,
                      likeCount=db_video.likeCount,
                      shareCount=db_video.shareCount,
                      createdAt=db_video.createdAt
                      )


@app.get("/get_user_videos", response_model=List[UserVideos])
def get_user_videos(db: Session = Depends(get_db)):
    data = db.query(UserVideosDB).all()
    return [
        UserVideos(
            videoName=item.videoName,
            viewCount=item.viewCount,
            likeCount=item.likeCount,
            shareCount=item.shareCount,
            collectCount=item.collectCount,
            createdAt=item.createdAt
        )
        for item in data
    ]


async def init_data():
    data = await myTikTokSatus()

    db = SessionLocal()

    try:
        existing_user = db.query(TikTokDB).filter(
            TikTokDB.username == data['username']).first()

        new_user = TikTokDB(
            username=data['username'],
            nickname=data['nickname'],
            videoCount=data['videoCount'],
            heartCount=data['heartCount'],
            friendCount=data['friendCount'],
            followerCount=data['followerCount'],
            followingCount=data['followingCount'],
            avatar=data['avatar'],
            description=data['description'],
            createdAt=currentTime
        )
        db.add(new_user)
        db.commit()

    finally:
        db.close()


async def init_videos():
    data = await myTikTokSatus()

    db = SessionLocal()

    try:
        for video in data['videos']:
            new_video = UserVideosDB(
                videoName=video['desc'],
                viewCount=video['stats']['playCount'],
                likeCount=video['stats']['diggCount'],
                shareCount=video['stats']['shareCount'],
                collectCount=video['stats']['collectCount'] if 'collectCount' in video['stats'] else 0,
                createdAt=video['createTime'] if 'createTime' in video else currentTime
            )
            db.add(new_video)
        db.commit()

    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(init_data())
    asyncio.run(init_videos())
    uvicorn.run(app, host="0.0.0.0", port=8001)
