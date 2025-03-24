import axios from "axios";

// Set the URL to your backend
const API_URL = "http://localhost:8000";

interface ChatResponse {
  message: string;
}

export const sendMessage = async (
  message: string,
  threadId: string
): Promise<ChatResponse> => {
  try {
    const response = await axios.post(`${API_URL}/query`, {
      query: message,
      thread_id: threadId,
    });
    return response.data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};
