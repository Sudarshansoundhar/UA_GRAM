import { useState, useEffect } from "react";
import API from "../api/api";
import { useNavigate, Link } from "react-router-dom";
import socket from "../socket";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [dark, setDark] = useState(false); // 🌗 theme state
  const navigate = useNavigate();

  // Load saved theme
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") setDark(true);
  }, []);

  // SMART RESET
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/feed");
      return;
    }
    localStorage.clear();
    socket.disconnect();
  }, [navigate]);

  const toggleTheme = () => {
    const newTheme = !dark;
    setDark(newTheme);
    localStorage.setItem("theme", newTheme ? "dark" : "light");
  };

  const login = async () => {
    if (!username || !password) {
      alert("Enter username and password");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("username", username);
      formData.append("password", password);

      const res = await API.post("/auth/login", formData);

      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("username", username);

      socket.connect();
      navigate("/feed");
    } catch (err) {
      console.error(err);
      alert("Invalid credentials");
    } finally {
      setLoading(false);
    }
  };

  // 🎨 Dynamic theme styles
  const styles = {
    page: {
      minHeight: "100vh",
      background: dark
        ? "linear-gradient(180deg, #0f172a 0%, #020617 100%)"
        : "linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily:
        "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Inter, sans-serif",
      transition: "all 0.3s ease"
    },

    toggle: {
      position: "absolute",
      top: 20,
      right: 20,
      background: dark ? "#1e293b" : "#fff",
      border: "1px solid #e5e7eb",
      borderRadius: "999px",
      padding: "6px 12px",
      cursor: "pointer",
      fontSize: "13px",
      boxShadow: "0 5px 12px rgba(0,0,0,0.1)"
    },

    card: {
      background: dark ? "#020617" : "#ffffff",
      padding: "44px 38px",
      width: "380px",
      borderRadius: "18px",
      boxShadow: dark
        ? "0 20px 50px rgba(0,0,0,0.6)"
        : "0 20px 50px rgba(0,0,0,0.08)",
      border: dark ? "1px solid #1e293b" : "1px solid #f1f5f9",
      transition: "all 0.3s ease"
    },

    logo: {
      textAlign: "center",
      fontWeight: "800",
      fontSize: "20px",
      letterSpacing: "0.5px",
      color: dark ? "#e2e8f0" : "#1e293b",
      marginBottom: "16px"
    },

    title: {
      fontSize: "26px",
      fontWeight: "700",
      textAlign: "center",
      marginBottom: "6px",
      color: dark ? "#f1f5f9" : "#0f172a"
    },

    subtitle: {
      fontSize: "14px",
      textAlign: "center",
      color: dark ? "#94a3b8" : "#64748b",
      marginBottom: "26px"
    },

    input: {
      width: "100%",
      padding: "14px 15px",
      marginBottom: "14px",
      borderRadius: "12px",
      border: dark ? "1px solid #1e293b" : "1px solid #e2e8f0",
      fontSize: "14px",
      background: dark ? "#020617" : "#f8fafc",
      color: dark ? "#e2e8f0" : "#020617",
      outline: "none"
    },

    button: {
      width: "100%",
      padding: "14px",
      borderRadius: "12px",
      border: "none",
      background: "#2563eb",
      color: "#ffffff",
      fontWeight: "600",
      fontSize: "15px",
      cursor: "pointer",
      marginTop: "4px",
      boxShadow: "0 8px 18px rgba(37,99,235,0.25)"
    },

    switch: {
      textAlign: "center",
      marginTop: "18px",
      fontSize: "14px",
      color: dark ? "#94a3b8" : "#64748b"
    },

    link: {
      color: "#2563eb",
      fontWeight: "600"
    }
  };

  return (
    <div style={styles.page}>
      {/* 🌗 THEME TOGGLE */}
      <div style={styles.toggle} onClick={toggleTheme}>
        {dark ? "☀ Light" : "🌙 Dark"}
      </div>

      <div style={styles.card}>
        <div style={styles.logo}>UAGRAM</div>

        <div style={styles.title}>Welcome back</div>
        <div style={styles.subtitle}>
          Sign in to continue to your network
        </div>

        <input
          style={styles.input}
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          style={styles.input}
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button style={styles.button} onClick={login} disabled={loading}>
          {loading ? "Signing in..." : "Sign in"}
        </button>

        <div style={styles.switch}>
          New here?{" "}
          <Link to="/register" style={styles.link}>
            Create account
          </Link>
        </div>
      </div>
    </div>
  );
}