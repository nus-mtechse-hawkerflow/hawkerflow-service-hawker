from collections import defaultdict

from sqlalchemy import Engine
from sqlmodel import Session, select

from entities.stalls import Stalls
from entities.stall_menu import StallMenu
from entities.stall_owner import StallOwner
from models.hawker_details import HawkerDetails


class HawkerRepository:
    def __init__(self, engine: Engine):
        self._engine = engine

    def create_hawker(self, hawker_details: HawkerDetails):
        with Session(self._engine) as session:

            stall = Stalls(
                f_stall_name=hawker_details.stall_name,
                f_stall_description=hawker_details.stall_description
            )

            stall_owner = StallOwner(
                f_stall_owner_name=hawker_details.stall_owner.name,
                f_stall_owner_phone=hawker_details.stall_owner.phone,
                f_stall_owner_sub=hawker_details.stall_owner.stall_owner_sub,
                f_stall_owner_email=hawker_details.stall_owner.email
            )

            stall.stall_owner = stall_owner

            for menu in hawker_details.stall_menu:
                stall_menu = StallMenu(
                    f_menu_name=menu.name,
                    f_menu_price=menu.price,
                    f_menu_description=menu.description
                )

                stall.stall_menu.append(stall_menu)

            session.add(stall)
            session.commit()
            session.refresh(stall)

            return stall

    def get_all_hawker(self):
        with Session(self._engine) as session:
            statement = select(Stalls)
            result = session.exec(statement)

            stall_list = []

            for stall in result.all():
                stall_list.append(
                    {
                        "stall_name": stall.f_stall_name,
                        "stall_description": stall.f_stall_description,
                        "stall_menu": [
                            menu.model_dump(
                                exclude={"f_created_at", "f_updated_at"}
                            ) for menu in stall.stall_menu
                        ],
                        "stall_owner": [stall.stall_owner.model_dump()]
                    }
                )

            return stall_list

    def get_hawker_by_sub(self, hawker_sub: str) -> dict[str, int | float | str]:

        with Session(self._engine) as session:
            stall_details = defaultdict()

            statement = select(StallOwner).where(StallOwner.f_stall_owner_sub == hawker_sub)
            stall_owner = session.exec(statement).one()

            stall_details["stall_id"] = stall_owner.stall.f_stall_id
            stall_details["stall_name"] = stall_owner.stall.f_stall_name
            stall_details["stall_menu"] = [
                {
                    "menu_id": menu.f_menu_id,
                    "menu_name": menu.f_menu_name,
                    "menu_price": menu.f_menu_price,
                    "menu_description": menu.f_menu_description
                } for menu in stall_owner.stall.stall_menu
            ]

            return stall_details
