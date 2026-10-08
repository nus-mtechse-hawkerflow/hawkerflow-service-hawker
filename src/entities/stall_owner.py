from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .stalls import Stalls


class StallOwner(SQLModel, table=True):
    __tablename__ = "stall_owner"

    f_stall_owner_id: int = Field(default=None, primary_key=True)
    f_stall_owner_sub: str
    f_stall_id: int = Field(foreign_key="stalls.f_stall_id")
    f_stall_owner_name: str
    f_stall_owner_phone: str
    f_stall_owner_email: str

    stall: "Stalls" = Relationship(back_populates="stall_owner")
