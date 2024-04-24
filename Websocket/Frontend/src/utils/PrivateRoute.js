// utils/PrivateRoute.js
import { Navigate, useLocation } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";

function PrivateRoute({ children }) {
  const { isLoggedIn } = useContext(AuthContext);
  const location = useLocation();

  // console.log("Private Route", isLoggedIn);
  return isLoggedIn ? (
    children
  ) : (
    <Navigate to="/login" state={{ from: location }} replace />
  );
}

export default PrivateRoute;
