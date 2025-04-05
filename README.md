# Opentrons Nanopore Library Preparation Protocol

## Protocol Overview

The **Opentrons Nanopore Library Preparation Protocol** automates critical steps in DNA library preparation for Nanopore sequencing. This protocol is optimized for adapter ligation, bead-based cleanup, and elution, with an optional end-prep step. The automation of these processes reduces manual labor and variability, ensuring consistency and reproducibility across experiments.

### Requirements

Before running the protocol, please ensure the following equipment and materials are available:

#### 1. **Robot and Modules:**
- **Opentrons OT-2**: The primary robot for automating pipetting and liquid handling.
- **Magnetic Module GEN2**: Required for bead-based cleanup steps.

#### 2. **Pipettes:**
- **Opentrons P300 8-Channel GEN2**:  
  - Used for high-throughput liquid handling with 8 channels for parallel pipetting, essential for transferring larger volumes across multiple wells.
- **Opentrons P20 Single-Channel GEN2**:  
  - Provides precise, single-channel pipetting for smaller volume transfers, especially for critical steps like ligation.

#### 3. **Labware:**
- **Armadillo 96-well PCR Plate (AB2396)**:  
  - Required for performing the library preparation steps. This PCR plate has unique properties to prevent bead pickup during supernatant aspiration, making it ideal for this protocol.
- **Opentrons Tipracks (20 µL & 300 µL)**:  
  - For storing the pipette tips used for liquid handling with both the P20 and P300 pipettes.
- **NEST or Custom Reservoirs**:  
  - To store reagents (e.g., ligation mix, beads, buffers). Ensure the reservoirs are properly labeled and filled with the required reagents.

#### 4. **Reagents:**
Refer to the [reagents documentation](docs/reagents.md) for specific reagents needed for the protocol. You will need:
- **Ligation reagents** (for adapter ligation)
- **Beads** (for cleanup steps)
- **Elution buffer** (for the elution step)
- **Optional**: End-prep reagents (if using an optional end-prep step)

#### 5. **Software:**
- **Opentrons App** (Version 2.x or higher):  
  - This is the interface used to upload and run the protocol. It is essential to have the Opentrons App installed and configured on your computer.

#### 6. **Custom Labware:**
- **Armadillo 96-well PCR Plate** must be added to the Opentrons Labware Library for compatibility with the protocol. If you do not already have it in your library, you will need to import the custom labware definitions from the `custom_labware/` directory.

For more details on how to import custom labware, refer to the [custom labware documentation](protocol/custom_labware/README.md).

---

## Deck Layout

A proper deck layout is essential for the protocol to run smoothly. The labware should be arranged as follows:

- **Tip Racks** (20 µL & 300 µL):  
  - Ensure that the tip racks are placed in the designated positions for the P20 and P300 pipettes.
- **Armadillo 96-well PCR Plate**:  
  - Located on the deck for pipetting and magnetic bead handling.
- **Magnetic Module GEN2**:  
  - Place the magnetic module in the correct slot to handle bead separation during the cleanup step.
- **Reservoirs**:  
  - Store reagents such as ligation mix, beads, and buffers in the reservoirs, following the deck layout provided.

Refer to the [deck setup image](docs/images/deck_setup.png) for more detailed visual guidance.

---

## How to Run

Follow the steps below to execute the protocol:

1. **Open the Opentrons App**:  
   Download and open the Opentrons App, then upload the `nanopore_library_prep.py` script.

2. **Import Custom Labware**:  
   If you do not have the required custom labware (e.g., Armadillo 96-well PCR Plate) already in your library, import it from the `custom_labware/` directory.

3. **Prepare the Deck**:  
   - Arrange reagents, tip racks, and the magnetic module according to the specified deck layout.
   - Ensure the pipettes (P300 and P20) are installed and calibrated correctly.
   
4. **Calibrate Labware**:  
   Perform calibration of the pipettes and labware to ensure accurate liquid handling.

5. **Run the Protocol**:  
   Click **Run** in the Opentrons App to begin the library preparation process. The App will guide you through each step, providing estimated time remaining and current protocol status.

6. **Post-Run**:  
   After the protocol finishes, retrieve the samples and assess the quality of the final product to confirm proper preparation. The resulting library should be ready for sequencing.

---

## Protocol Notes

- **Bead Drying Time**: Bead drying time is critical for the cleanup step. Adjust the drying time according to your lab conditions (e.g., humidity, temperature).
  
- **Customization**:  
  - The protocol includes adjustable parameters such as elution volume, mixing speed, and incubation time. These can be modified to fit specific experimental needs or reagent conditions.
  
- **Reagent Compatibility**: This protocol is validated for use with **ONT ligation sequencing kits** (e.g., LSK114). If using different reagents, test and validate the protocol conditions to ensure compatibility.

---

## Author

**Naweed Yakubi**  
[GitHub Profile](https://github.com/YOUR_USERNAME)

This protocol was developed to support automated, high-throughput Nanopore library preparation. For contributions or issues, please reach out via GitHub.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

---

### Optional Sections for Future Updates:

- **Changelog**: Track protocol updates and improvements.
- **Validation Data**: Include results from validation experiments (e.g., Bioanalyzer data).
- **Performance Metrics**: Document key sequencing metrics such as yield, read length, and QC%.

