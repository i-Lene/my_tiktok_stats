import { useEffect, useState } from "react";
import { fetchUserData } from "../../utils/api_helper";
import LineChart from "./LineChart";

export default function TikTokStats() {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function getData() {
      const userData = await fetchUserData();
      setData(userData);
    }
    getData();
  }, []);

  if (!data[0]) return <div>Loading...</div>;

  const sortedData = [...data[0]].sort(
    (a, b) => new Date(a.createdAt) - new Date(b.createdAt)
  );

  const xValues = sortedData.map((item) => {
    const date = new Date(item.createdAt);
    return date.toLocaleDateString('pt-PT');
  });

  const yValuesFollowers = sortedData.map((item) => item.followerCount);

  const yValuesLikes = sortedData.map((item) => item.heartCount);

  return (
    <>
      <div>
        <h2>TikTok Follower Count Over Time</h2>
        <LineChart
          labelTitle="Follower Count"
          xtitle={"Date"}
          ytitle={"Followers"}
          labels={xValues}
          dataPoints={yValuesFollowers}
        />
      </div>
      <div>
        <h2>TikTok Likes Count Over Time</h2>
        <LineChart
          labelTitle="Likes Count"
          xtitle={"Date"}
          ytitle={"Likes"}
          labels={xValues}
          dataPoints={yValuesLikes}
        />
      </div>
    </>
  );
}
