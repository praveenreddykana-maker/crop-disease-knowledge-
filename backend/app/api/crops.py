"""
Crop disease info API - returns structured crop disease information.
"""

from fastapi import APIRouter, HTTPException
from app.core.knowledge_base import CROP_DISEASE_DATA

router = APIRouter(prefix="/api/crops", tags=["Crops"])

SUPPORTED_CROPS = ["Rice", "Wheat", "Tomato", "Potato", "Cotton", "Maize", "Groundnut"]


@router.get("/")
async def get_supported_crops():
    """Return list of supported crops."""
    crop_counts = {}
    for disease in CROP_DISEASE_DATA:
        crop = disease["crop"]
        if crop != "All Crops":
            crop_counts[crop] = crop_counts.get(crop, 0) + 1

    return {
        "crops": [
            {"name": crop, "disease_count": crop_counts.get(crop, 0)}
            for crop in SUPPORTED_CROPS
        ]
    }


@router.get("/{crop_name}/diseases")
async def get_crop_diseases(crop_name: str):
    """Get all diseases for a specific crop."""
    crop_name_title = crop_name.title()
    diseases = [
        d for d in CROP_DISEASE_DATA
        if d["crop"].lower() == crop_name_title.lower()
    ]
    if not diseases:
        raise HTTPException(status_code=404, detail=f"No disease data found for crop '{crop_name}'.")
    return {"crop": crop_name_title, "diseases": diseases}


@router.get("/{crop_name}/diseases/{disease_name}")
async def get_disease_detail(crop_name: str, disease_name: str):
    """Get detailed information for a specific disease."""
    matches = [
        d for d in CROP_DISEASE_DATA
        if d["crop"].lower() == crop_name.lower()
        and disease_name.lower() in d["disease"].lower()
    ]
    if not matches:
        raise HTTPException(status_code=404, detail="Disease information not found.")
    return matches[0]

