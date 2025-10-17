import axios from "axios";

// ✅ Use backend URL if provided, else use localhost for dev
const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

console.log("🔍 BASE_URL:", BASE_URL);
console.log("🔍 process.env.NEXT_PUBLIC_API_URL:", process.env.NEXT_PUBLIC_API_URL);

export const api = axios.create({
  baseURL: BASE_URL,
});

// API functions
export const createUser = async (email, name) => {
  const res = await api.post("/users", { email, name });
  return res.data;
};

export const getUserByEmail = async (email) => {
  try {
    const res = await api.get("/users");
    const users = res.data;
    return users.find((u) => u.email === email);
  } catch (error) {
    console.error("❌ Error connecting to backend:", error.message);
    throw error;
  }
};

export const addWorkout = async (userId, workout) => {
  const res = await api.post(`/users/${userId}/workouts`, workout);
  return res.data;
};

export const getWorkouts = async (userId) => {
  const res = await api.get(`/users/${userId}/workouts`);
  return res.data;
};
