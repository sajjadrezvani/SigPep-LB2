**vonHeijne steps tree**

1. Prepare the Dataset
   │
   ├── Positive proteins → proteins with Signal Peptide
   └── Negative proteins → proteins without Signal Peptide
   │
   ▼
2. Split the Dataset into 5 Folds
   │
   ├── 3 folds → Training
   ├── 1 fold  → Validation
   └── 1 fold  → Testing
   │
   ▼
3. Extract Cleavage-Site Contexts from Positive Training Proteins
   │
   └── Take positions -13 to +2
       → 15 amino acids per positive protein
   │
   ▼
4. Build the Count Matrix
   │
   └── 20 amino acids × 15 positions
   │
   ▼
5. Add Pseudocounts
   │
   └── Initialize every cell with 1
   │
   ▼
6. Compute the PSPM
   │
   └── Convert counts into probabilities
       Count / (N + 20)
   │
   ▼
7. Apply the SwissProt Background Distribution
   │
   └── Compare motif probabilities with normal amino-acid frequencies
   │
   ▼
8. Compute the PSWM
   │
   └── Weight = log(PSPM / Background)
   │
   ▼
9. Score Validation Proteins
   │
   ├── Take the first 90 N-terminal residues
   ├── Slide a 15-residue window
   ├── Score every window
   └── Keep the maximum score for each protein
   │
   ▼
10. Select the Best Threshold
    │
    ├── Use validation labels
    ├── Compute Precision-Recall values
    └── Choose the threshold with the best F1-score
    │
    ▼
11. Score the Testing Proteins
    │
    └── Use the same PSWM
    │
    ▼
12. Classify the Testing Proteins
    │
    ├── Score ≥ threshold → SP
    └── Score < threshold → NO_SP
    │
    ▼
13. Evaluate the Test Results
    │
    └── Compare predictions with true labels
    │
    ▼
14. Repeat for All 5 Cross-Validation Runs
    │
    ▼
15. Combine the Results
    │
    └── Compute the final cross-validation performance
