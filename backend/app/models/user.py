import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    """
    Local mirror of a Supabase-authenticated user.

    Supabase Auth owns identity end-to-end (registration, login, password
    reset, sessions). FastAPI never issues or manages credentials - this
    table exists only so other tables have a local integer FK target,
    anchored back to Supabase via `supabase_id`.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    supabase_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )