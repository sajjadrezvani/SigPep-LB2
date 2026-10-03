# Signal Peptide Prediction: Comparative Review of Five Key Papers

> **Scope:** DeepSig (2018), SignalP 6.0 (2022), TSignal (2023), SaSPNet
> / StrucAware (2026), and Signal-3L 4.0 (2026).
>
> **Main focus:** What problem remains difficult after these advances,
> especially **cleavage-site prediction and minority/low-resource SP
> classes**?

------------------------------------------------------------------------

## 1. Executive conclusion

After reviewing the five uploaded papers, the strongest conclusion is
**not** simply that Sec/SPI and Tat/SPI are the main bottlenecks.

A better statement is:

> **The main remaining difficulty is precise cleavage-site localization
> and robust generalization to underrepresented/unusual signal-peptide
> classes. Which class is hardest depends on organism, dataset,
> evaluation protocol, and whether prediction is conditioned on correct
> SP-type classification.**

Three observations support this:

1.  **SignalP 6.0** substantially improved the previously
    underrepresented SP types, especially **Sec/SPIII and Tat/SPII**,
    showing that low-data classes were a major limitation of earlier
    predictors.
2.  **TSignal** improved overall cleavage-site F1 over SignalP 6.0, but
    cleavage remained substantially harder than SP detection.
3.  **SaSPNet and Signal-3L 4.0** explicitly target
    minority/low-resource settings and show that the difficult tail of
    the SP-class distribution is still a meaningful problem.

A second important conclusion is:

> **Structure is useful, but mainly as complementary information.
> Sequence/PLM representations remain the dominant source of
> information.**

Signal-3L 4.0 provides particularly clean evidence: removing the
structural branch reduces performance, but removing the sequence branch
hurts more.

------------------------------------------------------------------------

# 2. The five papers at a glance

  -------------------------------------------------------------------------------------------------------
  Paper                       Year Main idea              Main innovation           Main remaining issue
  -------------- ----------------- ---------------------- ------------------------- ---------------------
  **DeepSig**                 2018 Deep CNN + structured  Learns N-terminal         Precise cleavage
                                   cleavage prediction    patterns and explicitly   prediction; limited
                                                          handles TM confusion      SP-type modeling

  **SignalP                   2022 Protein LM + CRF       Protein language model    Rare classes and
  6.0**                                                   captures                  cleavage localization
                                                          evolutionary/contextual   
                                                          information and supports  
                                                          all five SP types         

  **TSignal**                 2023 ProtBERT + Transformer Removes hard-coded SP     Cleavage remains
                                   sequence-to-sequence   structure and learns      harder than SP
                                                          label sequences directly  detection

  **SaSPNet /                 2026 Sequence + PLM +       Explicitly targets        Complexity,
  StrucAware**                     predicted 3D           minority SP classes using predicted-structure
                                   structure + GCN        structural information    dependence, remaining
                                                                                    rare-class errors

  **Signal-3L                 2026 ESM2 + sequence        Better multimodal fusion  Exact cleavage
  4.0**                            branch + structure     and explicit              remains difficult,
                                   representation +       low-resource/imbalance    especially in some
                                   co-attention + CRF +   treatment                 classes
                                   imbalance-aware loss                             
  -------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 3. Biological problem

A classical signal peptide usually contains:

``` text
N-region       H-region             C-region
positive       hydrophobic          cleavage context
charges        core                 ↓
   |              |                |
M K R A A L L L L L L A A S A | E P V ...
```

The fundamental prediction problem has two related parts:

### Task A --- SP detection / classification

> Does the protein have a signal peptide, and which SP type is it?

### Task B --- cleavage-site prediction

> If an SP exists, exactly where is it cleaved?

These are **not equally difficult**.

Modern models can achieve very strong SP classification while still
making more errors in the exact cleavage position.

------------------------------------------------------------------------

# 4. The central distinction: classification vs cleavage

  -----------------------------------------------------------------------
  Task                    Typical output          Why difficult?
  ----------------------- ----------------------- -----------------------
  SP presence             SP / no-SP              SP hydrophobic region
                                                  resembles N-terminal TM
                                                  helix

  SP type                 Sec/SPI, Sec/SPII,      Some classes have very
                          Tat/SPI, etc.           few training examples

  Cleavage site           Exact residue boundary  No universal cleavage
                                                  motif; nearby positions
                                                  can be biologically
                                                  plausible

  Cleavage with tolerance Correct within ±1, ±2,  Easier and often more
                          ±3 residues             biologically realistic
  -----------------------------------------------------------------------

The Bioinformatics II lecture material also emphasizes cleavage-site
variability and the difficulty of distinguishing SPs from N-terminal
transmembrane helices.

------------------------------------------------------------------------

# 5. Paper 1 --- DeepSig (2018)

## Core question

Can deep learning improve signal-peptide detection and cleavage-site
prediction while reducing confusion between signal peptides and
N-terminal transmembrane regions?

## Core idea

DeepSig uses:

``` text
Protein sequence
      ↓
Deep CNN
      ↓
SP / TM / other
      ↓
if SP detected
      ↓
structured sequence labeling
      ↓
cleavage site
```

The first stage uses a deep convolutional neural network on the
N-terminus.

