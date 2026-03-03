import { useState } from "react";
import API from "../api/api";
import socket from "../socket";

export default function CreatePost({ onPostCreated }) {
  const [caption, setCaption] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    if (!file) {
      alert("Select an image");
      return;
    }

    if (!caption.trim()) {
      alert("Caption cannot be empty");
      return;
    }

    try {
      setLoading(true);

      const fd = new FormData();
      fd.append("caption", caption.trim());
      fd.append("media", file);

      const res = await API.post("/posts/create", fd);

      // ⚠ AI WARNING HANDLING
      if (res.data?.warning) {
        const go = confirm("⚠ AI detected harmful caption. Post anyway?");
        if (!go) return;
      }

      // 🔥 realtime update
      socket.emit("new_post");

      // reset form
      setCaption("");
      setFile(null);

      if (onPostCreated) onPostCreated();
    } catch (err) {
      console.error("Create post error:", err);

      // 🚫 AI BLOCK MESSAGE SUPPORT
      const msg =
        err.response?.data?.detail?.message ||
        err.response?.data?.detail ||
        "Upload failed";

      alert(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginBottom: 20 }}>
      <input
        placeholder="Write something..."
        value={caption}
        onChange={(e) => setCaption(e.target.value)}
      />

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={submit} disabled={loading}>
        {loading ? "Posting..." : "Post"}
      </button>
    </div>
  );
}