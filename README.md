# 🧬 Nanopore Library Preparation Protocol for Opentrons OT-2
This repository contains an automated protocol for preparing DNA libraries for Nanopore sequencing using the Opentrons OT-2 liquid-handling robot. The protocol covers end-repair, adapter ligation and magnetic bead-based cleanup steps, and is compatible with Flongle and MinION workflows.


## ⚙️ Protocol Details

- **Robot**: Opentrons OT-2
- **API Version**: 2.x
- **Modules**: Magnetic Module GEN2
- **Pipettes**:
  - Left: P20 Single-Channel GEN2
  - Right: P300 Multi-Channel GEN2
- **Labware**:
  - Armadillo 96-well PCR Plate (AB2396)
  - Opentrons Tiprack 20 µL & 300 µL
  - NEST or custom reservoirs
- **Steps Included**:
  - Adapter ligation
  - Bead-based cleanup
  - Elution
  - Optional: end-prep

## 🧪 Reagent Setup

Refer to [`docs/reagents.md`](docs/reagents.md) for full details on:
- Reagent names, concentrations, and suppliers
- Volumes required for each step
- Deck slot assignments
- Mixing & incubation settings

## 🖼️ Deck Layout

![Deck Layout](docs/images/deck_setup.png)

## 🚀 How to Run

1. Open the [Opentrons App](https://opentrons.com/ot-app) and upload `nanopore_library_prep.py`.
2. Import any custom labware from `custom_labware/` if not already in your labware library.
3. Place reagents, tip racks, and modules as specified.
4. Calibrate labware and pipettes.
5. Click **Run** and monitor progress.

See [`docs/usage.md`](docs/usage.md) for step-by-step instructions.

## 📂 Custom Labware

Custom labware (e.g., Armadillo 96 PCR Plate) must be added to your Opentrons Labware Library. See the [`custom_labware/`](protocol/custom_labware) folder.

## 📌 Notes

- Bead drying time is critical; adjust as needed for your conditions.
- Includes configurable variables for elution volume, mixing speed, and incubation times.
- Designed for compatibility with ONT ligation sequencing kits (e.g., LSK114).

## 🧑‍🔬 Author

Created by **Naweed Yakubi**  
[GitHub Profile](https://github.com/YOUR_USERNAME)

## 📜 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

### 🛠️ Optional Sections You Can Add Later:

- ✅ **Changelog**
- 👩‍🔬 **Validation Data** (e.g., Bioanalyzer results)
- 📈 **Performance Metrics** (e.g., yield, read length, QC%)

---

Want me to turn this into a complete file with your name inserted and deck image placeholder?
