import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Feed from "./pages/Feed";
import Profile from "./pages/Profile";
import EditProfile from "./pages/EditProfile";
import Chat from "./pages/Chat";
import AdminAI from "./pages/AdminAI";

// 🔒 Protected Route
function ProtectedRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" replace />;
}

// 🌐 Public Route
function PublicRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? <Navigate to="/feed" replace /> : children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ================= PUBLIC ROUTES ================= */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />

        <Route
          path="/register"
          element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          }
        />

        {/* ================= PROTECTED ROUTES ================= */}
        <Route
          path="/feed"
          element={
            <ProtectedRoute>
              <Feed />
            </ProtectedRoute>
          }
        />

        <Route
          path="/profile/:username"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />

        <Route
          path="/edit-profile"
          element={
            <ProtectedRoute>
              <EditProfile />
            </ProtectedRoute>
          }
        />

        {/* CHAT ROUTES */}
        <Route
          path="/chat/:chatId"
          element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          }
        />

        {/* BACKWARD COMPATIBILITY */}
        <Route
          path="/dm/:chatId"
          element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          }
        />

        {/* ADMIN AI PANEL (PROTECTED) */}
        <Route
          path="/admin-ai"
          element={
            <ProtectedRoute>
              <AdminAI />
            </ProtectedRoute>
          }
        />

        {/* DEFAULT ROUTE */}
        <Route
          path="/"
          element={
            localStorage.getItem("token")
              ? <Navigate to="/feed" replace />
              : <Navigate to="/login" replace />
          }
        />

        {/* FALLBACK */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
