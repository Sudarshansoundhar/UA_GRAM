import { useEffect, useState } from "react";
import API from "../api/api";

export default function Comments({ postId }) {
  const [comments, setComments] = useState([]);
  const [text, setText] = useState("");

  const loadComments = async () => {
    const res = await API.get(`/comments/${postId}`);
    setComments(res.data);
  };

  const addComment = async () => {
    await API.post(`/comments/${postId}`, null, {
      params: { content: text }
    });
    setText("");
    loadComments();
  };

  useEffect(() => {
    loadComments();
  }, []);

  return (
    <div>
      {comments.map((c) => (
        <p key={c.id}>
          <b>@{c.owner}</b>: {c.content}
        </p>
      ))}

      <input
        placeholder="Add a comment..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={addComment}>Post</button>
    </div>
  );
}
