from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .stall_menu import StallMenu
    from .stall_owner import StallOwner


class Stalls(SQLModel, table=True):
    __tablename__ = "stalls"

    f_stall_id: int = Field(primary_key=True, default=None)
    f_stall_name: str
    f_stall_description: str

    stall_menu: list["StallMenu"] = Relationship(back_populates="stall")
    stall_owner: "StallOwner" = Relationship(back_populates="stall")
