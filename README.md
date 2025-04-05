# Opentrons Nanopore Library Preparation Protocol

## Protocol Overview

The **Opentrons Nanopore Library Preparation Protocol** automates key steps in the DNA library preparation process for Nanopore sequencing. This protocol is designed to enable a smooth, reproducible workflow for adapter ligation, bead-based cleanup, and elution, with an optional end-prep step. Automation reduces manual labor, minimizes variability, and ensures consistent results across experiments.

### Robot: Opentrons OT-2  
### API Version: 2.x  
### Modules: Magnetic Module GEN2 (for bead-based cleanup)  
### Pipettes:
- **Left Pipette**: P20 Single-Channel GEN2  
- **Right Pipette**: P300 Multi-Channel GEN2 (8-channel, 300 µL)  

### Required Pipettes:
- **Opentrons P300 8-Channel GEN2**: Used for high-throughput liquid handling, enabling parallel pipetting across 8 channels for efficient reagent handling.
- **Opentrons P20 Single-Channel GEN2**: Provides precise, single-channel pipetting capabilities for smaller volume transfers.

### Labware:
- **Armadillo 96-well PCR Plate (AB2396)**: This plate is ideal for its optimal bead separation properties and prevents bead pickup during supernatant aspiration.
- **Opentrons Tipracks (20 µL & 300 µL)**: These tipracks are used to ensure precise liquid transfers for both small and large volumes.
- **NEST or Custom Reservoirs**: Used to store reagents necessary for the protocol steps.

## Reagent Setup

For detailed information on reagents, including names, concentrations, suppliers, and volumes required for each step, please refer to the [reagents documentation](docs/reagents.md).

The reagent setup includes:
- **Reagent Names**: Full list of required reagents, such as adapter ligation kits, cleanup beads, and elution buffers.
- **Concentrations and Suppliers**: Exact reagent concentrations and their respective suppliers.
- **Volume Requirements**: Specifies required volumes for each step of the protocol.
- **Deck Slot Assignments**: Instructions for placing reagents, tip racks, and modules on the OT-2 deck for efficient protocol execution.
- **Mixing & Incubation Settings**: Details on temperature, time, and mixing speeds for each protocol step to ensure optimal performance.

## Deck Layout

The deck layout provides a visual guide for arranging the necessary labware on the Opentrons OT-2. Proper arrangement of labware ensures the efficient execution of the protocol.

For detailed deck setup, see the following image:

![Deck Layout](docs/images/deck_setup.png)

Key labware placements:
- **Tip Racks**: Located for both 20 µL and 300 µL pipette tips.
- **PCR Plate**: Armadillo 96-well plate for pipetting and magnetic bead handling.
- **Magnetic Module**: Positioned for optimal bead-based cleanup operations.
- **Reservoirs**: For storing reagents such as elution buffer and ligation mix.

## How to Run

Follow these steps to execute the Nanopore Library Preparation Protocol on the Opentrons OT-2:

1. **Open the Opentrons App**: Download and open the Opentrons App, then upload the `nanopore_library_prep.py` script.
2. **Import Custom Labware**: If not already in your library, import custom labware such as the Armadillo 96-well PCR Plate from the `custom_labware/` directory.
3. **Deck Setup**: Arrange reagents, tip racks, and the magnetic module according to the deck layout provided in the documentation.
4. **Calibrate Pipettes and Labware**: Ensure proper calibration of both the pipettes and labware to guarantee accurate liquid handling.
5. **Run the Protocol**: Click **Run** in the Opentrons App to begin. The App will display the current step and estimated time remaining for each phase.
6. **Post-Run**: Once the protocol completes, remove samples and assess the quality of the final product to confirm proper preparation.

For step-by-step guidance and troubleshooting, refer to the [usage documentation](docs/usage.md).

## Custom Labware

The **Armadillo 96-well PCR Plate** and other custom labware must be added to the Opentrons Labware Library for compatibility with the protocol.

### How to Add Custom Labware:
Instructions for loading custom labware definitions into the Opentrons Labware Library are available in the `custom_labware/README.md`.

Ensure that all required custom labware is loaded and calibrated before running the protocol.

## Protocol Notes

- **Bead Drying Time**: Bead drying time is a critical step after the cleanup phase. Adjust the drying time based on environmental conditions (e.g., humidity, temperature) to ensure optimal performance.
- **Mixing and Incubation Settings**: The protocol includes customizable mixing and incubation settings for each step (adapter ligation, cleanup, elution). These settings can be modified to suit specific reagent conditions or experimental preferences.
- **Reagent Compatibility**: This protocol has been validated with ONT ligation sequencing kits, specifically **LSK114**. If using different kits or reagents, validate the protocol conditions to ensure compatibility.

## Author

Created by **Naweed Yakubi**  
[GitHub Profile](https://github.com/YOUR_USERNAME)

This protocol was designed to support high-throughput, reproducible Nanopore library preparation for sequencing. Contributions and feedback are encouraged to improve the protocol.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

---

### Optional Sections for Future Updates:

- **Changelog**: Keep track of updates, changes, and improvements made to the protocol over time.
- **Validation Data**: Include data from validation experiments, such as Bioanalyzer results, to support protocol efficacy.
- **Performance Metrics**: Document key metrics such as yield, read length, and QC% from sequencing runs to assess the protocol's effectiveness.

