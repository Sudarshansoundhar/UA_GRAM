import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../api/api";
import Navbar from "../components/Navbar";


export default function Profile() {
  const { username } = useParams();
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  const loggedInUsername = localStorage.getItem("username");

  // ✅ STRONG AUTH GUARD
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }
    fetchProfile();
    // eslint-disable-next-line
  }, [username]);

  const fetchProfile = async () => {
    try {
      const res = await API.get(`/profile/${username}`);
      setProfile(res.data);
    } catch (err) {
      console.error(err);

      if (err.response?.status === 401) {
        localStorage.clear();
        navigate("/login");
      } else {
        alert("Profile not found");
        navigate("/feed");
      }
    } finally {
      setLoading(false);
    }
  };

  const toggleFollow = async () => {
    try {
      await API.post(`/profile/${username}/follow`);
      fetchProfile();
    } catch (err) {
      console.error(err);
    }
  };

  const startDM = async () => {
    try {
      const res = await API.post(`/dm/${username}`);

      // ✅ FIXED ROUTE
      navigate(`/chat/${res.data.chat_id}`);
    } catch (err) {
      console.error(err);
      alert("Failed to start chat");
    }
  };

  if (loading) {
    return (
      <>
        <Navbar />
        <p style={{ textAlign: "center", marginTop: 50 }}>Loading...</p>
      </>
    );
  }

  if (!profile) return null;

  const isSelf = loggedInUsername === profile.username;

  return (
    <>
      <Navbar />

      <div style={{ maxWidth: 800, margin: "auto", padding: 20 }}>
        {/* HEADER */}
        <div style={{ display: "flex", gap: 30, alignItems: "center" }}>
          <img
            src={
              profile.profile_pic
                ? `http://127.0.0.1:8000/uploads/profile/${profile.profile_pic}`
                : "https://via.placeholder.com/120"
            }
            width="120"
            height="120"
            style={{ borderRadius: "50%", objectFit: "cover" }}
            alt="profile"
          />

          <div>
            <h2>@{profile.username}</h2>

            <div style={{ display: "flex", gap: 20, margin: "10px 0" }}>
              <span>
                <b>{profile.posts?.length || 0}</b> posts
              </span>
              <span>
                <b>{profile.followers || 0}</b> followers
              </span>
              <span>
                <b>{profile.following || 0}</b> following
              </span>
            </div>

            {/* ACTION BUTTONS */}
            {isSelf ? (
              <button onClick={() => navigate("/edit-profile")}>
                Edit Profile
              </button>
            ) : (
              <>
                <button onClick={toggleFollow}>
                  {profile.is_following ? "Unfollow" : "Follow"}
                </button>

                <button onClick={startDM} style={{ marginLeft: 10 }}>
                  Message
                </button>
              </>
            )}

            <p style={{ marginTop: 10 }}>
              {profile.bio || "No bio yet"}
            </p>
          </div>
        </div>

        {/* POSTS GRID */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: 10,
            marginTop: 30,
          }}
        >
          {(profile.posts || []).map((p) => (
            <div key={p.id}>
              {p.media_url &&
                (p.media_url.endsWith(".mp4") ? (
                  <video width="100%" controls>
                    <source
                      src={`http://127.0.0.1:8000/uploads/${p.media_url}`}
                    />
                  </video>
                ) : (
                  <img
                    src={`http://127.0.0.1:8000/uploads/${p.media_url}`}
                    width="100%"
                    alt="post"
                  />
                ))}
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

