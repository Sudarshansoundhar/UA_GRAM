import { useEffect, useState } from "react";
import API from "../api/api";

export default function AdminAI() {
  const [logs, setLogs] = useState([]);

  const loadLogs = async () => {
    const res = await API.get("/admin/ai/logs");
    setLogs(res.data);
  };

  useEffect(() => {
    loadLogs();
  }, []);

  const approve = async (id) => {
    await API.post(`/admin/ai/approve/${id}`);
    loadLogs();
  };

  const reject = async (id) => {
    await API.post(`/admin/ai/reject/${id}`);
    loadLogs();
  };

  return (
    <div style={{ maxWidth: 800, margin: "auto" }}>
      <h2>AI Moderation Panel</h2>

      {logs.map((log) => (
        <div key={log.id} style={{ border: "1px solid #ccc", padding: 10, marginBottom: 10 }}>
          <b>Text:</b> {log.content}
          <br />
          <b>Score:</b> {log.score.toFixed(2)}
          <br />
          <b>Reasons:</b> {log.reasons.join(", ")}
          <br />
          <b>Status:</b> {log.decision}

          <div style={{ marginTop: 5 }}>
            <button onClick={() => approve(log.id)}>Approve AI</button>
            <button onClick={() => reject(log.id)} style={{ marginLeft: 10 }}>
              Reject AI
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
