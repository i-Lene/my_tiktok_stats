import api from "../src/api";

export async function fetchUserData() {
  try {
    const response = await api.get("get_tiktok_data");

    const data = response.data;

    if (!Array.isArray(data) || data.length === 0) {
      return ;
    }

    const sorted = data.sort((a, b) => {
      return new Date(b.createdAt) - new Date(a.createdAt);
    });

    return sorted;
  } catch (error) {
    console.error("Error fetching TikTok user data:", error);
    return ;
  }
}
export async function fetchVideosData() {
  try {
    const response = await api.get("get_user_videos");

    const data = response.data;

    if (!Array.isArray(data) || data.length === 0) {
      return [];
    }

    const sorted = data.sort((a, b) => {
      return new Date(b.createdAt) - new Date(a.createdAt);
    });

    return sorted;
  } catch (error) {
    console.error("Error fetching TikTok user data:", error);
    return [];
  }
}
