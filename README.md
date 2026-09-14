# Quantum Algorithm Performance Under Noise

A research-oriented quantum computing project investigating how different noise mechanisms affect the reliability of quantum circuits as **circuit depth**, **qubit count**, and **noise strength** increase.

The project implements five different noise models, runs controlled experiments using Qiskit Aer, computes statistical performance metrics over repeated trials, generates analysis figures, and provides an interactive Streamlit dashboard for exploring the results.

---

## Overview

Quantum computers are inherently sensitive to noise. Errors can occur during quantum gates, interactions between qubits, and measurement. As quantum circuits become deeper and involve more qubits, these errors can accumulate and reduce the probability of obtaining the intended result.

This project studies that behavior experimentally using controlled simulations of a benchmark quantum circuit under noise — it is **not** a study of a specific quantum algorithm.

The primary research question is:

> **How does quantum circuit performance degrade under different noise models as circuit depth, qubit count, and noise strength increase?**

The project compares:

- Bit-flip noise
- Phase-flip noise
- Depolarizing noise
- Readout error
- Thermal relaxation

Performance is evaluated using:

- Success probability
- Error rate
- Measurement-distribution fidelity
- Circuit gate count
- Statistical variation across repeated experiments
- 95% confidence intervals

---

## Research Questions

The experiment was designed around several questions:

1. How does increasing noise strength affect quantum circuit success probability?
2. How does increasing circuit depth affect performance?
3. How does increasing the number of qubits affect sensitivity to noise?
4. Which noise models produce the largest performance degradation?
5. Are some types of noise significantly more damaging than others?
6. How consistent are results across independent simulation repetitions?

---

## Experimental Design

The experiment systematically varies three primary circuit/noise parameters.

### Qubit Count

```text
2, 3, 4, 5, 6
```

### Circuit Depth

```text
1, 2, 4, 8, 16, 32
```

### Noise Strength

```text
0.000
0.001
0.002
0.005
0.010
0.020
0.050
0.100
```

### Shots

Each circuit configuration is simulated using:

```text
1000 shots
```

A shot represents one execution of the circuit.

### Repetitions

Every experimental condition is independently repeated:

```text
5 times
```

using different simulator seeds. This allows the experiment to estimate variability rather than relying on a single simulation result.

---

## Experimental Dataset

The complete validation experiment contains:

```text
5 noise models
× 5 qubit counts
× 6 circuit depths
× 8 noise levels
× 5 repetitions
= 6,000 experimental runs
```

Each run produces measurements and performance metrics. The resulting raw dataset contains approximately **6,000 rows**, including:

- Number of qubits
- Circuit depth
- Noise model
- Gate count
- Noise strength
- Number of shots
- Random seed
- Repetition number
- Success probability
- Error rate
- Measurement fidelity
- Measurement counts

---

## Circuit Design

### Benchmark Circuit

The project uses a deterministic benchmark circuit designed to contain both:

- Single-qubit operations
- Multi-qubit entangling operations

The circuit begins by placing every qubit into superposition using Hadamard gates.

```text
|0> ──H── ...
|0> ──H── ...
|0> ──H── ...
...
```

The circuit then performs repeated layers of entangling operations. Adjacent qubits are connected using CNOT gates:

```text
q0 ──●────────
     │
q1 ──X──●─────
        │
q2 ────X──●───
           │
q3 ───────X───
```

The circuit subsequently applies additional Hadamard gates and reverses the entangling structure. This creates a computation that contains non-trivial quantum operations while ultimately being **uncomputed back toward a deterministic final state**.

The deterministic ideal output is important because it provides a clear reference against which noisy executions can be compared.

### Circuit Construction

For a selected depth `d`, the circuit performs:

1. Hadamard gates on every qubit.
2. `d` layers of nearest-neighbor CNOT operations.
3. Hadamard gates across all qubits after each entangling layer.
4. A reverse sequence of Hadamard and CNOT operations.
5. A final layer of Hadamard gates.

The number of operations therefore grows with both the number of qubits and the requested circuit depth, allowing the experiment to investigate how accumulated operations influence noise sensitivity.

