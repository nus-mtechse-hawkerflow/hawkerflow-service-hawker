from pydantic import BaseModel, EmailStr


class StallMenu(BaseModel):
    name: str
    price: float
    description: str


class StallOwner(BaseModel):
    stall_owner_sub: str
    name: str
    phone: str
    email: EmailStr


class HawkerDetails(BaseModel):
    stall_name: str
    stall_number: str
    stall_description: str
    stall_location: str
    stall_menu: list[StallMenu]
    stall_owner: StallOwner
