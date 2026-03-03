import express from "express";
import http from "http";
import { Server } from "socket.io";
import cors from "cors";

const app = express();
app.use(cors());

const server = http.createServer(app);

const io = new Server(server, {
  cors: { origin: "*" },
});

io.on("connection", (socket) => {
  console.log("User connected:", socket.id);

  // FEED
  socket.on("like_post", (data) => io.emit("post_liked", data));
  socket.on("comment_post", (data) => io.emit("post_commented", data));
  socket.on("new_post", () => io.emit("refresh_feed"));

  // DM
  socket.on("join_dm", (chatId) => {
    socket.join(chatId.toString());
  });

  socket.on("send_dm", ({ chatId, message }) => {
    io.to(chatId.toString()).emit("receive_dm", message);
  });

  socket.on("message_seen", (chatId) => {
    io.to(chatId.toString()).emit("seen_update");
  });

  socket.on("disconnect", () => {
    console.log("User disconnected:", socket.id);
  });
});

server.listen(5000, () => {
  console.log("⚡ Realtime server running on http://localhost:5000");
});
