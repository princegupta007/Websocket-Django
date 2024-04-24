import React, { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import {
  getItemFromLocalStorage,
  setItemToLocalStorage,
  removeItemFromLocalStorage,
} from "../utils/localStorage";
import { useCallback } from "react";

const AuthContext = createContext();
export default AuthContext;

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState({
    access: getItemFromLocalStorage("accessToken") || null,
    refresh: getItemFromLocalStorage("refreshToken") || null,
  });
  const [user, setUser] = useState(
    getItemFromLocalStorage("user")
      ? JSON.parse(getItemFromLocalStorage("user"))
      : null,
  );
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // console.log("User initialized:", user); // Debug log for initial user state
  }, [user]);

  const loginUser = async (username, password) => {
    try {
      const response = await fetch("http://192.168.0.224:8000/account/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      // console.log(data,"login time..........");

      if (response.ok) {
        setAuthTokens({
          access: data.access,
          refresh: data.refresh,
        });
        setUser({
          user_id: data.user_id,
          user_type: data.user_type,
        });
        setItemToLocalStorage("accessToken", data.access);
        setItemToLocalStorage("refreshToken", data.refresh);
        setItemToLocalStorage(
          "user",
          JSON.stringify({
            user_id: data.user_id,
            user_type: data.user_type,
          }),
        );
        setLoading(false);
        navigate("/");
      } else {
        console.error("Error occurred during login:", data.error);
      }
    } catch (error) {
      console.error("Error occurred during login:", error);
    }
  };

  const logoutUser = useCallback(() => {
    removeItemFromLocalStorage("accessToken");
    removeItemFromLocalStorage("refreshToken");
    removeItemFromLocalStorage("user");
    setAuthTokens({
      access: null,
      refresh: null,
    });
    setUser(null);
    navigate("/login", { replace: true });
  }, [navigate]);

  const updateToken = useCallback(async () => {
    try {
      const response = await fetch(
        "http://192.168.0.224:8000/account/token/refresh/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ refresh: authTokens.refresh }),
        },
      );

      const data = await response.json();
      if (response.ok) {
        setAuthTokens({
          access: data.access,
          refresh: authTokens.refresh, // Since refresh token remains the same
        });
        setUser({ user_id: jwtDecode(data.access).user_id }); // Extract user_id from decoded token
        setItemToLocalStorage("accessToken", data.access);
      } else {
        logoutUser();
      }
    } catch (error) {
      console.error("Error updating token:", error);
      logoutUser();
    }
  }, [authTokens.refresh, logoutUser]);

  const isLoggedIn = authTokens.access !== null;

  useEffect(() => {
    if (authTokens.access) {
      const tokenExpiration = jwtDecode(authTokens.access).exp * 1000;
      const currentTime = new Date().getTime();

      console.log("Current Time:", new Date(currentTime));
      console.log("Token Expiration Time:", new Date(tokenExpiration));

      const timeBeforeExpiration = tokenExpiration - currentTime - 1000; // 1 second before token expiration

      if (timeBeforeExpiration < 0) {
        // Token already expired, call updateToken immediately
        updateToken();
      } else {
        // Schedule the next token check just before 1 second before token expiration
        const timeout = setTimeout(() => {
          updateToken();
        }, timeBeforeExpiration);

        // Clean up the timeout on component unmount`
        return () => clearTimeout(timeout);
      }
    }
  }, [authTokens.access, updateToken]); // Include authTokens.access as a dependency

  useEffect(() => {
    // console.log("User updated:", user); // Debug log for updated user state
    setLoading(false);
  }, [user]);

  const contextData = {
    loginUser,
    logoutUser,
    authTokens,
    userId: user ? user.user_id : null, // Assuming user is an object with a user_id field
    userType: user ? user.user_type : null,
    isLoggedIn,
    loading,
  };
  return (
    <AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
  );
};
