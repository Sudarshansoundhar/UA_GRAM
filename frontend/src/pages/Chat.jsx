import { useEffect, useRef, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../api/api";
import Navbar from "../components/Navbar";
import socket from "../socket";
import EmojiPicker from "emoji-picker-react";

export default function Chat() {
  const { chatId } = useParams();
  const navigate = useNavigate();
  const username = localStorage.getItem("username");

  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [showEmoji, setShowEmoji] = useState(false);

  const bottomRef = useRef(null);

  useEffect(() => {
    if (!localStorage.getItem("token")) navigate("/login");
  }, [navigate]);

  // Load history
  useEffect(() => {
    API.get(`/dm/${chatId}`).then(res => setMessages(res.data || []));
  }, [chatId]);

  // Socket listeners
  useEffect(() => {
    socket.emit("join_dm", chatId);
    socket.emit("message_seen", chatId);

    const handleReceive = (msg) => {
      if (msg.sender === username) return;
      setMessages(prev => [...prev, msg]);
    };

    const handleSeen = () => {
      setMessages(prev =>
        prev.map(m =>
          m.sender === username ? { ...m, status: "SEEN" } : m
        )
      );
    };

    socket.on("receive_dm", handleReceive);
    socket.on("seen_update", handleSeen);

    return () => {
      socket.off("receive_dm", handleReceive);
      socket.off("seen_update", handleSeen);
    };
  }, [chatId, username]);

  // Auto scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // SEND MESSAGE (AI SAFE)
  const sendMessage = async () => {
    if (!text && !file) return;

    try {
      const fd = new FormData();
      if (text) fd.append("content", text);
      if (file) fd.append("media", file);

      const res = await API.post(`/dm/${chatId}/send`, fd);

      if (res.data?.level === "block") {
        const reasonText = res.data.reasons?.join("\n• ") || "Toxic content";
        alert(`🚫 Message blocked\n\n• ${reasonText}`);
        return;
      }

      if (res.data?.level === "warn") {
        const proceed = confirm("⚠ AI Warning. Send anyway?");
        if (!proceed) return;

        const bypassRes = await API.post(
          `/dm/${chatId}/send?bypass_ai=true`,
          fd
        );

        socket.emit("send_dm", { chatId, message: bypassRes.data });
        setMessages(prev => [...prev, bypassRes.data]);
        setText("");
        setFile(null);
        return;
      }

      socket.emit("send_dm", { chatId, message: res.data });
      setMessages(prev => [...prev, res.data]);
      setText("");
      setFile(null);
    } catch {
      alert("Send failed");
    }
  };

  // 🗑 DELETE MESSAGE
  const deleteMessage = async (id) => {
    if (!confirm("Delete this message?")) return;

    await API.delete(`/dm/message/${id}`);

    setMessages(prev => prev.filter(m => m.id !== id));
  };

  const styles = {
    wrapper: {
      maxWidth: "700px",
      margin: "20px auto",
      height: "calc(100vh - 90px)",
      display: "flex",
      flexDirection: "column",
      background: "#f5f7fb",
      borderRadius: "14px",
      overflow: "hidden",
      boxShadow: "0 10px 30px rgba(0,0,0,0.08)"
    },
    messagesArea: {
      flex: 1,
      overflowY: "auto",
      padding: "16px"
    },
    row: (isMe) => ({
      textAlign: isMe ? "right" : "left",
      marginBottom: "10px"
    }),
    bubble: (isMe) => ({
      display: "inline-block",
      padding: "10px 12px",
      borderRadius: "14px",
      background: isMe ? "#6366f1" : "#e5e7eb",
      color: isMe ? "#fff" : "#111",
      maxWidth: "70%",
      fontSize: "14px",
      position: "relative"
    }),
    deleteBtn: {
      fontSize: "10px",
      color: "#ff4d4f",
      cursor: "pointer",
      marginLeft: 6
    },
    inputBar: {
      borderTop: "1px solid #e5e7eb",
      padding: "10px",
      background: "#fff",
      display: "flex",
      gap: "6px"
    },
    textInput: {
      flex: 1,
      padding: "10px",
      borderRadius: "10px",
      border: "1px solid #ddd"
    },
    sendBtn: {
      background: "#6366f1",
      border: "none",
      color: "#fff",
      padding: "8px 14px",
      borderRadius: "8px"
    }
  };

  return (
    <>
      <Navbar />

      <div style={styles.wrapper}>
        <div style={styles.messagesArea}>
          {messages.map((m, i) => {
            const isMe = m.sender === username;
            return (
              <div key={i} style={styles.row(isMe)}>
                <div style={styles.bubble(isMe)}>
                  {m.content}

                  {isMe && (
                    <span
                      style={styles.deleteBtn}
                      onClick={() => deleteMessage(m.id)}
                    >
                      delete
                    </span>
                  )}
                </div>
              </div>
            );
          })}
          <div ref={bottomRef} />
        </div>

        <div style={styles.inputBar}>
          <input
            value={text}
            onChange={(e) => setText(e.target.value)}
            style={styles.textInput}
            placeholder="Type a message..."
          />

          <input type="file" onChange={(e) => setFile(e.target.files[0])} />

          <button style={styles.sendBtn} onClick={sendMessage}>
            Send
          </button>
        </div>
      </div>
    </>
  );
}