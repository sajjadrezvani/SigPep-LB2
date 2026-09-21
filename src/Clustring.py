import os
import subprocess
from pathlib import Path

# Project directories
project_root = Path(__file__).resolve().parent.parent
raw_dir = project_root / "data" / "raw"
processed_dir = project_root / "data" / "processed"
processed_dir.mkdir(parents=True, exist_ok=True)

# Download and setup MMseqs2 on the Linux VM
mmseqs_dir = project_root / "mmseqs"
mmseqs_bin = mmseqs_dir / "bin" / "mmseqs"

if not mmseqs_bin.exists():
    os.system(
        f"wget -q https://mmseqs.com/latest/mmseqs-linux-avx2.tar.gz "
        f"-O {project_root}/mmseqs.tar.gz"
    )
    os.system(f"mkdir -p {mmseqs_dir}")
    os.system(f"tar -xzf {project_root}/mmseqs.tar.gz -C {mmseqs_dir} --strip-components=1")

def cluster_dataset(name):
    """Cluster one dataset and keep one representative per cluster."""
    fasta = raw_dir / f"{name}.fasta"
    tsv = raw_dir / f"{name}.tsv"
    output_prefix = processed_dir / f"{name}_clusters"
    tmp_dir = processed_dir / f"{name}_tmp"
    representative_fasta = Path(f"{output_prefix}_rep_seq.fasta")
    representative_tsv = processed_dir / f"{name}_representatives.tsv"

    # MMseqs2: 30% identity, 40% coverage, coverage on query and target
    subprocess.run([
        str(mmseqs_bin), "easy-cluster",
        str(fasta),
        str(output_prefix),
        str(tmp_dir),
        "--min-seq-id", "0.30",
        "-c", "0.40",
        "--cov-mode", "0",
        "--cluster-mode", "1"
    ], check=True)

    # Get UniProt accessions of representative sequences
    representatives = []

    with open(representative_fasta) as f:
        for line in f:
            if line.startswith(">"):
                representatives.append(line[1:].strip().split()[0])

    # Keep only representative proteins in the original TSV
    with open(tsv) as infile, open(representative_tsv, "w") as outfile:
        header = infile.readline()
        outfile.write(header)

        accession_index = header.rstrip("\n").split("\t").index("accession")

        for line in infile:
            fields = line.rstrip("\n").split("\t")
            if fields[accession_index] in representatives:
                outfile.write(line)

    print(f"{name}: {len(representatives)} representatives → {representative_tsv}")

cluster_dataset("positive")
cluster_dataset("negative")