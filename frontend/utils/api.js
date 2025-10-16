import axios from "axios";

// Use environment variable for API URL, fallback to localhost for development
const BASE_URL = process.env.NEXT_PUBLIC_API_URL 
  ? `${process.env.NEXT_PUBLIC_API_URL}/api` 
  : "http://localhost:8000/api";

export const createUser = async (email, name) => {
  const res = await axios.post(`${BASE_URL}/users`, { email, name });
  return res.data;
};

export const getUserByEmail = async (email) => {
  try {
    const res = await axios.get(`${BASE_URL}/users`);
    const users = res.data;
    return users.find((u) => u.email === email);
  } catch (error) {
    console.error("Error connecting to backend:", error.message);
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