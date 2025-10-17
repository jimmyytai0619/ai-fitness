import axios from "axios";

// HARDCODED for now - we'll fix this after we confirm it works
const BASE_URL = "https://ai-fitness-production-ddab.up.railway.app/api";

console.log("🔍 BASE_URL:", BASE_URL);

export const createUser = async (email, name) => {
  console.log("✅ Creating user at:", `${BASE_URL}/users`);
  const res = await axios.post(`${BASE_URL}/users`, { email, name });
  return res.data;
};

export const getUserByEmail = async (email) => {
  try {
    console.log("✅ Getting users from:", `${BASE_URL}/users`);
    const res = await axios.get(`${BASE_URL}/users`);
    const users = res.data;
    return users.find((u) => u.email === email);
  } catch (error) {
    console.error("❌ Error connecting to backend:", error.message);
    throw error;
  }
};

export const addWorkout = async (userId, workout) => {
  const res = await axios.post(`${BASE_URL}/users/${userId}/workouts`, workout);
  return res.data;
};

export const getWorkouts = async (userId) => {
  const res = await axios.get(`${BASE_URL}/users/${userId}/workouts`);
  return res.data;
};