---

## Ideal Reference

For every experimental configuration, the circuit is first executed **without noise**. The resulting measurement distribution is used as the ideal reference.

The most frequently observed ideal measurement state is selected as the expected state:

```python
expected_state = max(
    ideal_counts,
    key=ideal_counts.get
)
```

The noisy execution is then compared against this reference. The experiment does not assume a hard-coded output bitstring — the expected state is determined from the ideal simulation itself.

---

## Noise Models

Five different noise models are implemented, each representing a different mechanism through which quantum computations can become unreliable.

### 1. Bit-Flip Noise

**Concept:** Bit-flip noise applies an `X` operation with probability `p`, analogous to flipping a computational-basis bit (`|0>` → `|1>`, `|1>` → `|0>`).

```text
X with probability p
I with probability 1-p
```

**Implementation:**

```python
single_qubit_error = pauli_error([
    ("X", probability),
    ("I", 1 - probability)
])
```

Applied to `H` and `X` single-qubit gates. For CNOT gates, the single-qubit error is tensored with itself:

```python
two_qubit_error = (
    single_qubit_error.tensor(single_qubit_error)
)
```

### 2. Phase-Flip Noise

**Concept:** Phase-flip noise applies a `Z` operation with probability `p`. Unlike a bit flip, this does not change the computational-basis value directly — it changes the phase of the quantum state.

```text
Z with probability p
I with probability 1-p
```

**Implementation:**

```python
single_qubit_error = pauli_error([
    ("Z", probability),
    ("I", 1 - probability)
])
```

Applied to single-qubit gates, with a tensor-product version applied to CNOT operations.

### 3. Depolarizing Noise

**Concept:** Depolarizing noise represents a more general loss of quantum-state information, introducing randomized errors across the quantum state rather than one specific error type.

**Implementation:**

```python
# Single-qubit gates
single_qubit_error = depolarizing_error(probability, 1)

# Two-qubit gates
two_qubit_error = depolarizing_error(probability, 2)
```

### 4. Readout Error

**Concept:** Readout error occurs when the quantum state is correct but the measurement system reports the wrong classical result.

```text
P(measured 0 | actual 0) = 1-p
P(measured 1 | actual 0) = p
P(measured 0 | actual 1) = p
P(measured 1 | actual 1) = 1-p
```

**Implementation:**

```python
ReadoutError([
    [1 - probability, probability],
    [probability, 1 - probability]
])
```

Unlike the gate-based noise models, this noise occurs at the **measurement stage**.

### 5. Thermal Relaxation

**Concept:** Thermal relaxation models physical processes associated with finite qubit coherence times.

- **T1** (energy-relaxation timescale): `50 μs`
- **T2** (phase-coherence timescale): `70 μs`

These values are representative experimental parameters rather than measurements from a particular physical quantum processor.

**Thermal Noise Strength:** For the Pauli and depolarizing models, the experimental parameter can be interpreted directly as an error probability. For thermal relaxation, the experimental parameter instead scales the effective gate duration:

```python
gate_time = noise_strength * 1e-6
```

The resulting gate time is passed into:

```python
thermal_relaxation_error(t1, t2, gate_time)
```

> **The thermal `noise_strength` parameter is an experimental control variable and should not be interpreted as a literal physical error probability.** This distinction matters when comparing thermal relaxation against the other noise models.

---

## Simulation

The project uses Python, Qiskit, and Qiskit Aer. The simulator is `AerSimulator`.

Each circuit is copied and measurements are added before execution:

```python
simulator.run(
    measured_circuit,
    shots=1000,
    seed_simulator=seed
)
```

The simulator returns measurement counts such as:

```text
{'000': 972, '001': 12, '100': 9, '010': 7}
```

These counts are then converted into performance metrics.

---

## Performance Metrics

### Success Probability

```text
success probability = successful shots / total shots
```

Example: expected state `000` observed 900/1000 times → success probability = 0.90.

A value of `1.0` means every shot produced the expected state; `0.0` means it was never observed.

### Error Rate

```text
error rate = 1 - success probability
```

