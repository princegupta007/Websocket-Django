import React, { useState, useContext } from "react";
import AuthContext from "../context/AuthContext";

function CreateEntityForm() {
  const { userType, userId } = useContext(AuthContext);

  const [formData, setFormData] = useState({
    username: "",
    firstname: "",
    lastname: "",
    email: "",
    mobile: "",
    password: "",
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem("accessToken");
      let apiUrl = "";
      let requestBody = { ...formData }; // Make a copy of formData

      if (userType === "superadmin") {
        apiUrl = "http://192.168.0.224:8000/components/create_admin/";
        requestBody = {
          ...requestBody,
          admin_username: formData.username,
          admin_firstname: formData.firstname,
          admin_lastname: formData.lastname,
          admin_email: formData.email,
          admin_mobile: formData.mobile,
          admin_password: formData.password,
          superadmin: userId,
        };
      } else if (userType === "admin") {
        apiUrl = "http://192.168.0.224:8000/components/create_user/";
        requestBody = {
          ...requestBody,
          user_username: formData.username,
          user_firstname: formData.firstname,
          user_lastname: formData.lastname,
          user_email: formData.email,
          user_mobile: formData.mobile,
          user_password: formData.password,
          admin: userId,
        };
      }

      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail);
      }
      console.log("Entity created successfully");
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Username:
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
        />
      </label>
      <label>
        First Name:
        <input
          type="text"
          name="firstname"
          value={formData.firstname}
          onChange={handleChange}
          required
        />
      </label>
      <label>
        Last Name:
        <input
          type="text"
          name="lastname"
          value={formData.lastname}
          onChange={handleChange}
          required
        />
      </label>
      <label>
        Email:
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </label>
      <label>
        Mobile:
        <input
          type="text"
          name="mobile"
          value={formData.mobile}
          onChange={handleChange}
          required
        />
      </label>
      <label>
        Password:
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
      </label>
      <button type="submit" disabled={isLoading}>
        {isLoading ? "Creating..." : "Create Entity"}
      </button>
      {error && <div>Error: {error}</div>}
    </form>
  );
}

export default CreateEntityForm;
