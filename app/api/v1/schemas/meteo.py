from datetime import datetime
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class MeteoRead(SQLModel):
    ville: str
    temperature: float
    vitesse_vent: float
    date_heure: datetime
    unite_temperature: str
    unite_vitesse_vent: str

class WeatherCurrentModel(BaseModel):
    time: str
    temperature_2m: float
    wind_speed_10m: float


class WeatherResponseModel(BaseModel):
    current: WeatherCurrentModel
    current_units: dict[str, str]