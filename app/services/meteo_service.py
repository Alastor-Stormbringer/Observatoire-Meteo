from datetime import datetime, timezone

import requests
from fastapi import HTTPException, status
from pydantic import ValidationError

from app.api.v1.schemas.meteo import WeatherResponseModel


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def obtenir_meteo_actuelle(latitude: float, longitude: float) -> dict:
    try:
        response = requests.get(
            OPEN_METEO_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,wind_speed_10m",
                "timezone": "UTC",
            },
            timeout=10,
        )

        response.raise_for_status()

        data = WeatherResponseModel.model_validate(response.json())
        current = data.current
        units = data.current_units

        return {
            "temperature": current.temperature_2m,
            "vitesse_vent": current.wind_speed_10m,
            "date_heure": datetime.fromisoformat(current.time).replace(
                tzinfo=timezone.utc
            ),
            "unite_temperature": units["temperature_2m"],
            "unite_vitesse_vent": units["wind_speed_10m"],
        }

    except (
        requests.RequestException,
        ValidationError,
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Impossible de récupérer les données météo depuis Open-Meteo.",
        ) from exc