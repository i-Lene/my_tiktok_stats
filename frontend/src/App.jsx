import "./App.scss";
import TikTokStats from "./components/TikTokStats";
import TikTokUserData from "./components/TikTokUserData";
import VideosData from "./components/Videosdata";

function App() {
  return (
    <>
      <TikTokUserData />
      <TikTokStats />
      <VideosData />
    </>
  );
}

export default App;
