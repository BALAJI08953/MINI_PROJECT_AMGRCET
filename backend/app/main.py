from contextlib import asynccontextmanager
import numpy as np
import pandas as pd
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from .database import Base, engine, get_db
from .models import GenerationCompany, Plant, Utility, Substation, Feeder, Transformer
from .seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        seed(db)
    yield


app = FastAPI(title="GridGuard AI Energy Data API", version="1.0.0", description="Stage 1 synthetic energy data foundation. All seeded figures are demonstration data.", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_methods=["*"], allow_headers=["*"])


@app.get("/api/health", tags=["system"])
def health():
    return {"status": "ok", "data_label": "Synthetic demonstration data"}


@app.get("/api/generation/companies", tags=["generation"])
def generation_companies(db: Session = Depends(get_db)):
    rows = db.scalars(select(GenerationCompany).options(joinedload(GenerationCompany.plants))).unique().all()
    return [{"id": c.id, "name": c.name, "location": c.location, "plant_count": len(c.plants)} for c in rows]


@app.get("/api/generation/plants", tags=["generation"])
def generation_plants(db: Session = Depends(get_db)):
    rows = db.scalars(select(Plant).options(joinedload(Plant.company))).all()
    return [{"id": p.id, "company": p.company.name, "company_id": p.company_id, "name": p.name, "location": p.location,
             "generation_type": p.generation_type, "capacity_mw": p.capacity_mw, "current_generation_mw": p.current_generation_mw,
             "daily_generation_mwh": p.daily_generation_mwh, "availability_pct": p.availability_pct, "status": p.status,
             "renewable": p.renewable, "reading_at": p.reading_at} for p in rows]


@app.get("/api/utilities", tags=["distribution"])
def utilities(db: Session = Depends(get_db)):
    rows = db.scalars(select(Utility).options(joinedload(Utility.substations).joinedload(Substation.feeders).joinedload(Feeder.transformers))).unique().all()
    output = []
    for u in rows:
        feeders = [f for s in u.substations for f in s.feeders]
        output.append({"id": u.id, "name": u.name, "region": u.region, "substation_count": len(u.substations),
            "feeder_count": len(feeders), "transformer_count": sum(len(f.transformers) for f in feeders),
            "demand_mw": u.demand_mw, "received_mw": u.received_mw, "supplied_mw": u.supplied_mw,
            "losses_mw": u.losses_mw, "losses_pct": u.losses_pct, "active_outages": u.active_outages,
            "status": u.status, "reading_at": u.reading_at})
    return output


@app.get("/api/substations", tags=["distribution"])
def substations(db: Session = Depends(get_db)):
    rows = db.scalars(select(Substation).options(joinedload(Substation.utility))).all()
    return [{"id": s.id, "name": s.name, "location": s.location, "utility": s.utility.name, "utility_id": s.utility_id} for s in rows]


@app.get("/api/feeders", tags=["distribution"])
def feeders(db: Session = Depends(get_db)):
    rows = db.scalars(select(Feeder).options(joinedload(Feeder.substation).joinedload(Substation.utility))).all()
    return [{"id": f.id, "name": f.name, "status": f.status, "substation": f.substation.name, "utility": f.substation.utility.name} for f in rows]


@app.get("/api/transformers", tags=["distribution"])
def transformers(db: Session = Depends(get_db)):
    rows = db.scalars(select(Transformer).options(joinedload(Transformer.feeder).joinedload(Feeder.substation).joinedload(Substation.utility))).all()
    return [{"id": t.id, "name": t.name, "capacity_kva": t.capacity_kva, "status": t.status, "feeder": t.feeder.name, "utility": t.feeder.substation.utility.name} for t in rows]


@app.get("/api/overview", tags=["overview"])
def overview(db: Session = Depends(get_db)):
    plants = db.scalars(select(Plant)).all()
    utilities_rows = db.scalars(select(Utility)).all()
    if not plants or not utilities_rows:
        return {"installed_capacity_mw": 0, "generation_mw": 0, "demand_mw": 0, "supplied_mw": 0, "losses_mw": 0, "operational_plants": 0, "generation_companies": 0, "power_companies": 0}
    p = pd.DataFrame([{"capacity": x.capacity_mw, "generation": x.current_generation_mw, "status": x.status} for x in plants])
    u = pd.DataFrame([{"demand": x.demand_mw, "supplied": x.supplied_mw, "losses": x.losses_mw} for x in utilities_rows])
    return {"installed_capacity_mw": round(float(np.sum(p.capacity)), 1), "generation_mw": round(float(np.sum(p.generation)), 1),
        "demand_mw": round(float(np.sum(u.demand)), 1), "supplied_mw": round(float(np.sum(u.supplied)), 1), "losses_mw": round(float(np.sum(u.losses)), 1),
        "operational_plants": int((p.status == "Operational").sum()), "generation_companies": db.query(GenerationCompany).count(), "power_companies": len(utilities_rows)}
