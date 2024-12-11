# plipinteractor

This repository is created to organize and analyze the outputs of **Protein-Ligand Interaction Profiler (PLIP)**.

## Sections

### Atom
This section contains scripts for atom - atom interactions organized by interaction types.

### Residue
This section contains scripts for residue - residue interactions organized by interaction types.

### Chain
This section contains scripts for chain - chain interactions organized by interaction types.

### Statistical Analysis
This section contains scripts for analyzing mean and standard deviation between simulations.

## Running Scripts

### Prerequisites
Ensure that you have installed the following libraries in your environment before running any script in this repository:

- Pandas
- Numpy
- Time

### Execution Instructions

#### For scripts in the **Atom/**, **Residue/**, **Chain/** folders:
1. Select the file according to the type of interaction you want to analyze.
2. Define the path to the output file.
3. Run the script from the file with the `.txt` extension to report results.

Example command:

    python atom_hydrophobic_interactions.py

### For scripts in the **Statistical Analysis/** folder:

1. Select the file according to the type of interaction you want to analyze.
   - The `stat_residue.py` and `stat_chain.py` files in this folder are available for all interaction types.
2. Define input files and output file.
3. Run the script.

Example command:

    python stat_chain.py
