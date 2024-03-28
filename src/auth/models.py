from datetime import datetime
from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from uuid import UUID, uuid4
from sqladmin import ModelView
from ..config import settings


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, unique=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    refresh_token: Mapped[list['RefreshToken']] = relationship(back_populates='user', cascade="all, delete")
    
    styrol_polymerization_bulk: Mapped[list["StyrolPolymerizationBulkORM"]] = relationship(back_populates="user")

    if settings.MODE == 'TEST':
        __mapper_args__ = {
            'confirm_deleted_rows': False
        }


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    refresh_token_id: Mapped[int] = mapped_column(primary_key=True)
    refresh_key: Mapped[UUID] = mapped_column(nullable=False)
    exp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    iat: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    access_key: Mapped[UUID] = mapped_column(nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.user_id', ondelete="CASCADE"))

    user: Mapped['User'] = relationship(back_populates='refresh_token')


class UserAdmin(ModelView, model=User):
    column_exclude_list = [User.password, User.refresh_token]
    column_details_exclude_list = [User.password]
    form_columns = [
        User.username,
        User.is_active,
        User.is_verified,
        User.is_superuser
    ]


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_exclude_list = [RefreshToken.user]
    can_edit = False
