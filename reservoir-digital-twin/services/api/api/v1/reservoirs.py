from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/reservoirs")
def get_reservoirs():
    # Minimal placeholder: return a static GeoJSON feature collection
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Demo Reservoir"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]]],
                },
            }
        ],
    }
    return JSONResponse(content=geojson)
