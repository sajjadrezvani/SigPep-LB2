# 🧬 Signal Peptide Prediction

## Laboratory of Bioinformatics II — Module 2
### Group 12: Sajjad - Sara - Roxana 
A computational study of **signal peptide prediction in eukaryotic proteins**, combining classical bioinformatics methods with machine-learning approaches.

---
## 📌 Progress update

### setup
- setup VM, VPN, and github 
- Data collection:

### data collection
> Positive: 2972 retrieved → 2961 final
> 
> Negative: 20975 retrieved → 20975 final
## Data preparation
### Reduce redundancy & build splits
### 1.Reduce Redundancy
To prevent homology bias and avoid data leakage between partitions, sequence redundancy reduction was performed independently on both the positive and negative datasets using **MMseqs2**.

* **Clustering Method**: Connected-component clustering (`--cluster-mode 1`) executed via an explicit pairwise search and clustering pipeline (`mmseqs createdb` → `search` → `clust`).
* **Thresholds**:
  * Minimum sequence identity: 30%
  * Minimum bidirectional coverage: 40%
* **Representative Selection**: For every connected component (subgraph of homologous proteins meeting the similarity thresholds), the sequence with the highest vertex degree (most alignment connections within the cluster) was chosen as the cluster representative, with ties broken by sequence length.
* **Outputs**:
  * Clustered mapping tables (`pos_clustered_cluster.tsv`, `neg_clustered_cluster.tsv`) tracking cluster membership.
  * Non-redundant representative sequence databases (`pos_clustered_rep_seq.fasta`, `neg_clustered_rep_seq.fasta`) used for downstream train/benchmark partitioning and 5-fold cross-validation.


Following sequence redundancy reduction, representative sequences were split into training and benchmarking subsets to ensure unbiased model training and validation.

### 2. Train / Benchmark Split (80/20)
* **Independent Partitioning**: The 80/20 partition was performed separately on the positive and negative representative sets to preserve class distribution across subsets.
* **Benchmarking Set (20%)**: Held out completely as an independent, untouched evaluation set for final performance assessment.
* **Training Set (80%)**: Reserved strictly for model parameter estimation, hyperparameter optimization, and internal validation.
* **Reproducibility**: Datasets were shuffled with a fixed random seed (`seed=42`) prior to partitioning.

### 3. 5-Fold Cross-Validation
* **Internal Folds**: The 80% training pool was divided into 5 balanced folds (folds `0` through `4`).
* **Preserving Class Ratio**: Fold assignment was conducted independently across positive and negative training records using round-robin modulo indexing (`idx % 5`), ensuring each fold maintained the overarching class balance (~1:8.26 positive-to-negative ratio).
* **Fold Tracking**: Every protein's subset assignment was explicitly recorded in a `CV_Fold` column across output tables (`positive_train_5fold.tsv`, `negative_train_5fold.tsv`, and `training_5fold_cv_master.tsv`) to ensure identical, reproducible cross-validation partitions across all downstream models.

---

## 🗂️ Repository Structure

```text
LB2/
│
├── README.md
├── .gitignore
│
├── src/
│   └── collect_uniprot_data.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── results/
│
└── docs/
'''

---

## 📌 Project Overview

Signal peptides (SPs) are short N-terminal amino-acid sequences that direct newly synthesized proteins into the **secretory pathway**, enabling their transport through the endoplasmic reticulum (ER), Golgi apparatus, and ultimately to destinations such as the cell membrane or extracellular space.

Predicting signal peptides from protein sequences is an important problem in **protein function prediction, subcellular localization, and genome/proteome annotation**.

This project investigates different computational approaches for identifying signal peptides and their cleavage sites, starting from classical statistical methods and progressing toward machine-learning approaches.

> **Main question:**  
> Can we reliably distinguish proteins containing signal peptides from proteins without signal peptides using sequence information?

---

## 🎯 Objectives

- Collect and curate a high-quality **eukaryotic protein dataset** from UniProtKB.
- Construct positive and negative datasets for signal peptide prediction.
- Analyze sequence and dataset characteristics.
- Extract informative sequence features.
- Implement the **von Heijne weight-matrix approach** for signal peptide/cleavage-site prediction.
- Implement a **feature-based Support Vector Machine (SVM)** approach.
- Evaluate the models using cross-validation and an independent/blind test set.
- Compare the approaches and analyze their strengths and limitations.
- Discuss more recent approaches to signal peptide prediction.

The project therefore covers both:
1. **Signal peptide detection** — does the protein contain a signal peptide?
2. **Cleavage-site prediction** — where is the signal peptide cleaved?

---

## 🧪 Dataset

Protein sequences are collected from **UniProtKB** and restricted to **eukaryotic proteins**.

### Positive Dataset

Positive examples satisfy the project criteria, including:

- Reviewed UniProt entries
- No protein fragments
- Experimental evidence for a signal peptide
- Protein-level evidence for protein existence
- Protein length ≥ 40 amino acids
- Signal peptide length > 13 amino acids
- Known signal peptide cleavage site

### Negative Dataset

Negative examples satisfy:

- Reviewed UniProt entries
- No protein fragments
- Protein-level evidence for protein existence
- Protein length ≥ 40 amino acids
- No annotated signal peptide at any evidence level
- Experimental localization to selected non-secretory compartments

The datasets will be stored in both **TSV** and **FASTA** formats.

---
