import { useEffect, useState } from "react";
import { fetchUserData } from "../../utils/api_helper";
import LineChart from "./LineChart";
import "./TikTokStats.scss";

export default function TikTokStats() {
  const [data, setData] = useState([]);
  const [view, setView] = useState("30days");

  useEffect(() => {
    async function getData() {
      const userData = await fetchUserData();
      let flat = userData;
      if (Array.isArray(userData) && Array.isArray(userData[0])) {
        flat = userData[0];
      }
      setData(flat || []);
    }
    getData();
  }, []);

  if (!data || data.length === 0) return <div>No Data</div>;

  let filteredData = [];
  const now = new Date();

  if (view === "30days") {
    const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
    filteredData = data.filter((item) => {
      const itemDate = new Date(item.createdAt);
      return itemDate >= thirtyDaysAgo && itemDate <= now;
    });
  } else if (view === "monthly") {
    const byMonth = {};
    data.forEach((item) => {
      const date = new Date(item.createdAt);
      const key = `${date.getFullYear()}-${(date.getMonth() + 1)
        .toString()
        .padStart(2, "0")}`;
      if (
        !byMonth[key] ||
        new Date(item.createdAt) > new Date(byMonth[key].createdAt)
      ) {
        byMonth[key] = item;
      }
    });
    filteredData = Object.values(byMonth).sort(
      (a, b) => new Date(a.createdAt) - new Date(b.createdAt)
    );
  }

  const sortedData = [...filteredData].sort(
    (a, b) => new Date(a.createdAt) - new Date(b.createdAt)
  );

  const xValues = sortedData.map((item) => {
    const date = new Date(item.createdAt);
    return view === "monthly"
      ? `${date.toLocaleString("default", {
          month: "short",
        })} ${date.getFullYear()}`
      : date.toLocaleDateString("pt-PT");
  });

  const yValuesFollowers = sortedData.map((item) => item.followerCount);
  const yValuesLikes = sortedData.map((item) => item.heartCount);

  return (
    <div className="tiktok_stats">
      <div className="view_selector">
        <label>View: </label>
        <select value={view} onChange={(e) => setView(e.target.value)}>
          <option value="30days">Last 30 Days</option>
          <option value="monthly">Monthly (latest per month)</option>
        </select>
      </div>
      <div className="charts_container">
        <div className="chart">
          <h2>
            Follower Count {view === "monthly" ? "(Monthly)" : "(Last 30 Days)"}
          </h2>
          <LineChart
            labelTitle="Follower Count"
            xtitle={view === "monthly" ? "Month" : "Date"}
            ytitle={"Followers"}
            labels={xValues}
            dataPoints={yValuesFollowers}
            borderColor="#1e9370"
            backgroundColor="rgba(30, 147, 112, 0.2)"
          />
        </div>
        <div className="chart">
          <h2>
            Likes Count {view === "monthly" ? "(Monthly)" : "(Last 30 Days)"}
          </h2>
          <LineChart
            labelTitle="Likes Count"
            xtitle={view === "monthly" ? "Month" : "Date"}
            ytitle={"Likes"}
            labels={xValues}
            dataPoints={yValuesLikes}
            borderColor="#1e9370"
            backgroundColor="rgba(30, 147, 112, 0.2)"
          />
        </div>
      </div>
    </div>
  );
}
