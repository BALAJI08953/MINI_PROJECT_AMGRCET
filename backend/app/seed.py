from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import GenerationCompany, Plant, Utility, Substation, Feeder, Transformer

STAMP = datetime.now(timezone.utc).isoformat(timespec="minutes")


def seed(db: Session):
    if db.scalar(select(GenerationCompany.id).limit(1)):
        return
    specs = [
        ("Sunrise Renewables (Demo)", "Rajasthan", [("Thar Sun Park", "Jaisalmer", "Solar", 520, 418, 1680, 96, True), ("Desert Edge Solar", "Barmer", "Solar", 180, 142, 590, 93, True)]),
        ("Western Wind Collective (Demo)", "Gujarat", [("Kutch Ridge Wind", "Kutch", "Wind", 310, 186, 710, 91, True)]),
        ("Riverbend Energy (Demo)", "Himachal Pradesh", [("Satluj Hydro Station", "Kinnaur", "Hydro", 240, 198, 4520, 98, True)]),
        ("Central Thermal Works (Demo)", "Madhya Pradesh", [("Narmada Thermal Unit", "Singrauli", "Thermal", 600, 512, 10900, 94, False)]),
        ("Coastal Atomic Power (Demo)", "Maharashtra", [("Konkan Demonstration Unit", "Ratnagiri", "Nuclear", 400, 376, 9000, 97, False)]),
    ]
    for company_name, location, plants in specs:
        company = GenerationCompany(name=company_name, location=location)
        for name, place, kind, cap, current, daily, avail, renewable in plants:
            company.plants.append(Plant(name=name, location=place, generation_type=kind, capacity_mw=cap,
                current_generation_mw=current, daily_generation_mwh=daily, availability_pct=avail,
                status="Operational", renewable=renewable, reading_at=STAMP))
        db.add(company)
    utility_specs = [
        ("MetroGrid Distribution (Demo)", "Pune Metro", 680, 720, 662, 58, 8.1, 3),
        ("North Plains Electric (Demo)", "Punjab North", 540, 575, 521, 54, 9.4, 2),
        ("Coastal Light & Power (Demo)", "Konkan Coast", 420, 448, 405, 43, 9.6, 4),
    ]
    for ui, (name, region, demand, received, supplied, losses, pct, outages) in enumerate(utility_specs, 1):
        utility = Utility(name=name, region=region, demand_mw=demand, received_mw=received,
                          supplied_mw=supplied, losses_mw=losses, losses_pct=pct,
                          active_outages=outages, status="Operational", reading_at=STAMP)
        for si in range(1, 3):
            sub = Substation(name=f"{region.split()[0]} Substation {si}", location=f"{region} Zone {si}")
            for fi in range(1, 3):
                feeder = Feeder(name=f"{region.split()[0]} F-{si}{fi}", status="Operational")
                for ti in range(1, 3):
                    feeder.transformers.append(Transformer(name=f"{region.split()[0]} DT-{si}{fi}{ti}", capacity_kva=500 if ti == 1 else 1000, status="Operational"))
                sub.feeders.append(feeder)
            utility.substations.append(sub)
        db.add(utility)
    db.commit()
