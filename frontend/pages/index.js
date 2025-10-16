import { useState } from "react";
import { createUser, getUserByEmail, addWorkout, getWorkouts } from "../utils/api";

export default function Home() {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [user, setUser] = useState(null);
  const [workouts, setWorkouts] = useState([]);

  // Workout form
  const [type, setType] = useState("strength");
  const [duration, setDuration] = useState(30);
  const [calories, setCalories] = useState(200);

  const handleSignup = async () => {
    const newUser = await createUser(email, name);
    setUser(newUser);
    alert(`Welcome, ${newUser.name}!`);
  };

  const handleLogin = async () => {
    const found = await getUserByEmail(email);
    if (!found) {
      alert("User not found. Please sign up first.");
      return;
    }
    setUser(found);
    const list = await getWorkouts(found.id);
    setWorkouts(list);
  };

  const handleAddWorkout = async () => {
    if (!user) return alert("Please log in first");
    const workout = {
      date: new Date().toISOString().slice(0, 10),
      type,
      duration_min: Number(duration),
      calories_burned: Number(calories),
    };
    await addWorkout(user.id, workout);
    const list = await getWorkouts(user.id);
    setWorkouts(list);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>🏋️‍♂️ AI Fitness Coach</h1>

      {!user ? (
        <>
          <h2>Login / Signup</h2>
          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ marginRight: "0.5rem" }}
          />
          <input
            placeholder="Name (for signup)"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <div style={{ marginTop: "1rem" }}>
            <button onClick={handleLogin}>Log In</button>
            <button onClick={handleSignup} style={{ marginLeft: "0.5rem" }}>Sign Up</button>
          </div>
        </>
      ) : (
        <>
          <h2>Welcome, {user.name}!</h2>

          <div style={{ marginTop: "2rem" }}>
            <h3>Add Workout</h3>
            <div>
              <label>Type: </label>
              <select value={type} onChange={(e) => setType(e.target.value)}>
                <option value="strength">Strength</option>
                <option value="cardio">Cardio</option>
                <option value="yoga">Yoga</option>
                <option value="stretching">Stretching</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div>
              <label>Duration (min): </label>
              <input
                type="number"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
              />
            </div>

            <div>
              <label>Calories burned: </label>
              <input
                type="number"
                value={calories}
                onChange={(e) => setCalories(e.target.value)}
              />
            </div>

            <button style={{ marginTop: "1rem" }} onClick={handleAddWorkout}>
              Add Workout
            </button>
          </div>

          <div style={{ marginTop: "2rem" }}>
            <h3>Your Workouts</h3>
            <ul>
              {workouts.map((w) => (
                <li key={w.id}>
                  {w.date} - {w.type} - {w.duration_min} min - {w.calories_burned} cal
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}
