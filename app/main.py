from datetime import date
from fastapi import FastAPI, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from .db import init_db, get_session
from .models import FieldItem, CropItem, OperationItem

app = FastAPI(title="KOVXO3 Operations")
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return RedirectResponse(url="/dashboard")


@app.get("/dashboard")
def dashboard(request: Request, season: int | None = None, session: Session = Depends(get_session)):
    season = season or date.today().year

    fields = session.exec(select(FieldItem)).all()
    crops = session.exec(select(CropItem)).all()
    ops = session.exec(select(OperationItem).where(OperationItem.season == season)).all()

    by_crop: dict[str, float] = {}
    for op in ops:
        c = next((x for x in crops if x.id == op.crop_id), None)
        key = c.name if c else "Не указана"
        by_crop[key] = by_crop.get(key, 0) + op.planned_area_ha

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "season": season,
            "fields_count": len(fields),
            "ops_count": len(ops),
            "planned_sum": round(sum(x.planned_area_ha for x in ops), 2),
            "completed_sum": round(sum(x.completed_area_ha for x in ops), 2),
            "by_crop": by_crop,
            "ops": ops,
            "fields": {f.id: f for f in fields},
            "crops": {c.id: c for c in crops},
        },
    )


@app.post("/seed")
def seed_data(session: Session = Depends(get_session)):
    if not session.exec(select(FieldItem)).first():
        session.add_all([
            FieldItem(name="Поле-1", group_name="Север", area_ha=210.5),
            FieldItem(name="Поле-2", group_name="Север", area_ha=148.7),
            FieldItem(name="Поле-3", group_name="Юг", area_ha=99.5),
        ])
    if not session.exec(select(CropItem)).first():
        session.add_all([CropItem(name="Пшеница яровая"), CropItem(name="Горох"), CropItem(name="Рапс яровой")])
    session.commit()
    return RedirectResponse(url="/dashboard", status_code=303)


@app.post("/operations")
def add_operation(
    season: int = Form(...),
    operation_type: str = Form(...),
    field_id: int = Form(...),
    crop_id: int = Form(...),
    planned_area_ha: float = Form(...),
    status: str = Form("planned"),
    session: Session = Depends(get_session),
):
    session.add(
        OperationItem(
            season=season,
            operation_type=operation_type,
            field_id=field_id,
            crop_id=crop_id,
            planned_area_ha=planned_area_ha,
            completed_area_ha=0,
            status=status,
            planned_date=date.today(),
        )
    )
    session.commit()
    return RedirectResponse(url=f"/dashboard?season={season}", status_code=303)


@app.get("/api/report/{season}")
def report(season: int, session: Session = Depends(get_session)):
    ops = session.exec(select(OperationItem).where(OperationItem.season == season)).all()
    return {
        "season": season,
        "operations": len(ops),
        "planned_area_ha": round(sum(x.planned_area_ha for x in ops), 2),
        "completed_area_ha": round(sum(x.completed_area_ha for x in ops), 2),
    }
