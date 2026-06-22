from fastapi import APIRouter, HTTPException
from app.api.schemas import (
    HelmetRuleRequest,
    IntersectionRuleRequest,
    WrongSideRuleRequest,
    ParkingRuleRequest,
    SeatbeltRuleRequest,
    TripleRidingRuleRequest,
)
from app.services.helmet_rule import run_helmet_rule
from app.services.intersection_rule import run_intersection_rule
from app.services.wrongside_rule import run_wrongside_rule
from app.services.parking_rule import run_parking_rule
from app.services.seatbelt_rule import run_seatbelt_rule
from app.services.triple_riding_rule import run_triple_riding_rule

router = APIRouter()

@router.post("/rules/helmet")
async def post_helmet_rule(request: HelmetRuleRequest):
    """
    Accepts a tracked-frame job (simulating a consumed queue event),
    and delegates to the helmet violation rule logic.
    """
    try:
        result = await run_helmet_rule(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/rules/intersection")
async def post_intersection_rule(request: IntersectionRuleRequest):
    """
    Accepts a tracked-frame job with signal state and delegates
    to the intersection violation rule (red-light + stop-line).
    """
    try:
        result = await run_intersection_rule(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/rules/wrong-side")
async def post_wrongside_rule(request: WrongSideRuleRequest):
    """
    Accepts a tracked-frame job and delegates to the wrong-side
    driving violation rule (direction vs. allowed lane direction).
    """
    try:
        result = await run_wrongside_rule(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/rules/parking")
async def post_parking_rule(request: ParkingRuleRequest):
    """
    Accepts a tracked-frame job with optional dwell-time state and
    delegates to the illegal parking violation rule.
    """
    try:
        result = await run_parking_rule(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/rules/seatbelt")
async def post_seatbelt_rule(request: SeatbeltRuleRequest):
    """
    Accepts a tracked-frame job with frame image path and delegates
    to the seatbelt violation rule (cabin crop + classification).
    """
    try:
        result = await run_seatbelt_rule(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/rules/triple-riding")
async def post_triple_riding_rule(request: TripleRidingRuleRequest):
    """
    Accepts a tracked-frame job with person + motorcycle tracks and
    delegates to the triple-riding violation rule (rider count ≥ 3).
    """
    try:
        result = await run_triple_riding_rule(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
