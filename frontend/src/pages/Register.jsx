import { useState, useEffect } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [dark, setDark] = useState(false);

  const navigate = useNavigate();

  // Load saved theme
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") setDark(true);
  }, []);

  const toggleTheme = () => {
    const newTheme = !dark;
    setDark(newTheme);
    localStorage.setItem("theme", newTheme ? "dark" : "light");
  };

  const register = async () => {
    try {
      const res = await API.post("/auth/register", {
        username,
        email,
        password,
      });

      alert(res.data.message || "Registration successful");
      navigate("/login");
    } catch (err) {
      const data = err.response?.data;

      if (Array.isArray(data)) {
        alert(data.map(e => `${e.loc[1]}: ${e.msg}`).join("\n"));
      } else if (data?.detail) {
        alert(data.detail);
      } else {
        alert("Registration failed");
      }

      console.error("REGISTER ERROR:", data);
    }
  };

  // 🌗 THEME STYLES
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
        "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Inter, sans-serif"
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
      border: dark ? "1px solid #1e293b" : "1px solid #f1f5f9"
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

    footer: {
      textAlign: "center",
      marginTop: "18px",
      fontSize: "14px",
      color: dark ? "#94a3b8" : "#64748b"
    },

    link: {
      color: "#2563eb",
      fontWeight: "600",
      cursor: "pointer"
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

        <div style={styles.title}>Create account</div>
        <div style={styles.subtitle}>
          Join the safe AI-powered network
        </div>

        <input
          style={styles.input}
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          style={styles.input}
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          style={styles.input}
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button style={styles.button} onClick={register}>
          Create account
        </button>

        <div style={styles.footer}>
          Already have an account?{" "}
          <span style={styles.link} onClick={() => navigate("/login")}>
            Sign in
          </span>
        </div>
      </div>
    </div>
  );
}