The second stage treats cleavage-site prediction as a
**sequence-labeling problem** and uses a probabilistic structured model.
Deep Taylor Decomposition provides a relevance profile that is added as
information for cleavage prediction.

### Important innovation

DeepSig explicitly treats **N-terminal transmembrane regions as a hard
negative class**.

That was important because:

> hydrophobic SP core ≈ hydrophobic TM helix

but biologically:

``` text
SP:
hydrophobic region → CLEAVED → mature protein

TM:
hydrophobic region → RETAINED → membrane anchor
```

------------------------------------------------------------------------

## DeepSig: independent SPDS17 benchmark

  Organism               MCC   TM false-positive rate   Cleavage F1
  --------------- ---------- ------------------------ -------------
  Eukaryotes        **0.86**                 **2.5%**      **0.72**
  Gram-positive         0.54                     0.0%      **0.82**
  Gram-negative     **0.95**                     2.6%      **0.36**

Source: DeepSig Table 3, independent SPDS17 dataset.

### Cleavage-site plot

``` text
DeepSig cleavage F1 — SPDS17

Eukaryotes       ██████████████      0.72
Gram-positive    ████████████████    0.82
Gram-negative    ███████             0.36
```

The striking point is that **good SP detection does not guarantee good
cleavage prediction**.

Gram-negative bacteria have MCC = 0.95 but cleavage F1 = 0.36.

------------------------------------------------------------------------

## DeepSig cross-validation

  Organism          DeepSig MCC   DeepSig cleavage F1
  --------------- ------------- ---------------------
  Eukaryotes              0.910                 0.733
  Gram-positive           0.878                 0.723
  Gram-negative           0.900                 0.862

DeepSig reports a roughly **2--4 percentage-point cleavage improvement**
over the corresponding SignalP results in this benchmark, except for
Gram-positive bacteria.

------------------------------------------------------------------------

## Important limitation for our five-paper comparison

DeepSig does **not** report the later five-class breakdown:

-   Sec/SPI
-   Sec/SPII
-   Sec/SPIII
-   Tat/SPI
-   Tat/SPII

Instead, it reports performance by **organism group**.

Therefore, it is not valid to claim from DeepSig that "Tat/SPI was its
weakest class."

------------------------------------------------------------------------

# 6. Paper 2 --- SignalP 6.0 (2022)

## Core question

Can a protein language model provide better representations for
signal-peptide prediction, particularly for **rare SP types and
distantly related sequences**?

## Core architecture

``` text
Protein sequence
      ↓
Protein Language Model
(BERT / ProtBERT-style)
      ↓
contextual residue representations
      ↓
CRF
      ↓
SP region + SP type + cleavage
```

The major conceptual shift was:

> Instead of learning mainly from manually designed local sequence
> patterns, use a protein language model that has already learned broad
> protein sequence context.

------------------------------------------------------------------------

## Five SP types

SignalP 6.0 models:

1.  Sec/SPI
2.  Sec/SPII
3.  Sec/SPIII
4.  Tat/SPI
5.  Tat/SPII

It also distinguishes non-SP sequences.

------------------------------------------------------------------------

## Why SignalP 6.0 mattered

The paper explicitly hypothesized that protein language models would
help with:

-   limited-data SP types
-   distant sequences
-   unknown species

The paper reports particularly strong improvements for the
**underrepresented Sec/SPIII and Tat/SPII classes**.

This is important for our question:

> **The hardest class is not necessarily the most common class.**

------------------------------------------------------------------------

## SignalP 6.0 benchmark metrics

The later TSignal paper reports the following SignalP 6.0 benchmark
averages:

  Metric                   SignalP 6.0
  ---------------------- -------------
  MCC1                      **0.8532**
  MCC2                      **0.8263**
  Weighted cleavage F1      **0.7976**

SignalP 6.0 also reports class × organism results graphically, including
Eukarya.

### Class-level information?

**YES.**

This is important:

> SignalP 6.0 **does have class-based information**, both for SP
> detection and cleavage prediction.

Its Figure 2 explicitly separates:

-   Sec/SPI
-   Sec/SPII
-   Sec/SPIII
-   Tat/SPI
-   Tat/SPII

and organism groups including Eukarya.

Therefore, it is incorrect to say that SignalP 6.0 has no class-level
evaluation.

------------------------------------------------------------------------

# 7. Paper 3 --- TSignal (2023)

## Core question

Can a fully data-driven Transformer model learn signal-peptide structure
and cleavage behavior **without hard-coding N/H/C structural assumptions
through an HMM/CRF-style model**?

## Core architecture

``` text
Protein sequence
       ↓
ProtBERT
       ↓
1024-dimensional residue representations
       ↓
Transformer encoder/decoder
       ↓
per-residue labels
       ↓
SP type + cleavage site
```

TSignal uses eight residue-level labels:

-   Sec/SPase I
-   Sec/SPase II
-   Sec/SPase IV
-   TAT/SPase I
-   TAT/SPase II
-   intracellular
-   transmembrane
-   extracellular

The SP type is inferred from the predicted label at the beginning of the
sequence.

The cleavage site is determined from the transition from SP labels to a
non-SP label.

------------------------------------------------------------------------

## Important conceptual innovation

