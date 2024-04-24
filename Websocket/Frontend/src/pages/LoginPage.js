// pages/LoginPage.js
import React, { useState, useContext } from "react";
import AuthContext from "../context/AuthContext";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null); // Add state for error handling
  const { loginUser } = useContext(AuthContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await loginUser(username, password);
    } catch (error) {
      setError("Invalid username or password. Please try again."); // Set error message
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        {error && <div className="error">{error}</div>}{" "}
        {/* Display error message */}
        <input type="submit" value="Login" />
      </form>
    </div>
  );
};

export default LoginPage;
