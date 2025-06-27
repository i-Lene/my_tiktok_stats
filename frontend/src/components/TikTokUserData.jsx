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

  const userdata = data && data.length > 0 ? data[0][0] : null;

  return (
    <div className="tiktok-user-data">
      <h1>TikTok User Data</h1>
      {data && (
        <div>
          <img
            src={userdata.avatar}
            alt={`${userdata.nickname}'s avatar`}
            className="avatar"
          />
          <p>
            <strong>Username: </strong>
            <span>{userdata.username}</span>
          </p>
          <p>
            <strong>Name: </strong>
            <span>{userdata.nickname}</span>
          </p>
          <p>
            <strong>Bio: </strong>
            <span>{userdata.description}</span>
          </p>
          <p>
            <strong>Followers: </strong>
            <span>{userdata.followerCount}</span>
          </p>
          <p></p>
          <strong>Following: </strong>
          <span>{userdata.followingCount}</span>
          <p>
            <strong>Friends: </strong>
            <span>{userdata.friendCount}</span>
          </p>
          <p>
            <strong>Likes: </strong>
            <span>{userdata.heartCount}</span>
          </p>
          <p>
            <strong>Videos: </strong>
            <span>{userdata.videoCount}</span>
          </p>
        </div>
      )}
    </div>
  );
}
