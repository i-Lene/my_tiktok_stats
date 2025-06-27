import api from "../src/api";

export async function fetchUserData() {
  try {
    const response = await api.get("get_tiktok_data");

    const sorted = response.data.sort((a, b) => {
      return new Date(b.createdAt) - new Date(a.createdAt);
    });

    return sorted? [sorted] : null;
    
  } catch (error) {
    console.error("Error fetching TikTok user data:", error);
  }
}


export async function fetchVideosData() {
  try {
    const response = await api.get("get_user_videos");

    const sorted = response.data.sort((a, b) => {
      return new Date(b.createdAt) - new Date(a.createdAt);
    });

    return sorted? [sorted] : null;
    
  } catch (error) {
    console.error("Error fetching TikTok user data:", error);
  }
}