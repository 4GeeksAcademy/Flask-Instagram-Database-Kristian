from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    following: Mapped[list['Follower']]= relationship(back_populates= 'user_from_id')
    followers: Mapped[list['Follower']]= relationship(back_populates= 'user_to_id')
    post: Mapped[list['Post']]= relationship(back_populates= 'user_post')
    comment: Mapped[list['Comment']]= relationship(back_populates= 'user_comment')


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    follower_user: Mapped['User']= relationship(back_populates= 'following')
    followed_user: Mapped['User']= relationship(back_populates= 'followers')

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user_post: Mapped['User'] = relationship(back_populates= 'post')
    post_media: Mapped['Media'] = relationship(back_populates= 'media_post')
    comment_post: Mapped['Comment'] = relationship(back_populates= '')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    media_post: Mapped['Post'] = relationship(back_populates= 'post_media')

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "post_id": self.post_id
        }
    
class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(), nullable=False)
    author_id: Mapped[str] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[str] = mapped_column(ForeignKey('post.id'))
    user_comment: Mapped['User'] = relationship(back_populates= 'comment')
    post_comment: Mapped['Post'] = relationship(back_populates= 'comment_post')

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }
