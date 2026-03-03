import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/api";


export default function Navbar() {
  const token = localStorage.getItem("token");
  const username = localStorage.getItem("username");

  // 🚫 HARD STOP — Navbar DOES NOT EXIST without auth
  if (!token || !username) {
    return null;
  }

  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    API.get(`/profile/${username}`)
      .then((res) => setUser(res.data))
      .catch(() => console.log("Navbar user load failed"));
  }, [username]);

  // ✅ LOGOUT FUNCTION (ADDED)
  const handleLogout = () => {
    // Remove auth data
    localStorage.removeItem("token");
    localStorage.removeItem("username");

    // OPTIONAL: if you later store more auth data
    // localStorage.clear();

    // Redirect to login
    navigate("/login");
  };
const styles = {
  nav: {
    height: "64px",
    position: "sticky",
    top: 0,
    background: "rgba(255,255,255,0.8)",
    backdropFilter: "blur(12px)",
    borderBottom: "1px solid #e5e7eb",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 24px",
    zIndex: 1000
  },
  brand: {
    fontWeight: "700",
    fontSize: "18px",
    color: "#6366f1",
    cursor: "pointer",
    letterSpacing: "0.3px"
  },
  right: {
    display: "flex",
    alignItems: "center",
    gap: "14px"
  },
  avatar: {
    width: "40px",
    height: "40px",
    borderRadius: "50%",
    objectFit: "cover",
    cursor: "pointer",
    border: "2px solid #6366f1"
  },
  logout: {
    background: "#ef4444",
    color: "#fff",
    border: "none",
    padding: "6px 14px",
    borderRadius: "999px",
    cursor: "pointer",
    fontSize: "13px",
    fontWeight: "600"
  }
};
 return (
  <div style={styles.nav}>
    {/* LEFT BRAND */}
    <div style={styles.brand} onClick={() => navigate("/feed")}>
      SafeSphere
    </div>

    {/* RIGHT SIDE */}
    <div style={styles.right}>
      {user && (
        <img
          src={
            user.profile_pic
              ? `http://127.0.0.1:8000/uploads/profile/${user.profile_pic}`
              : "https://via.placeholder.com/40"
          }
          style={styles.avatar}
          onClick={() => navigate(`/profile/${user.username}`)}
        />
      )}

      <button onClick={handleLogout} style={styles.logout}>
        Logout
      </button>
    </div>
  </div>
);
}
