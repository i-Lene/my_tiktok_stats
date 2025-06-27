import { useEffect, useState } from "react";
import { fetchVideosData } from "../../utils/api_helper";

export default function VideosData() {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function getData() {
      const userData = await fetchVideosData();
      setData(userData);
    }
    getData();
  }, []);

  return (
    <div className="videos_data">
      <h2>TikTok Videos Data</h2>
      <table>
        <thead>
          <tr>
            <th>Video ID</th>
            <th>Title</th>
            <th>View Count</th>
            <th>Like Count</th>
            <th>Share Count</th>
            <th>Collect Count</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {data && data.length > 0 ? (
            data[0].map((video, index) => {
              let dateString = "";
              if (video.createdAt) {
                const date = new Date(Number(video.createdAt) * 1000);
                dateString = date.toLocaleDateString("pt-PT");
              }

              return (
                <tr key={index + 1}>
                  <td>{index + 1}</td>
                  <td>{video.videoName}</td>
                  <td>{video.viewCount}</td>
                  <td>{video.likeCount}</td>
                  <td>{video.shareCount}</td>
                  <td>{video.collectCount}</td>
                  <td>{dateString}</td>
                </tr>
              );
            })
          ) : (
            <tr>
              <td colSpan="8">No videos found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
