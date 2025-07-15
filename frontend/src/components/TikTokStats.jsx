import { useEffect, useState } from "react";
import { fetchUserData } from "../../utils/api_helper";
import LineChart from "./LineChart";
import "./TikTokStats.scss";

export default function TikTokStats() {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function getData() {
      const userData = await fetchUserData();
      setData(userData);
    }
    getData();
  }, []);

  if (!data || data.length === 0) return <div>No Data</div>;


  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

  const filteredData = data.filter((item) => {
    const itemDate = new Date(item.createdAt);
    return itemDate >= thirtyDaysAgo;
  });

  const sortedData = [...filteredData].sort(
    (a, b) => new Date(a.createdAt) - new Date(b.createdAt)
  );

  const xValues = sortedData.map((item) => {
    const date = new Date(item.createdAt);
    return date.toLocaleDateString("pt-PT");
  });

  const yValuesFollowers = sortedData.map((item) => item.followerCount);
  const yValuesLikes = sortedData.map((item) => item.heartCount);

  return (
    <div className="tiktok-stats">
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
    </div>
  );
}