TSignal says that unlike HMM/CRF approaches, it does **not hard-code SP
structure**.

Instead:

> The model learns the sequence-label structure from data.

This is a significant conceptual step from:

``` text
"we know the SP has N → H → C"
```

toward:

``` text
"let the model discover the relevant sequence dependencies"
```

------------------------------------------------------------------------

## TSignal benchmark

  Metric                        TSignal   SignalP 6.0
  ---------------- -------------------- -------------
  MCC1               **0.8520 ± 0.016**        0.8532
  MCC2               **0.8312 ± 0.013**        0.8263
  Weighted CS F1     **0.8127 ± 0.005**        0.7976

### Improvement in cleavage

``` text
Weighted cleavage F1

SignalP 6.0   ████████████████     0.7976
TSignal       ████████████████▎    0.8127
```

Difference:

**+0.0151 absolute F1**

The TSignal paper describes this as approximately three standard
deviations above SignalP 6.0 for the overall cleavage prediction
benchmark.

------------------------------------------------------------------------

## Class-level information?

**YES.**

TSignal evaluates SP types and organism groups.

It specifically discusses:

-   Sec/SPase I
-   Sec/SPase II
-   TAT/SPase I

and reports that the model has particularly interesting improvements for
**Sec/SPase II and TAT-related cleavage prediction**.

It also reports supplementary results for Sec/SPase IV and TAT/SPase II.

Therefore, TSignal is **not** a paper with only one overall cleavage
score.

------------------------------------------------------------------------

# 8. Paper 4 --- SaSPNet / StrucAware (2026)

## Core question

Can **3D structural information** compensate for poor sequence
representation in rare signal-peptide classes?

This paper is especially important for our discussion because it
directly attacks the **minority-class problem**.

------------------------------------------------------------------------

## Dataset imbalance

Approximate class distribution reported in the paper:

  Class             Number   Percentage
  ----------- ------------ ------------
  NO-SP             15,625    **77.0%**
  Sec/SPI            2,582       12.73%
  Sec/SPII           1,615        7.96%
  Tat/SPI              365        1.80%
  Tat/SPII              33    **0.16%**
  Sec/SPIII             70    **0.34%**
  **Total**     **20,290**         100%

This is an extreme long-tail distribution.

### Visualization

``` text
NO-SP       ██████████████████████████████████████████████████ 77.0%
Sec/SPI     ████████                                           12.7%
Sec/SPII    █████                                              8.0%
Tat/SPI     █                                                    1.8%
Sec/SPIII   ▏                                                    0.34%
Tat/SPII    ▏                                                    0.16%
```

This is why "overall accuracy" or even overall MCC can hide the real
problem.

------------------------------------------------------------------------

## SaSPNet architecture

``` text
                    Protein sequence
                          │
              ┌───────────┴───────────┐
              ↓                       ↓
           ESM-2                  Sequence encoder
              │                 CNN + BiLSTM + attention
              └───────────┬───────────┘
                          │
                    sequence features
                          │
                ┌─────────┴─────────┐
                ↓                   ↓
          predicted 3D          residue graph
           structure             GCN
                └─────────┬─────────┘
                          ↓
                    multimodal fusion
                          ↓
                    classification
                    + cleavage
```

The structural graph represents residues as nodes and spatial contacts
as edges.

------------------------------------------------------------------------

## What did SaSPNet actually improve?

The paper's key result is **not a huge universal improvement**.

Instead:

> The strongest gains occur for **minor classes**.

The paper reports:

-   improved minor-class precision
-   improved minor-class recall
-   improved minor-class F1
-   improved minor-class cleavage prediction
-   improved performance on an independent minor-class test set

The paper explicitly evaluates:

-   overall multiclass MCC
-   minority precision/recall/F1
-   one-vs-rest MCC for individual minority classes
-   overall cleavage performance
-   minority-class cleavage performance

### Therefore:

**SaSPNet is the clearest evidence among the five papers that the
minority classes themselves are still a research problem.**

------------------------------------------------------------------------

## Structure ablation

The paper shows that removing structure reduces performance.

But this does **not** mean:

> "Structure solves SP prediction."

Rather:

> **Structure provides complementary information, particularly for
> difficult/minority classes.**

This distinction is important.

------------------------------------------------------------------------

# 9. Paper 5 --- Signal-3L 4.0 (2026)

## Core question

Can better multimodal fusion of sequence and structure, together with
explicit handling of class imbalance, improve SP classification and
cleavage prediction in low-resource settings?

------------------------------------------------------------------------

## Core architecture

``` text
                     Protein sequence
                           │
                     ESM-2 / sequence
                           │
                  ┌────────┴────────┐
                  ↓                 ↓
             sequence branch    structural branch
                  │                 │
             CNN / sequence      Foldseek /
             representation      FoldExplorer
                  │                 │
                  └────────┬────────┘
                           ↓
                     Co-attention
                           ↓
                         CRF
                           ↓
                 SP type + cleavage
```

The paper tests different structural representations:

-   pLDDT features
-   pLDDT filtering
-   pLDDT gating
-   Foldseek
-   FoldExplorer

------------------------------------------------------------------------

# 10. Signal-3L 4.0: the most important numerical table

