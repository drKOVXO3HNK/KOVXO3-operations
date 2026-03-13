from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field


class FieldItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    group_name: Optional[str] = None
    area_ha: float = 0


class CropItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class OperationItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    season: int
    operation_type: str
    field_id: int
    crop_id: Optional[int] = None
    planned_area_ha: float = 0
    completed_area_ha: float = 0
    status: str = "planned"
    planned_date: Optional[date] = None
    completed_date: Optional[date] = None
    notes: Optional[str] = None
