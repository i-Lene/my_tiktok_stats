import { useEffect, useState } from "react";
import { fetchVideosData } from "../../utils/api_helper";
import * as bootstrap from "bootstrap";
import DataTable from "datatables.net-react";
import DataTablesCore from "datatables.net-bs5";
import "datatables.net-responsive-bs5";
import "datatables.net-select-bs5";
import Responsive from "datatables.net-responsive-bs5";

export default function VideosData() {
  const [data, setData] = useState([]);

  DataTablesCore.use(bootstrap);
  DataTable.use(DataTablesCore);
  DataTable.use(Responsive);

  useEffect(() => {
    async function getData() {
      const userData = await fetchVideosData();
      setData(userData);
    }
    getData();
  }, []);


  const isMobile = window.innerWidth < 1024;

  return (
    <div className="videos_data">
      <h2>TikTok Videos Data</h2>
      <div className="table-container">
        <DataTable
          style={{ width: "100%" }}
          data={data || []}
          className="display"
          options={{
            columns: [
              {
                title: "Title",
                data: "videoName", 
                responsivePriority: 1,
                className: "all",
              },
              {
                title: "View Count",
                data: "viewCount",
                responsivePriority: 100,
                className: isMobile && "none",
              },
              {
                title: "Like Count",
                data: "likeCount",
                responsivePriority: 101,
                className: isMobile && "none",
              },
              {
                title: "Share Count",
                data: "shareCount",
                responsivePriority: 102,
                className: isMobile && "none",
              },
              {
                title: "Collect Count",
                data: "collectCount",
                responsivePriority: 103,
                className: isMobile && "none",
              },
              {
                title: "Comment Count",
                data: "commentCount",
                responsivePriority: 104,
                className: isMobile && "none",
              },
              {
                title: "Created At",
                data: "createdAt",
                responsivePriority: 104,
                className: isMobile && "none",
                render: {
                  display: function (data) {
                    if (!data) return "";
                    const date = new Date(Number(data) * 1000);
                    const pad = (n) => n.toString().padStart(2, "0");
                    const d = pad(date.getDate());
                    const mo = pad(date.getMonth() + 1);
                    const y = date.getFullYear();
                    return `${d}-${mo}-${y}`;
                  },
                  sort: function (data) {
                    return Number(data);
                  },
                },
              },
            ],

            order: [[6, "desc"]],
            select: false,
            paging: true,
            pageLength: 10,
            scrollX: true,
            responsive: true,
            autoWidth: false,
          }}
        ></DataTable>
      </div>
    </div>
  );
}