### Benchmark --- exact-match cleavage F1 (±0)

  ---------------------------------------------------------------------------------
  Model                    MCC1         MCC2   Sec/SPI CS  Sec/SPII CS   Tat/SPI CS
                                                       F1           F1           F1
  ---------------- ------------ ------------ ------------ ------------ ------------
  **SignalP 6.0**         0.843        0.798        0.638        0.818        0.557

  **Signal-3L 4.0     **0.884**    **0.861**    **0.688**    **0.927**    **0.615**
  --- Foldseek**                                                       

  **Signal-3L 4.0     **0.891**    **0.865**    **0.689**    **0.924**    **0.603**
  ---                                                                  
  FoldExplorer**                                                       
  ---------------------------------------------------------------------------------

------------------------------------------------------------------------

## Signal-3L classification improvement

Compared with SignalP 6.0:

  Metric     Signal-3L Foldseek         Gain   Signal-3L FoldExplorer         Gain
  -------- -------------------- ------------ ------------------------ ------------
  MCC1                    0.884   **+0.041**                    0.891   **+0.048**
  MCC2                    0.861   **+0.063**                    0.865   **+0.067**

So the biggest overall classification gain is in **MCC2**.

------------------------------------------------------------------------

## Signal-3L cleavage improvement

Compared with SignalP 6.0:

  SP type      SignalP 6   Foldseek         Gain   FoldExplorer         Gain
  ---------- ----------- ---------- ------------ -------------- ------------
  Sec/SPI          0.638      0.688   **+0.050**          0.689   **+0.051**
  Sec/SPII         0.818      0.927   **+0.109**          0.924   **+0.106**
  Tat/SPI          0.557      0.615   **+0.058**          0.603   **+0.046**

### This is extremely informative.

The biggest improvement is:

> **Sec/SPII cleavage: approximately +0.11 F1**

while Tat/SPI remains the lowest of the three:

> **Tat/SPI ≈ 0.60--0.62**

So it would be wrong to conclude that Tat/SPI has been "solved."

------------------------------------------------------------------------

## Plot: Signal-3L vs SignalP 6.0

``` mermaid
xychart-beta
    title "Exact-match cleavage F1: SignalP 6.0 vs Signal-3L 4.0"
    x-axis ["Sec/SPI", "Sec/SPII", "Tat/SPI"]
    y-axis "F1" 0 --> 1
    bar [0.638, 0.818, 0.557]
    bar [0.688, 0.927, 0.615]
```

**Series order:** SignalP 6.0, Signal-3L Foldseek.

------------------------------------------------------------------------

# 11. Signal-3L conditional vs unconditional cleavage

Signal-3L performs an especially useful analysis by separating:

### Unconditional cleavage

Can the model predict the cleavage site regardless of whether it first
predicts the SP type correctly?

### Conditional cleavage

Evaluate cleavage only when the global SP type was correctly identified.

This separates two sources of error.

  -----------------------------------------------------------------------
  Model                     Sec/SPI           Sec/SPII            Tat/SPI
                      unconditional      unconditional      unconditional
  -------------- ------------------ ------------------ ------------------
  Foldseek                    0.727          **0.945**          **0.640**

  FoldExplorer            **0.730**              0.941              0.635
  -----------------------------------------------------------------------

Conditional:

  -----------------------------------------------------------------------
  Model                     Sec/SPI           Sec/SPII            Tat/SPI
                        conditional        conditional        conditional
  -------------- ------------------ ------------------ ------------------
  Foldseek                **0.824**              0.990          **0.686**

  FoldExplorer                0.821          **0.991**              0.635
  -----------------------------------------------------------------------

### Interpretation

Once the model already knows the correct SP class:

> cleavage prediction becomes much easier.

This means that some of the apparent cleavage difficulty is actually
caused by **upstream SP-type recognition errors**.

------------------------------------------------------------------------

# 12. Structure ablation in Signal-3L

Signal-3L provides one of the cleanest experiments for asking:

> "Is structure actually useful?"

  -------------------------------------------------------------------------------------
  Model            Parameters        MCC1        MCC2  Sec/SPI CS   Sec/SPII Tat/SPI CS
                          (M)                                  F1      CS F1         F1
  -------------- ------------ ----------- ----------- ----------- ---------- ----------
  No structural         10.38       0.832       0.799       0.634      0.887      0.543
  branch                                                                     

  Foldseek              25.21       0.884       0.861       0.688      0.927      0.615

  FoldExplorer          25.34   **0.891**   **0.865**   **0.689**      0.924      0.603
  -------------------------------------------------------------------------------------

### Structure contribution

Compared with no structure:

  Metric             Foldseek gain   FoldExplorer gain
  ---------------- --------------- -------------------
  MCC1                      +0.052          **+0.059**
  MCC2                      +0.062          **+0.066**
  Sec/SPI CS F1             +0.054              +0.055
  Sec/SPII CS F1            +0.040              +0.037
  Tat/SPI CS F1             +0.072              +0.060

The largest cleavage gain from adding structure is for **Tat/SPI** in
this ablation.

------------------------------------------------------------------------

# 13. The most important question: what is actually still difficult?

## Short answer

### Not simply:

> "Sec/SPI is difficult."

### Not simply:

> "Tat/SPI is difficult."

