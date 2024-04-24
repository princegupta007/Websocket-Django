import React, { useContext } from "react";
import { Link } from "react-router-dom";
import AuthContext from "../context/AuthContext";

const Header = () => {
  const { userId, logoutUser } = useContext(AuthContext);

  const handleLogout = () => {
    logoutUser(); // Call logoutUser function
  };

  return (
    <div>
      <Link to="/">Home</Link>
      <span> | </span>
      <Link to="/dashboard">Dashboard</Link>
      <span> | </span>

      {userId ? (
        <button onClick={handleLogout}>Logout</button>
      ) : (
        <Link to="/login">Login</Link>
      )}
      <br />
      <br />
      {userId ? <p>Welcome, {userId}!</p> : null}
    </div>
  );
};

export default Header;
