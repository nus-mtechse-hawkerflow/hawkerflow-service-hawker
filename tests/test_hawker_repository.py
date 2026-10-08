from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine

from entities.stall_menu import StallMenu  # noqa: F401  (registers the table)
from entities.stall_owner import StallOwner  # noqa: F401
from entities.stalls import Stalls  # noqa: F401
from models.hawker_details import HawkerDetails
from repository.hawker_repository import HawkerRepository


def _repo() -> HawkerRepository:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return HawkerRepository(engine)


def _details() -> HawkerDetails:
    return HawkerDetails(
        stall_name="Ah Huat Chicken Rice",
        stall_number="#01-28",
        stall_description="Hainanese chicken rice",
        stall_location="Maxwell Food Centre",
        stall_menu=[{"name": "Steamed Chicken Rice", "price": 4.5, "description": ""}],
        stall_owner={
            "stall_owner_sub": "sub-123",
            "name": "Uncle Tan",
            "phone": "+6591234567",
            "email": "ahhuat@maxwell.sg",
        },
    )


def test_public_stall_list_names_the_owner_and_stall():
    repo = _repo()
    repo.create_hawker(_details())

    [stall] = repo.get_all_hawker()

    assert stall["stall_name"] == "Ah Huat Chicken Rice"
    assert stall["stall_owner"] == [{"f_stall_id": 1, "f_stall_owner_name": "Uncle Tan"}]
    assert [m["f_menu_name"] for m in stall["stall_menu"]] == ["Steamed Chicken Rice"]


def test_public_stall_list_does_not_expose_owner_contact_or_identity():
    repo = _repo()
    repo.create_hawker(_details())

    [stall] = repo.get_all_hawker()

    exposed = str(stall)
    assert "ahhuat@maxwell.sg" not in exposed
    assert "+6591234567" not in exposed
    assert "sub-123" not in exposed


def test_owner_can_still_load_their_own_stall_by_sub():
    repo = _repo()
    repo.create_hawker(_details())

    stall = repo.get_hawker_by_sub("sub-123")

    assert stall["stall_id"] == 1
    assert stall["stall_name"] == "Ah Huat Chicken Rice"