### Better:

> **Exact cleavage localization and low-resource/generalization
> performance remain the central weaknesses, with difficulty varying by
> SP type and organism.**

------------------------------------------------------------------------

# 14. Which SP classes are actually "weak"?

The evidence is different across papers.

  -------------------------------------------------------------------------
  SP type / problem       Evidence                Interpretation
  ----------------------- ----------------------- -------------------------
  **Sec/SPI**             Signal-3L exact CS F1 ≈ Still imperfect, but not
                          0.69                    the weakest among the
                                                  three major types

  **Sec/SPII**            Signal-3L CS F1 ≈       **Not currently the main
                          0.92--0.93              cleavage bottleneck** in
                                                  this benchmark

  **Tat/SPI**             Signal-3L CS F1 ≈       **Clearly difficult** in
                          0.60--0.62              this benchmark

  **Tat/SPII**            SignalP6 identifies it  Low-data/generalization
                          as underrepresented;    remains important
                          SaSPNet treats it as    
                          minority                

  **Sec/SPIII**           SignalP6 specifically   Historically a major
                          reports major gains     low-data problem
                          over SignalP5           

  **Minor classes         SaSPNet explicitly      Strong evidence that the
  overall**               targets them            long tail remains
                                                  important
  -------------------------------------------------------------------------

------------------------------------------------------------------------

# 15. The long-tail problem

The five-class formulation reveals a major statistical problem.

``` text
                 Training examples

NO-SP       ███████████████████████████████████████████████
Sec/SPI     ███████
Sec/SPII    █████
Tat/SPI     █
Sec/SPIII   ▏
Tat/SPII    ▏
```

A model can obtain excellent overall performance by becoming very good
at:

-   NO-SP
-   Sec/SPI

while remaining poor on:

-   Tat/SPI
-   Tat/SPII
-   Sec/SPIII

This is why **macro metrics and per-class metrics are much more
informative than a single overall accuracy**.

------------------------------------------------------------------------

# 16. Why "the data is not few" can be misleading

A class may contain hundreds of proteins globally and still be a
**low-resource ML class**.

There are several reasons:

1.  It may contain only a small number of examples relative to the
    dominant class.
2.  Sequence redundancy must be removed.
3.  Train/test homology leakage must be avoided.
4.  Different organism groups create additional subdivisions.
5.  Rare combinations such as:

``` text
Tat/SPI × Archaea
Sec/SPII × Gram-negative
Tat/SPI × Gram-positive
```

can contain extremely few independent examples.

Signal-3L demonstrates this very clearly.

On its independent test set, three rare organism × SP-type categories
contained only **six proteins in total**, and every compared method
correctly predicted 5/6 cleavage sites.

That is a 5/6 result, but it is **not enough evidence to claim a robust
83.3% class-level performance**.

------------------------------------------------------------------------

# 17. Very important: Eukaryotes vs bacteria

Our Bioinformatics II project focuses on:

> **Eukaryotic proteins**

The five modern papers, however, use broader benchmarks containing
combinations of:

-   Eukarya
-   Gram-positive bacteria
-   Gram-negative bacteria
-   Archaea

This matters because:

### Tat

The classical Tat pathway is mainly relevant to prokaryotes and plant
chloroplasts, whereas the main eukaryotic secretory pathway is
Sec/ER-based.

Therefore, **Tat/SPI and Tat/SPII are not directly representative of the
main difficulty of our eukaryotic-only project.**

For our project, the more directly relevant questions are:

-   Eukaryotic Sec/SPI prediction
-   cleavage localization
-   SP vs N-terminal TM discrimination
-   generalization to unseen eukaryotic proteins
-   robustness to sequence redundancy
-   experimentally supported labels

------------------------------------------------------------------------

# 18. Which papers have class-level information?

This was checked explicitly.

  -----------------------------------------------------------------------
  Paper                   Class-specific results? What level?
  ----------------------- ----------------------- -----------------------
  **DeepSig**             **NO** for the later    Organism groups:
                          five SP types           Eukaryotes / Gram+ /
                                                  Gram−

  **SignalP 6.0**         **YES**                 Five SP types ×
                                                  organism groups

  **TSignal**             **YES**                 SP types × organism
                                                  groups; supplementary
                                                  detailed results

  **SaSPNet**             **YES**                 Minor-class metrics,
                                                  OvR MCC, minor-class
                                                  cleavage

  **Signal-3L 4.0**       **YES**                 Sec/SPI, Sec/SPII,
                                                  Tat/SPI + organism ×
                                                  SP-type analyses
  -----------------------------------------------------------------------

### Important correction

So if someone says:

> "One of these papers has no class-based information even in plots"

the correct answer is:

**DeepSig is the exception only because its taxonomy predates the
five-class framework.**

It still has detailed organism-specific performance.

The other four clearly contain class-level analysis.

------------------------------------------------------------------------

# 19. Five-paper comparison of the central metrics

