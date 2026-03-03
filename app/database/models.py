from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Float,
    Text,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.db import Base


# ===================== USER =====================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    role = Column(String, default="USER")
    is_banned = Column(Boolean, default=False)

    bio = Column(Text, default="")
    profile_pic = Column(String, nullable=True)

    # 🔹 Content
    posts = relationship(
        "Post",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    comments = relationship(
        "Comment",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    likes = relationship(
        "Like",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # 🔹 Social graph
    followers = relationship(
        "Follow",
        foreign_keys="Follow.following_id",
        back_populates="following",
        cascade="all, delete-orphan",
    )

    following = relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User {self.username}>"


# ===================== POST =====================
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    media_url = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), index=True)

    is_flagged = Column(Boolean, default=False)
    bullying_score = Column(Float, default=0.0)
    status = Column(String, default="ACTIVE")

    owner = relationship("User", back_populates="posts")

    likes = relationship(
        "Like",
        back_populates="post",
        cascade="all, delete-orphan",
    )

    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Post id={self.id} owner={self.owner_id}>"


# ===================== LIKE =====================
class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, index=True)

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_like"),
    )

    def __repr__(self):
        return f"<Like user={self.user_id} post={self.post_id}>"


# ===================== COMMENT =====================
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def __repr__(self):
        return f"<Comment id={self.id} post={self.post_id}>"


# ===================== FOLLOW =====================
class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    follower = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following",
    )

    following = relationship(
        "User",
        foreign_keys=[following_id],
        back_populates="followers",
    )

    __table_args__ = (
        UniqueConstraint("follower_id", "following_id", name="unique_follow"),
    )

    def __repr__(self):
        return f"<Follow {self.follower_id} -> {self.following_id}>"


# ===================== CHAT =====================
class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)

    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])

    messages = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="unique_chat_pair"),
    )

    def __repr__(self):
        return f"<Chat {self.user1_id} & {self.user2_id}>"


# ===================== MESSAGE =====================
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    media_url = Column(String, nullable=True)
    status = Column(String, default="SENT")  # SENT / DELIVERED / SEEN
    timestamp = Column(String)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User")

# ===================== AI MODERATION LOG =====================
class AIModerationLog(Base):
    __tablename__ = "ai_moderation_logs"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    score = Column(Float)
    reasons = Column(Text)  # comma separated
    decision = Column(String, default="pending")  # pending / approved / rejected
