import { useEffect, useState } from "react";
import API from "../api/api";
import { useNavigate, Link } from "react-router-dom";
import CreatePost from "../components/CreatePost";
import Navbar from "../components/Navbar";
import socket from "../socket";

export default function Feed() {
  const navigate = useNavigate();
  const [posts, setPosts] = useState([]);
  const username = localStorage.getItem("username");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/login");
  }, [navigate]);

  const loadPosts = async () => {
    const res = await API.get("/posts");
    setPosts(res.data || []);
  };

  useEffect(() => {
    loadPosts();

    const handleLike = ({ postId, action }) => {
      setPosts(prev =>
        prev.map(p =>
          p.id === postId
            ? {
                ...p,
                likes:
                  action === "like"
                    ? (p.likes ?? 0) + 1
                    : Math.max((p.likes ?? 1) - 1, 0),
              }
            : p
        )
      );
    };

    const handleComment = ({ postId, comment }) => {
      setPosts(prev =>
        prev.map(p =>
          p.id === postId
            ? { ...p, comments: [...p.comments, comment] }
            : p
        )
      );
    };

    const handleRefresh = () => loadPosts();

    socket.on("post_liked", handleLike);
    socket.on("post_commented", handleComment);
    socket.on("refresh_feed", handleRefresh);

    return () => {
      socket.off("post_liked", handleLike);
      socket.off("post_commented", handleComment);
      socket.off("refresh_feed", handleRefresh);
    };
  }, []);

  const likePost = async (postId) => {
    const res = await API.post(`/posts/${postId}/like`);
    socket.emit("like_post", { postId, action: res.data.action });
  };

  // ✅ FIXED AI COMMENT HANDLING
  const addComment = async (postId, text) => {
    if (!text.trim()) return;

    const fd = new FormData();
    fd.append("content", text);

    try {
      const res = await API.post(`/posts/${postId}/comment`, fd);

      // ⚠ AI WARNING
      if (res.data?.warning) {
        const go = confirm("⚠ AI warning. Send comment anyway?");
        if (!go) return;
      }

      socket.emit("comment_post", { postId, comment: res.data });
    } catch (err) {
      const msg =
        err.response?.data?.detail?.message ||
        err.response?.data?.detail ||
        "Comment blocked";
      alert(msg);
    }
  };

  // DELETE POST
  const deletePost = async (postId) => {
    if (!confirm("Delete this post?")) return;
    await API.delete(`/posts/${postId}`);
    setPosts(prev => prev.filter(p => p.id !== postId));
  };

  // DELETE COMMENT
  const deleteComment = async (commentId, postId) => {
    if (!confirm("Delete this comment?")) return;

    await API.delete(`/comments/${commentId}`);

    setPosts(prev =>
      prev.map(p =>
        p.id === postId
          ? { ...p, comments: p.comments.filter(c => c.id !== commentId) }
          : p
      )
    );
  };

  const styles = {
    container: {
      maxWidth: "600px",
      margin: "20px auto",
      padding: "0 12px",
    },
    postCard: {
      background: "#fff",
      borderRadius: "14px",
      boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
      marginBottom: "18px",
      padding: "14px",
    },
    username: {
      fontWeight: "600",
      color: "#111",
      textDecoration: "none",
      fontSize: "15px",
    },
    deleteBtn: {
      marginLeft: 10,
      fontSize: 12,
      color: "red",
      cursor: "pointer",
    },
    content: {
      margin: "10px 0",
      fontSize: "14px",
      color: "#374151",
    },
    image: {
      width: "100%",
      borderRadius: "10px",
      marginTop: "8px",
    },
    actions: {
      marginTop: "10px",
      display: "flex",
      alignItems: "center",
      gap: "12px",
    },
    likeBtn: {
      background: "none",
      border: "none",
      cursor: "pointer",
      fontSize: "15px",
    },
    comments: {
      marginTop: "10px",
      fontSize: "13px",
      color: "#444",
    },
    commentInput: {
      marginTop: "8px",
      width: "100%",
      padding: "8px 10px",
      borderRadius: "8px",
      border: "1px solid #e5e7eb",
      fontSize: "13px",
    },
  };

  return (
    <>
      <Navbar />

      <div style={styles.container}>
        <CreatePost onPostCreated={loadPosts} />

        {posts.map((p) => (
          <div key={p.id} style={styles.postCard}>
            <Link to={`/profile/${p.owner}`} style={styles.username}>
              @{p.owner}
            </Link>

            {p.owner === username && (
              <span
                style={styles.deleteBtn}
                onClick={() => deletePost(p.id)}
              >
                Delete
              </span>
            )}

            <div style={styles.content}>{p.content}</div>

            {p.media_url && (
              <img
                src={`http://127.0.0.1:8000/uploads/${p.media_url}`}
                alt="post"
                style={styles.image}
              />
            )}

            <div style={styles.actions}>
              <button
                style={styles.likeBtn}
                onClick={() => likePost(p.id)}
              >
                ❤️ {p.likes}
              </button>
            </div>

            <div style={styles.comments}>
              {p.comments.map((c) => (
                <div key={c.id}>
                  <b>@{c.owner}</b>: {c.content}
                  {c.owner === username && (
                    <span
                      style={styles.deleteBtn}
                      onClick={() => deleteComment(c.id, p.id)}
                    >
                      delete
                    </span>
                  )}
                </div>
              ))}
            </div>

            <input
              style={styles.commentInput}
              placeholder="Add a comment..."
              onKeyDown={(e) =>
                e.key === "Enter" && addComment(p.id, e.target.value)
              }
            />
          </div>
        ))}
      </div>
    </>
  );
}