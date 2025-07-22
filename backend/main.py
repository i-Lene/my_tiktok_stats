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
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TikTokDB(Base):
    __tablename__ = "tiktok_user_data"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    videoCount = Column(Integer, nullable=True)
    heartCount = Column(Integer, nullable=True)
    friendCount = Column(Integer, nullable=True)
    followerCount = Column(Integer, nullable=True)
    followingCount = Column(Integer, nullable=True)
    avatar = Column(String, nullable=True)
    description = Column(String, nullable=True)
    createdAt = Column(String, default=lambda: datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"), nullable=True)


class UserVideosDB(Base):
    __tablename__ = "user_videos_data"
    id = Column(Integer, primary_key=True, index=True)
    videoId = Column(String, nullable=True)
    videoName = Column(String, nullable=True)
    viewCount = Column(Integer, nullable=True)
    likeCount = Column(Integer, nullable=True)
    shareCount = Column(Integer, nullable=True)
    collectCount = Column(Integer, nullable=True)
    commentCount = Column(Integer, nullable=True)
    createdAt = Column(String, default=lambda: datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"), nullable=True)


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
    createdAt: str = None


class UserVideos(BaseModel):
    videoId: str = None
    videoName: str = None
    viewCount: int = None
    likeCount: int = None
    shareCount: int = None
    collectCount: int = None
    commentCount: int = None
    createdAt: str = None


app = FastAPI(debug=True)

@app.get("/")
def read_root():
    return {"status": "FastAPI backend is running!", "endpoints": ["/get_tiktok_data", "/add_tiktok_data", "/get_user_videos", "/add_user_videos", "/docs"]}


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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_tiktok = TikTokDB(
        username=entry.username,
        nickname=entry.nickname,
        videoCount=entry.videoCount,
        heartCount=entry.heartCount,
        friendCount=entry.friendCount,
        followerCount=entry.followerCount,
        followingCount=entry.followingCount,
        avatar=entry.avatar,
        description=entry.description,
        createdAt=timestamp
    )
    db.add(db_tiktok)
    db.commit()
    db.refresh(db_tiktok)
    return Entry(
        username=db_tiktok.username,
        nickname=db_tiktok.nickname,
        videoCount=db_tiktok.videoCount,
        heartCount=db_tiktok.heartCount,
        friendCount=db_tiktok.friendCount,
        followerCount=db_tiktok.followerCount,
        followingCount=db_tiktok.followingCount,
        avatar=db_tiktok.avatar,
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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_video = UserVideosDB(
        videoId=user_videos.videoId,
        videoName=user_videos.videoName,
        viewCount=user_videos.viewCount,
        likeCount=user_videos.likeCount,
        shareCount=user_videos.shareCount,
        collectCount=user_videos.collectCount,
        commentCount=user_videos.commentCount,
        createdAt=timestamp
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return UserVideos(
        videoId=db_video.videoId,
        videoName=db_video.videoName,
        viewCount=db_video.viewCount,
        likeCount=db_video.likeCount,
        shareCount=db_video.shareCount,
        collectCount=db_video.collectCount,
        commentCount=db_video.commentCount,
        createdAt=db_video.createdAt
    )


@app.get("/get_user_videos", response_model=List[UserVideos])
def get_user_videos(db: Session = Depends(get_db)):
    data = db.query(UserVideosDB).all()
    return [
        UserVideos(
            videoId=item.videoId,
            videoName=item.videoName,
            viewCount=item.viewCount,
            likeCount=item.likeCount,
            shareCount=item.shareCount,
            collectCount=item.collectCount,
            commentCount=item.commentCount,
            createdAt=item.createdAt
        )
        for item in data
    ]


async def init_data():
    data = await myTikTokSatus()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
            createdAt=timestamp
        )
        db.add(new_user)
        db.commit()
    finally:
        db.close()


async def init_videos():
    data = await myTikTokSatus()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db = SessionLocal()
    try:
        for video in data['videos']:
            video_id = video['id']
            existing_video = db.query(UserVideosDB).filter(
                UserVideosDB.videoId == video_id).first()

            if existing_video:
                existing_video.videoName = video['desc']
                existing_video.viewCount = video['stats']['playCount']
                existing_video.likeCount = video['stats']['diggCount']
                existing_video.shareCount = video['stats']['shareCount']
                existing_video.collectCount = video['stats'].get(
                    'collectCount', 0)
                existing_video.commentCount = video['stats'].get(
                    'commentCount', 0)
                existing_video.createdAt = video.get('createTime', timestamp)
            else:
                new_video = UserVideosDB(
                    videoId=video_id,
                    videoName=video['desc'],
                    viewCount=video['stats']['playCount'],
                    likeCount=video['stats']['diggCount'],
                    shareCount=video['stats']['shareCount'],
                    collectCount=video['stats'].get('collectCount', 0),
                    commentCount=video['stats'].get('commentCount', 0),
                    createdAt=video.get('createTime', timestamp)
                )
                db.add(new_video)
        db.commit()
    finally:
        db.close()


def run_data_collection():
    asyncio.run(init_data())
    asyncio.run(init_videos())


def schedule_daily_collection():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_data_collection, 'cron', hour=00, minute=00)
    scheduler.start()


if __name__ == "__main__":
    schedule_daily_collection()
    asyncio.run(init_data())
    asyncio.run(init_videos())
    uvicorn.run(app, host="0.0.0.0", port=8001)
