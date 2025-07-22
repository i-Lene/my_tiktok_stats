import "./App.scss";
import TikTokUserData from "./components/TikTokUserData";
import VideosData from "./components/Videosdata";

function App() {

  console.log("App component loaded");
  
  return (
    <>
      <TikTokUserData />
      <VideosData />
    </>
  );
}

export default App;
