import { useState, useEffect } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";


export default function EditProfile() {
  const [bio, setBio] = useState("");
  const [profilePic, setProfilePic] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // ✅ AUTH GUARD
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/login");
  }, [navigate]);

  const submit = async () => {
    if (loading) return;

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("bio", bio);

      if (profilePic) {
        formData.append("profile_pic", profilePic);
      }

      await API.put("/profile/edit", formData);

      alert("Profile updated");
      navigate("/feed");
    } catch (err) {
      console.error(err);
      alert("Failed to update profile");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div style={{ maxWidth: 400, margin: "auto" }}>
        <h2>Edit Profile</h2>

        <textarea
          placeholder="Your bio"
          value={bio}
          onChange={(e) => setBio(e.target.value)}
          style={{ width: "100%", height: 80 }}
        />

        <input
          type="file"
          accept="image/*"
          onChange={(e) => setProfilePic(e.target.files[0])}
        />

        <button onClick={submit} disabled={loading}>
          {loading ? "Saving..." : "Save"}
        </button>
      </div>
    </>
  );
}