### Measurement-Distribution Fidelity

The project calculates fidelity between the ideal and noisy **measurement probability distributions**:

```text
F(P,Q) = ( Σ √(P(x)Q(x)) )²
```

```python
fidelity = sum(
    (ideal.get(state, 0) * noisy.get(state, 0)) ** 0.5
    for state in all_states
) ** 2
```

> **Important terminology:** this project refers to this quantity as **Measurement Fidelity**. It is **not** a full quantum-state fidelity calculation using density matrices or statevectors. Because the ideal benchmark circuit produces a deterministic measurement distribution, measurement fidelity and success probability are effectively equivalent for this particular benchmark — but the distinction is retained so the metric isn't misrepresented as a general quantum-state fidelity measure.

---

## Repeated Experiments and Statistics

Each experimental condition is repeated five times with independent simulator seeds (`seed = 0, 1, 2, 3, 4`), allowing the project to estimate variation caused by finite sampling.

For each experimental condition, the analysis computes:

- Mean success probability
- Standard deviation of success probability
- Mean fidelity
- Standard deviation of fidelity
- Mean error rate
- 95% confidence interval

### Confidence Intervals

With `n = 5` independent repetitions, the analysis uses the Student's t-distribution with `degrees of freedom = 4` and critical value `t = 2.776`:

```text
mean ± t × standard_error
standard_error = standard_deviation / √n
```

---

## Analysis Pipeline

```text
Benchmark Circuit
       ↓
Ideal Simulation
       ↓
Expected Measurement State
       ↓
Noise Model
       ↓
Noisy Simulation
       ↓
Measurement Counts
       ↓
Metrics
       ↓
Raw Dataset
       ↓
Statistical Analysis
       ↓
Sensitivity Analysis
       ↓
Noise Model Comparison
       ↓
Figures + Dashboard
```

---

## Project Structure

```text
quantum-noise-analysis/
│
├── app.py
├── config.py
├── styles.css
├── requirements.txt
├── .gitignore
│
├── analysis/
│   ├── noise_model_comparison.py
│   ├── noise_sensitivity.py
│   ├── sensitivity.py
│   └── statistics.py
│
├── experiments/
│   └── run_experiment.py
│
├── plots/
│   ├── noise_vs_success.py
│   ├── depth_vs_success.py
│   ├── qubits_vs_success.py
│   └── error_bars.py
│
├── results/
│   ├── raw/
│   │   └── noise_experiment.csv
│   │
│   ├── processed/
│   │   ├── statistical_results.csv
│   │   ├── noise_sensitivity_results.csv
│   │   ├── noise_model_comparison_results.csv
│   │   └── experiment_metadata.json
│   │
│   └── figures/
│       ├── noise_vs_success.png
│       ├── depth_vs_success.png
│       ├── qubits_vs_success.png
│       └── error_bars.png
│
└── src/
    ├── circuits.py
    ├── simulator.py
    ├── metrics.py
    ├── noise_models.py
    └── experiment_engine.py
```

---

## Code Architecture

**`src/circuits.py`** — generates the benchmark quantum circuit.

```python
create_circuit(num_qubits, depth)
```

**`src/noise_models.py`** — contains all five noise-model implementations:

```python
create_bit_flip_noise()
create_phase_flip_noise()
create_depolarizing_noise()
create_readout_noise()
create_thermal_relaxation_noise()
```

**`src/simulator.py`** — executes circuits using Qiskit Aer.

```python
run_circuit()
```

The simulator accepts an optional noise model and random seed.

**`src/metrics.py`** — calculates success probability, error rate, measurement fidelity, and probability distributions.

**`src/experiment_engine.py`** — connects the circuit, simulator, noise models, and metrics. Provides:

```python
run_experiment()          # single experimental condition
run_repeated_experiment() # repeated trials
```

**`experiments/run_experiment.py`** — runs the complete parameter sweep, iterating through noise model → qubit count → circuit depth → noise strength → repeated trials. Writes the final raw dataset to `results/raw/noise_experiment.csv`.

---

## Statistical Analysis