## Overall SP classification

  ------------------------------------------------------------------------
  Paper                 Main classification   Best reported value relevant
                        metric                                        here
  --------------------- --------------------- ----------------------------
  DeepSig               MCC                         Eukaryotes **0.86** on
                                                                    SPDS17

  SignalP 6.0           MCC1                                    **0.8532**

  SignalP 6.0           MCC2                                    **0.8263**

  TSignal               MCC1                            **0.8520 ± 0.016**

  TSignal               MCC2                            **0.8312 ± 0.013**

  SaSPNet               Overall MCC             \~**0.90** range; emphasis
                                                          on minor classes

  Signal-3L Foldseek    MCC1                                     **0.884**

  Signal-3L Foldseek    MCC2                                     **0.861**

  Signal-3L             MCC1                                     **0.891**
  FoldExplorer                                

  Signal-3L             MCC2                                     **0.865**
  FoldExplorer                                
  ------------------------------------------------------------------------

**Caution:** These values come from different datasets/evaluation
protocols and should not be interpreted as one universal leaderboard.

------------------------------------------------------------------------

# 20. Cleavage-site comparison

## Most directly comparable modern benchmark

  --------------------------------------------------------------------------
  Model                 Sec/SPI       Sec/SPII        Tat/SPI      Overall /
                                                                 weighted CS
                                                                      metric
  -------------- -------------- -------------- -------------- --------------
  SignalP 6.0         **0.638**      **0.818**      **0.557**       Weighted
                                                                  **0.7976**

  TSignal                   ---            ---            ---       Weighted
                                                                  **0.8127 ±
                                                                     0.005**

  Signal-3L           **0.688**      **0.927**      **0.615**    Macro class
  Foldseek                                                     average shown

  Signal-3L           **0.689**      **0.924**      **0.603**    Macro class
  FoldExplorer                                                 average shown
  --------------------------------------------------------------------------

`—` means that the exact class-level values were not recovered as
directly comparable numeric values from the uploaded main paper text;
TSignal reports them in its supplementary material/figures.

------------------------------------------------------------------------

# 21. DeepSig vs modern models: why direct comparison is dangerous

DeepSig:

``` text
2018
SPDS17
Eukaryotes / Gram+ / Gram−
```

Modern papers:

``` text
2022–2026
multiple SP classes
multiple organism groups
different datasets
different homology partitions
different cleavage tolerances
```

Therefore:

> **Do not rank all five papers by simply putting their F1/MCC numbers
> into one leaderboard.**

The meaningful comparison is **conceptual progression + matched
benchmark comparisons where available**.

------------------------------------------------------------------------

# 22. What did each innovation actually solve?

  -----------------------------------------------------------------------
  Innovation                          What it helped
  ----------------------------------- -----------------------------------
  Deep CNN                            Learned local sequence patterns

  Explicit TM class                   Reduced SP/TM confusion

  Structured cleavage model           Improved positional consistency

  Protein LM                          Better contextual/evolutionary
                                      representation

  CRF                                 Structured residue-level
                                      predictions

  Transformer decoder                 Learned sequence-label dependencies
                                      without hard-coded SP structure

  3D structure                        Added complementary information

  GCN / structural encoder            Modeled spatial residue
                                      relationships

  Co-attention                        Let sequence and structure interact
                                      rather than simply concatenate

  LDAM / class-aware loss             Addressed long-tail class imbalance

  Independent minor-class test        Tested whether rare-class
                                      improvements generalize
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 23. The evolution of the field

``` text
von Heijne
   │
   │ hand-designed statistical signal
   ↓
DeepSig
   │
   │ CNN + structured cleavage model
   ↓
SignalP 6.0
   │
   │ protein language model + CRF
   ↓
TSignal
   │
   │ PLM + Transformer sequence labeling
   ↓
SaSPNet
   │
   │ sequence + PLM + 3D structure + GCN
   ↓
Signal-3L 4.0
   │
   │ multimodal co-attention
   │ + structural representation
   │ + CRF
   │ + imbalance-aware learning
   ↓
Current frontier
```

------------------------------------------------------------------------

# 24. Is structure actually useful?

## Evidence from SaSPNet

Yes, especially for minority classes.

But the improvement is not equivalent to:

> "Sequence models cannot solve SP prediction."

Instead:

> **Sequence information remains foundational; structure provides
> complementary information.**

## Evidence from Signal-3L

The ablation is even clearer:

``` text
No structure
    ↓
MCC1 = 0.832
MCC2 = 0.799

        + structure

Foldseek
    ↓
MCC1 = 0.884
MCC2 = 0.861

FoldExplorer
    ↓
MCC1 = 0.891
MCC2 = 0.865
```

So structure contributes real information.

But the model becomes much larger:

``` text
No structural branch       ~10.38 M parameters
Foldseek                   ~25.21 M
FoldExplorer               ~25.34 M
```

Thus the question is not:

> "Does structure help?"

It does.

The more interesting question is:

> **Is the gain large enough to justify the additional structural
> prediction and model complexity?**

------------------------------------------------------------------------

# 25. The strongest evidence against "structure alone solves it"

Signal-3L's own baseline experiments show that:

> **ESM2 + CRF remains a very strong baseline.**

The sequence/PLM branch is the foundation.

Signal-3L explicitly concludes that sequence remains primary and
structure complementary.

This is consistent with the broader progression:

``` text
Sequence
   ↓
Protein language model
   ↓
still extremely powerful
   +
Structure
   ↓
additional information, especially difficult cases
```

