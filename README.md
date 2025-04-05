# Opentrons Nanopore Library Preparation Protocol

## Protocol Overview

The **Opentrons Nanopore Library Preparation Protocol** automates critical steps in DNA library preparation for Nanopore sequencing. This protocol is optimized for adapter ligation, bead-based cleanup, and elution, with an optional end-prep step. Automating these processes reduces manual labor, variability, and ensures consistency and reproducibility across experiments.

---

### Requirements

Before running the protocol, please ensure the following equipment and materials are available:

#### 1. **Robot and Modules:**
- **Opentrons OT-2**: The primary robot for automating pipetting and liquid handling.
- **Magnetic Module GEN2**: Required for bead-based cleanup steps. A 3D raiser mount has been added for better magnet engagement and proper spacing.

#### 2. **Pipettes:**
- **(Left Mount) Opentrons P300 8-Channel GEN2**:  
  - For high-throughput liquid handling with 8 channels, essential for transferring larger volumes across multiple wells.
- **(Right Mount) Opentrons P20 Single-Channel GEN2**:  
  - For precise, single-channel pipetting, especially for smaller volume transfers like ligation.

#### 3. **Labware:**
- **Abgene™ 96-Well 0.8mL Polypropylene DeepWell™ Sample Processing & Storage Plate**  
  - Ideal for performing library preparation steps, with unique properties to prevent bead pickup during supernatant aspiration.
- **Opentrons Tipracks (20 µL & 300 µL)**:  
  - Required for storing pipette tips used with both the P20 and P300 pipettes.  
  - For 8 input samples: Use **2 x 300 µL Tipracks**.  
  - For 1-7 input samples: **1 x 20/300 µL Tiprack** suffices.

#### 4. **Reagents:**
Refer to the official Nanopore Library Prep Sequencing Kits (SQK-LSK114) for specific reagents needed for the protocol. **Stock plates** for Armadillo are created through another custom protocol, allowing long-term storage and easy grab-and-go access. The reagents required for each DNA sample are:

- **Ampure Beads**: 100 µL
- **80% Ethanol**: 500 µL
- **Nuclease-Free Water**: 61 µL
- **Ligation Buffer**: 25 µL
- **Ligase**: 10 µL
- **Ligation Adapter**: 5 µL
- **Short Fragment Buffer**: 450 µL
- **Elution Buffer**: 15 µL

*(Note: An extra 2 µL dead volume is recommended for added accuracy.)*

#### 5. **Software:**
- **Opentrons App (Version 2.x or higher)**:  
  - Essential for uploading and running the protocol. Ensure the app is installed and configured with custom labware on your computer.

#### 6. **Custom Labware:**
- **Abgene™ 96-Well 0.8mL Polypropylene DeepWell™ Sample Processing & Storage Plate**  
  - This custom labware definition must be added to the Opentrons Labware Library.  
  - If not already available, import the labware definitions from the `custom_labware/` directory.

---

## Deck Layout

Proper deck layout is essential for smooth execution. The labware should be arranged as follows:

- **Tip Racks (20 µL & 300 µL)**:  
  - Place the tip racks in the designated positions for the P20 and P300 pipettes (as shown in the Opentrons App).
- **Abgene™ 96-Well Plate**:  
  - Place the plate on the magnetic module deck for pipetting and magnetic bead handling.
- **Magnetic Module GEN2**:  
  - Position the magnetic module in the appropriate slot to handle bead separation.  
  - Ensure the 3D printed spacer is placed correctly on top of the magnetic module for optimal performance.

Refer to the [deck setup image](docs/images/deck_setup.png) for a detailed visual guide.

---

## How to Run

1. **Open the Opentrons App**:  
   - Download and open the Opentrons App, then upload the `nanopore_library_prep.py` script.
   
2. **Import Custom Labware**:  
   - If the required custom labware (e.g., Abgene™ 96-Well PCR Plate) is not in your library, import it from the `custom_labware/` directory.

3. **Prepare the Deck**:  
   - Arrange the reagents, tip racks, and magnetic module according to the deck layout provided in the App.
   - Ensure the P300 and P20 pipettes are installed and calibrated correctly.

4. **Calibrate Labware**:  
   - Calibrate the pipettes and labware to ensure accurate liquid handling and proper positioning.

5. **Run the Protocol**:  
   - Click **Run** in the Opentrons App to begin the library preparation process. The App will guide you through each step and provide updates on the protocol’s progress.

6. **Post-Run**:  
   - After the protocol finishes, retrieve the samples and assess the quality of the final library preparation (ligated and bead-cleaned). The library should now be ready to add sequencing beads and proceed to sequencing.

---

## Protocol Notes

- **Bead Drying Time**: The drying time for beads is crucial for the cleanup step. Adjust the drying time based on your lab conditions (e.g., temperature, humidity).
  
- **Customization**:  
  - Parameters such as elution volume, mixing speed, and incubation time can be customized for specific experimental needs or reagent conditions.
  
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

