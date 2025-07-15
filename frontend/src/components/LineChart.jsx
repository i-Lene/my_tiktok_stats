import { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

export default function LineChart({
  labels = [],
  dataPoints = [],
  xtitle,
  ytitle,
  labelTitle,
  borderColor = "rgb(235, 86, 143)",
  backgroundColor = "rgba(209, 109, 171, 0.2)",
}) {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!labels.length || !dataPoints.length) return;

    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    chartInstance.current = new Chart(chartRef.current, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: labelTitle,
            backgroundColor: backgroundColor,
            borderColor: borderColor,
            data: dataPoints,
            fill: true,
            tension: 0.3,
            pointRadius: window.innerWidth < 1024 ? 0 : 4,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: true },
          tooltip: { mode: "index", intersect: false },
        },
        scales: {
          x: {
            title: { display: true, text: xtitle },
          },
          y: {
            title: { display: true, text: ytitle },
            beginAtZero: true,
          },
        },
      },
    });

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [
    labels,
    dataPoints,
    xtitle,
    ytitle,
    labelTitle,
    backgroundColor,
    borderColor,
  ]);

  return <canvas ref={chartRef} />;
}
