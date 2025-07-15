import { useEffect, useState } from "react";
import { fetchUserData } from "../../utils/api_helper";

export default function TikTokUserData() {
  const [data, setData] = useState(null);

  useEffect(() => {
    async function getData() {
      const userData = await fetchUserData();
      setData(userData);
    }
    getData();
  }, []);

  const userdata = data && data.length > 0 ? data[0] : null;

  return (
    <div className="tiktok_user_data">
      <h1>
        TikTok <span>@{userdata?.username} </span>
        User Data
      </h1>
      {data && (
        <div>
          <div className="avatar_container">
            <img
              src={userdata.avatar}
              alt={`${userdata.nickname}'s avatar`}
              className="avatar"
            />
          </div>
          <div className="user_info">
            <p className="nickname">
              <span>{userdata.nickname}</span>
            </p>
            <p className="description">
              <span>{userdata.description}</span>
            </p>
            <div className="stats">
              <p className="followers">
                <strong>Followers: </strong>
                <span>{userdata.followerCount}</span>
              </p>
              <p className="following">
                <strong>Following: </strong>
                <span>{userdata.followingCount}</span>
              </p>
              <p className="friends">
                <strong>Friends: </strong>
                <span>{userdata.friendCount}</span>
              </p>
              <p className="likes">
                <strong>Likes: </strong>
                <span>{userdata.heartCount}</span>
              </p>
              <p className="videos_count">
                <strong>Videos: </strong>
                <span>{userdata.videoCount}</span>
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