`analysis/statistics.py` aggregates the raw experimental data by `qubits`, `depth`, `noise_model`, and `noise_probability`, producing `results/processed/statistical_results.csv` — aggregated means, standard deviations, error rates, and confidence intervals.

---

## Sensitivity Analysis

The project evaluates how strongly performance changes as experimental parameters change, investigating sensitivity to noise strength, circuit depth, and number of qubits. Results are saved to `results/processed/noise_sensitivity_results.csv`.

---

## Noise Model Comparison

The project aggregates performance across the different noise models, including mean success probability, overall degradation, and relative model performance. Results are saved to `results/processed/noise_model_comparison_results.csv`.

The validated experiment produced the following overall mean success probabilities:

| Noise Model        | Mean Success Probability | Mean Degradation |
| ------------------ | ------------------------: | -----------------: |
| Thermal relaxation |                     0.9822 |               1.78% |
| Readout            |                     0.9166 |               8.34% |
| Depolarizing       |                     0.6069 |              39.31% |
| Bit flip           |                     0.5975 |              40.25% |
| Phase flip         |                     0.5797 |              42.03% |

These values summarize the current 6,000-run experiment across all tested qubit counts, depths, noise strengths, and repetitions. They should **not** be interpreted as universal rankings of physical quantum hardware — they describe performance under this project's benchmark circuit, parameter ranges, and simulated noise assumptions.

---

## Visualizations

**Noise Strength vs Success Probability** — shows how success probability changes as noise strength increases, helping identify which noise mechanisms cause the fastest degradation.

**Circuit Depth vs Success Probability** — shows the relationship between circuit depth and successful execution, investigating whether additional computation layers increase exposure to noise.

**Qubit Count vs Success Probability** — shows how increasing the number of qubits affects circuit performance, investigating whether larger circuits are more sensitive to the tested noise models.

**Error Bars** — uses the repeated experiments to show statistical variation and confidence intervals, providing more information than plotting only the mean value.

---

## Interactive Dashboard

The project includes a Streamlit dashboard:

```bash
streamlit run app.py
```

The dashboard allows users to interactively select noise model, number of qubits, circuit depth, and noise strength, and displays success probability, error rate, measurement fidelity, gate count, and measurement outcome distributions.

It also provides analysis sections for:

**Parameter Sensitivity**
- Success vs noise strength
- Success vs circuit depth
- Success vs qubit count
- Fidelity vs depth

**Comparative Analysis**
- Noise model comparison
- Depth × noise heatmap
- Performance loss

**Statistical Summary**
- Aggregated experimental statistics and model rankings

The dashboard reads the processed experimental data rather than duplicating the research logic.

---

## Configuration

Experiment parameters are centralized in `config.py`:

```python
NOISE_PROBABILITIES
DEPTHS
QUBIT_COUNTS
NOISE_MODELS
DEFAULT_SHOTS
DEFAULT_REPETITIONS
```

Thermal relaxation parameters are also defined centrally:

```python
T1 = 50e-6
T2 = 70e-6
```

Output paths are centralized as well, preventing different parts of the project from using inconsistent dataset or result locations.

---

## Reproducing the Experiment

### 1. Clone the repository