------------------------------------------------------------------------

# 26. Cleavage-site prediction is a special problem

The cleavage site is difficult because there is no perfectly conserved
motif.

A common pattern is:

``` text
... [hydrophobic H-region] ... small residues ... | mature protein
                                                   ↑
                                                cleavage
```

Often an Ala-X-Ala-like pattern occurs, but it is not a universal
deterministic rule.

The Bioinformatics II material uses a cleavage window such as:

``` text
[-13, +2]
```

around the cleavage position for sequence-logo analysis.

This is an important distinction:

> The biologically relevant cleavage context can be local, while the
> model may use a much larger N-terminal context to decide whether the
> protein is an SP at all.

------------------------------------------------------------------------

# 27. Why cleavage can remain hard even when SP detection is excellent

Imagine:

``` text
Protein A

SP --------------------|
                       ↑
                   true CS = 20

Model prediction:
SP -------------------|
                      ↑
                  predicted CS = 19
```

Biologically, positions 19 and 20 may both look plausible.

But exact-match F1 gives:

``` text
correct = 0
```

unless the evaluation allows ±1.

This explains why:

> SP classification can be 0.89 MCC while exact cleavage F1 is only
> \~0.60--0.70 for difficult classes.

------------------------------------------------------------------------

# 28. Most important evidence for the "minority-class" problem

## SignalP 6.0

Explicitly reports that performance improved substantially for:

-   **Sec/SPIII**
-   **Tat/SPII**

because these were underrepresented.

## SaSPNet

Builds an explicit minority-class evaluation.

## Signal-3L 4.0

Explicitly evaluates low-resource/challenging settings and reports
class-specific cleavage.

Therefore, the long-tail problem is **not merely our interpretation**.

It is a recurring design motivation in modern SP prediction.

------------------------------------------------------------------------

# 29. But what is the single most important unresolved problem?

For a research project, I would phrase it as:

> ### Robust cleavage-site localization and SP-type prediction for low-resource, weakly represented, and evolutionarily distant signal peptides.

For a **eukaryotic-only** project:

> ### Can we accurately localize the cleavage site and distinguish a true cleavable eukaryotic signal peptide from a similar N-terminal membrane anchor in evolutionarily novel proteins?

This combines the most important unresolved biological/ML issues.

------------------------------------------------------------------------

# 30. Why SP vs TM is still important

DeepSig showed that N-terminal TM helices are a major source of
confusion.

The reason is simple:

``` text
SIGNAL PEPTIDE

N-region → HYDROPHOBIC CORE → cleavage
                             ↓
                       hydrophobic part removed


TRANSMEMBRANE HELIX

N-region → HYDROPHOBIC CORE → remains in membrane
                             ↓
                       membrane anchor
```

Same broad physical signal:

> hydrophobic N-terminal region

Different biological fate:

> **cleaved vs retained**

This makes SP/TM discrimination a fundamental problem.

However, based on the five papers reviewed here, **cleavage
localization + rare-class generalization now appears to be a stronger
modern research opportunity than simply building another SP/TM
classifier.**

------------------------------------------------------------------------

# 31. Recommended evaluation strategy for our project

Because our project is **eukaryotic-only**, a strong evaluation should
not rely on only one number.

## Report:

### A. SP detection

-   MCC
-   precision
-   recall
-   F1
-   PR-AUC if appropriate

### B. Cleavage prediction

Report:

-   exact match (±0)
-   ±1
-   ±2
-   ±3 residues

### C. Per-class / per-subgroup

For eukaryotes, stratify where sample sizes permit:

-   kingdom
-   major taxonomic groups
-   protein length
-   SP length
-   sequence similarity to training set

### D. Hard negatives

Especially:

-   N-terminal TM proteins
-   membrane proteins
-   proteins with signal-anchor-like N-termini

### E. Homology-aware test

This is essential.

A model can appear excellent if highly similar proteins occur in both
training and test sets.

------------------------------------------------------------------------

# 32. What we should NOT do

Avoid:

``` text
Random train/test split
        ↓
99% accuracy
        ↓
"Excellent new SP predictor!"
```

Instead:

``` text
cluster / homology reduction
        ↓
train
        ↓
distant test proteins
        ↓
per-class metrics
        ↓
cleavage tolerance curves
```

The goal is to measure:

> **generalization to proteins the model has not effectively seen
> before.**

------------------------------------------------------------------------

# 33. Best metrics to emphasize in our manuscript

If only a few numbers can be shown:

  ------------------------------------------------------------------------
                      Priority Metric                Why
  ---------------------------- --------------------- ---------------------
                             1 **Per-class cleavage  Directly exposes weak
                               F1**                  SP types

                             2 **Macro-average       Prevents dominant
                               cleavage F1**         classes from hiding
                                                     minority classes

                             3 **MCC**               Strong balanced
                                                     classification metric

                             4 **SP/TM               Important biological
                               false-positive rate** failure mode

                             5 **Cleavage accuracy   Shows whether errors
                               ±1/±2/±3**            are biologically
                                                     close

                             6 Weighted F1           Useful, but can hide
                                                     minority classes
  ------------------------------------------------------------------------

------------------------------------------------------------------------

# 34. A useful figure for our future project

A very informative final figure would be:

