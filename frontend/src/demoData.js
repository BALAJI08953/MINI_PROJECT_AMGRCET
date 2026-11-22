// Synthetic fallback keeps the GitHub Pages dashboard useful without a hosted API.
export const demoPlants = [
  { id: 1, company: 'Sunrise Renewables (Demo)', name: 'Thar Sun Park', location: 'Jaisalmer', generation_type: 'Solar', capacity_mw: 520, current_generation_mw: 418, daily_generation_mwh: 1680, availability_pct: 96, status: 'Operational', renewable: true },
  { id: 2, company: 'Sunrise Renewables (Demo)', name: 'Desert Edge Solar', location: 'Barmer', generation_type: 'Solar', capacity_mw: 180, current_generation_mw: 142, daily_generation_mwh: 590, availability_pct: 93, status: 'Operational', renewable: true },
  { id: 3, company: 'Western Wind Collective (Demo)', name: 'Kutch Ridge Wind', location: 'Kutch', generation_type: 'Wind', capacity_mw: 310, current_generation_mw: 186, daily_generation_mwh: 710, availability_pct: 91, status: 'Operational', renewable: true },
  { id: 4, company: 'Riverbend Energy (Demo)', name: 'Satluj Hydro Station', location: 'Kinnaur', generation_type: 'Hydro', capacity_mw: 240, current_generation_mw: 198, daily_generation_mwh: 4520, availability_pct: 98, status: 'Operational', renewable: true },
  { id: 5, company: 'Central Thermal Works (Demo)', name: 'Narmada Thermal Unit', location: 'Singrauli', generation_type: 'Thermal', capacity_mw: 600, current_generation_mw: 512, daily_generation_mwh: 10900, availability_pct: 94, status: 'Operational', renewable: false },
  { id: 6, company: 'Coastal Atomic Power (Demo)', name: 'Konkan Demonstration Unit', location: 'Ratnagiri', generation_type: 'Nuclear', capacity_mw: 400, current_generation_mw: 376, daily_generation_mwh: 9000, availability_pct: 97, status: 'Operational', renewable: false },
];

export const demoUtilities = [
  { id: 1, name: 'MetroGrid Distribution (Demo)', region: 'Pune Metro', substation_count: 2, feeder_count: 4, transformer_count: 8, demand_mw: 680, received_mw: 720, supplied_mw: 662, losses_mw: 58, losses_pct: 8.1, active_outages: 3, status: 'Operational' },
  { id: 2, name: 'North Plains Electric (Demo)', region: 'Punjab North', substation_count: 2, feeder_count: 4, transformer_count: 8, demand_mw: 540, received_mw: 575, supplied_mw: 521, losses_mw: 54, losses_pct: 9.4, active_outages: 2, status: 'Operational' },
  { id: 3, name: 'Coastal Light & Power (Demo)', region: 'Konkan Coast', substation_count: 2, feeder_count: 4, transformer_count: 8, demand_mw: 420, received_mw: 448, supplied_mw: 405, losses_mw: 43, losses_pct: 9.6, active_outages: 4, status: 'Operational' },
];

export const demoOverview = { installed_capacity_mw: 2250, generation_mw: 1832, demand_mw: 1640, supplied_mw: 1588, losses_mw: 155, operational_plants: 6, generation_companies: 5, power_companies: 3 };
