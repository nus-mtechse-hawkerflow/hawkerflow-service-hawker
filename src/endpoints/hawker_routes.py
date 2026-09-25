from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from models.hawker_details import HawkerDetails
from hawker_service.hawker_service import HawkerService


hawker_router = APIRouter(prefix="/v1/hawker")


def get_hawker_service(request: Request):
    return request.app.state.hawker_service


@hawker_router.post("/register")
async def register_hawker(
    hawker_details: HawkerDetails,
    hawker_service: Annotated[HawkerService, Depends(get_hawker_service)],
):
    stall = hawker_service.create_hawker(hawker_details)

    return JSONResponse(
        content={
            "stall_name": stall.f_stall_name
        },
        status_code=201
    )


@hawker_router.get("/stalls")
async def get_stalls(hawker_service: Annotated[HawkerService, Depends(get_hawker_service)]):
    stalls = hawker_service.get_all_hawker()

    return JSONResponse(
        content={
            "stalls": stalls
        },
        status_code=200
    )


@hawker_router.get("/me/stall/{hawker_sub}")
async def get_my_stall(
        hawker_sub: str,
        hawker_service: Annotated[HawkerService, Depends(get_hawker_service)]
):
    stall_detail = hawker_service.get_hawker_by_sub(hawker_sub)

    return JSONResponse(
        content={
            **stall_detail
        },
        status_code=200
    )