``` text
                 Cleavage F1
                     ↑
1.0 ┤
    │       ●
0.9 ┤    ●     ●
    │
0.8 ┤
    │
0.7 ┤ ●
    │
0.6 ┤             ●
    │
0.5 ┤
    └────────────────────────→
       Sec/SPI  Sec/SPII  Tat/SPI
```

with separate curves for:

-   our model
-   SignalP6
-   TSignal
-   Signal-3L
-   possibly SaSPNet

**But only when the underlying benchmark and metric definition are
sufficiently comparable.**

------------------------------------------------------------------------

# 35. Final comparison

  ---------------------------------------------------------------------------------------------------------
  Dimension                    DeepSig     SignalP6               TSignal     SaSPNet     Signal-3L
  ---------------------------- ----------- ---------------------- ----------- ----------- -----------------
  Deep sequence learning       ✓           ✓                      ✓           ✓           ✓

  Protein LM                   ---         ✓                      ✓           ✓           ✓

  Structured prediction        ✓           ✓                      ---         ✓           ✓

  Explicit five-class SP       ---         ✓                      ✓           ✓           partial/major 3
  taxonomy                                                                                classes

  TM-aware evaluation          ✓           ✓                      ✓           ✓           ✓

  Rare-class focus             limited     **strong**             moderate    **very      **strong**
                                                                              strong**    

  3D structure                 ---         ---                    ---         **✓**       **✓**

  Multimodal fusion            ---         ---                    ---         ✓           **✓
                                                                                          co-attention**

  Class-imbalance handling     ---         implicit/data-driven   ---         ✓ LDAM      ✓ imbalance-aware

  Detailed cleavage evaluation ✓           ✓                      **✓**       ✓           **✓✓**

  Independent/generalization   ✓           ✓                      ✓           ✓           **✓**
  evaluation                                                                              
  ---------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 36. Bottom line

### DeepSig

Solved an important earlier problem:

> **deep sequence representation + better SP/TM discrimination +
> structured cleavage prediction**

### SignalP 6.0

Solved another major problem:

> **protein language models substantially improve rare SP-type
> recognition**

Especially:

> **Sec/SPIII and Tat/SPII**

### TSignal

Asked:

> **Can a Transformer learn SP structure instead of having it
> hard-coded?**

Answer:

> Yes, and cleavage F1 improved modestly over SignalP 6.0.

### SaSPNet

Asked:

> **Can 3D structure help the long-tail classes?**

Answer:

> Yes, especially for minority classes and minority-class cleavage
> prediction.

### Signal-3L 4.0

Asked:

> **Can sequence + structure be fused better, while explicitly
> addressing imbalance?**

Answer:

> Yes. It improves overall classification and cleavage, with the largest
> benchmark cleavage gain for **Sec/SPII**, while **Tat/SPI remains
> substantially harder**.

------------------------------------------------------------------------

# 37. Final research insight

The literature does **not** support:

> "We just need a bigger model."

Instead, the five papers suggest:

``` text
                    ┌─────────────────────────┐
                    │  Protein language model │
                    └────────────┬────────────┘
                                 ↓
                         strong baseline
                                 │
               ┌─────────────────┴─────────────────┐
               ↓                                   ↓
        rare-class problem                  cleavage problem
               ↓                                   ↓
       imbalance-aware ML                  better localization
               │                                   │
               └─────────────────┬─────────────────┘
                                 ↓
                         structural information
                                 ↓
                         multimodal models
                                 ↓
                    better difficult-case performance
```

So the strongest unresolved question for our project is:

> **Can we improve cleavage-site localization and generalization for
> difficult, evolutionarily distant eukaryotic signal peptides without
> simply increasing model complexity?**

That is more scientifically interesting than asking only:

> "Can we increase overall SP accuracy?"

------------------------------------------------------------------------

# 38. Source papers used

All five papers were provided in the project files:

1.  **DeepSig.pdf**\
    Savojardo et al. (2018), *DeepSig: deep learning improves signal
    peptide detection in proteins.*

2.  **SignalP6.pdf**\
    Teufel et al. (2022), *SignalP 6.0 predicts all five types of signal
    peptides using protein language models.*

3.  **tSignal.pdf**\
    *TSignal* (2023), Transformer/ProtBERT-based signal peptide and
    cleavage-site prediction.

4.  **StrucAware.pdf**\
    SaSPNet / StrucAware (2026), structure-aware multimodal prediction
    with emphasis on minority classes.

5.  **Signal-3L.pdf**\
    Piao et al. (2026), *Signal-3L 4.0*, multimodal sequence/structure
    signal-peptide prediction with co-attention and imbalance-aware
    learning.

------------------------------------------------------------------------

## Important comparison caveat

**Metrics across different papers are not automatically comparable.**

Differences include:

-   dataset composition
-   organism groups
-   SP classes
-   train/test splitting
-   sequence homology reduction
-   cross-validation vs blind testing
-   exact vs tolerance-based cleavage evaluation
-   macro vs weighted averaging
-   coupled vs conditional/unconditional cleavage evaluation

Therefore, the safest interpretation is:

> **Use within-paper improvements for quantitative claims, and use
> cross-paper comparisons primarily to understand the evolution of the
> research problem.**
