// import React, { useState, useEffect } from "react";

// function Dashboard() {
//   const [admins, setAdmins] = useState([]);
//   const [users, setUsers] = useState([]);
//   const [adminCount, setAdminCount] = useState(0);
//   const [userCount, setUserCount] = useState(0);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     async function fetchData() {
//       try {
//         const token = localStorage.getItem("accessToken");
//         const response = await fetch(
//           "http://192.168.0.224:8000/components/dashboard/",
//           {
//             method: "GET",
//             headers: {
//               Authorization: `Bearer ${token}`,
//             },
//           },
//         );

//         if (!response.ok) {
//           throw new Error("Failed to fetch data");
//         }

//         const data = await response.json();
//         setAdmins(data.admins);
//         setUsers(data.users);
//         setAdminCount(data.admin_count);
//         setUserCount(data.user_count);
//       } catch (error) {
//         setError(error.message);
//       }
//     }

//     fetchData();
//   }, []);

//   if (error) {
//     return <div>Error: {error}</div>;
//   }

//   return (
//     <div>
//       <h2>Admins ({adminCount}):</h2>
//       <ul>
//         {admins.map((admin) => (
//           <li key={admin.id}>
//             <p>Username: {admin.admin_username}</p>
//             <p>
//               Name: {admin.admin_firstname} {admin.admin_lastname}
//             </p>
//             <p>Email: {admin.admin_email}</p>
//             <p>Mobile: {admin.admin_mobile}</p>
//           </li>
//         ))}
//       </ul>

//       <h2>Users ({userCount}):</h2>
//       <ul>
//         {users.map((user) => (
//           <li key={user.id}>
//             <p>Username: {user.user_username}</p>
//             <p>
//               Name: {user.user_firstname} {user.user_lastname}
//             </p>
//             <p>Email: {user.user_email}</p>
//             <p>Mobile: {user.user_mobile}</p>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// }

// export default Dashboard;



































import React, { useState, useEffect } from 'react';

const WebSocketComponent = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // Establish WebSocket connection
    const socket = new WebSocket('ws://192.168.0.224:8000/wc/sc/');

    // Event handler for successful connection
    socket.onopen = () => {
      console.log('Connected to WebSocket server');
    };

    // Event handler for incoming messages
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Update the messages state with the new message
      setMessages(prevMessages => [...prevMessages, data]);
    };

    // Event handler for connection closure
    socket.onclose = () => {
      console.log('Disconnected from WebSocket server');
    };

    // Clean up function to close WebSocket connection when component unmounts
    return () => {
      socket.close();
    };
  }, []); // Empty dependency array ensures useEffect runs only once on component mount

  return (
    <div>
      <h1>Random Numbers</h1>
      <ul>
        {messages.map((number, index) => (
          <li key={index}>{number}</li>
        ))}
      </ul>
    </div>
  );
};

export default WebSocketComponent;