```bash
git clone https://github.com/Ybotic/quantum-noise-analysis.git
cd quantum-noise-analysis
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the full experiment

```bash
python -m experiments.run_experiment
```

This executes the complete parameter sweep and generates:

```text
results/raw/noise_experiment.csv
results/processed/experiment_metadata.json
```

### 5. Generate statistical results

```bash
python -m analysis.statistics
```

### 6. Run sensitivity analysis

```bash
python -m analysis.noise_sensitivity
```

### 7. Run noise-model comparison

```bash
python -m analysis.noise_model_comparison
```

### 8. Generate figures

```bash
python -m plots.noise_vs_success
python -m plots.depth_vs_success
python -m plots.qubits_vs_success
python -m plots.error_bars
```

Figures are saved to `results/figures/`.

### 9. Launch the dashboard

```bash
streamlit run app.py
```

---

## Requirements

The project uses the following major packages:

```text
qiskit==2.5.0
qiskit-aer==0.17.2
numpy==2.5.1
pandas==3.0.5
matplotlib==3.11.1
plotly==7.0.0
streamlit==1.63.0
```

Exact dependencies are provided in `requirements.txt`.

---

## Validation

The generated dataset was validated for expected row count, expected parameter combinations, duplicate experimental conditions, missing values, valid probability ranges, shot counts, repetition indices, metric consistency, statistical aggregation, confidence interval validity, and metadata consistency.

The validation experiment produced:

```text
6,000 raw experimental rows
1,200 rows per noise model
1,200 statistical aggregation rows
40 sensitivity-analysis rows
5 noise-model comparison rows
```

Consistency checks:

**Error Rate** — the maximum numerical difference between the stored error rate and `1 - success_probability` was approximately `1.1 × 10⁻¹⁶`, effectively zero and attributable to floating-point representation.

**Fidelity** — the maximum numerical difference between measurement fidelity and success probability was also approximately `1.1 × 10⁻¹⁶`, expected for the deterministic ideal measurement distribution used by the benchmark.

---

## Methodological Limitations

This project is a controlled simulation study rather than a direct characterization of a physical quantum processor. Several limitations should be considered:

1. **Simulated Noise** — all experiments use Qiskit Aer noise models; results do not directly represent the behavior of a specific physical quantum computer.
2. **Benchmark Circuit** — the experiment uses one deterministic benchmark circuit structure; different quantum algorithms or circuit architectures may respond differently to noise, so results should not be generalized to all quantum algorithms.
3. **Measurement Fidelity** — the fidelity metric is between classical measurement distributions, not a general quantum-state fidelity calculated from density matrices or statevectors.
4. **Thermal Relaxation Parameters** — `T1 = 50 μs` and `T2 = 70 μs` are assumed representative values, not measurements from a particular quantum processor.
5. **Thermal Noise Parameter** — for thermal relaxation, `noise_strength` represents a scaling of effective gate duration, not a probability directly equivalent to the other four models.
6. **Limited Qubit Range** — the current experiment tests 2–6 qubits; larger systems may exhibit additional scaling effects not captured here.
7. **Limited Repetitions** — each condition currently uses five repetitions; more repetitions would provide more precise estimates of statistical uncertainty.

---

## Future Work

- Running larger parameter sweeps
- Increasing the number of qubits, shots, and repetitions
- Testing additional circuit architectures and multiple quantum algorithms
- Introducing realistic hardware calibration data
- Comparing simulated noise against real quantum hardware
- Running the same circuits on cloud-accessible QPUs
- Studying error mitigation techniques and comparing error correction strategies
- Investigating how individual gate types contribute to accumulated error

A particularly important extension is comparing:

```text
Ideal simulation
      ↓
Noisy simulation
      ↓
Real quantum hardware
```

This would allow the simulated noise models to be compared against experimentally observed hardware behavior.

---

## Research Reproducibility

The project is designed so that the experiment can be reproduced from the source code. The experimental configuration is stored in `config.py` and exported as `results/processed/experiment_metadata.json`.

The raw experimental results are stored separately from processed statistical results, allowing the raw data to be independently reanalyzed without rerunning the quantum simulations.

---

## Technologies

- **Python** — experiment and analysis implementation
- **Qiskit** — quantum circuit construction
- **Qiskit Aer** — quantum simulation and noise modeling
- **NumPy** — numerical calculations
- **Pandas** — data processing and statistical aggregation
- **Matplotlib** — research visualizations
- **Plotly** — interactive visualizations
- **Streamlit** — interactive research dashboard

---

## Project Goals

The purpose of this project is not simply to demonstrate quantum circuits. The goal is to build a reproducible experimental framework for studying:

```text
Quantum Circuit
      +
Noise
      +
Circuit Complexity
      ↓
Observed Reliability
```

By systematically varying circuit depth, qubit count, and noise strength, the project provides a controlled way to study how different noise mechanisms influence quantum computation.

---

## Author

**Ybotic**

University of Maryland, College Park — Computer Science

GitHub: [https://github.com/Ybotic](https://github.com/Ybotic)