from fastapi import APIRouter, Depends

from ..auth.service import user_service

from .styrol_polymerization_bulk.router import router as router_styrol_polymerization_bulk


router_labs = APIRouter(
    prefix='/labs',
    # tags=['Labs'],
    dependencies=[Depends(user_service.get_current_user)],
)

router_labs.include_router(router_styrol_polymerization_bulk)
