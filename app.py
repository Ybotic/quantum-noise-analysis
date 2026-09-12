import streamlit as st

from src.experiment_engine import run_experiment

import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Quantum Noise Analysis",
    page_icon="⚛️",
    layout="wide"
)


st.title("Quantum Algorithm Performance Under Noise")

st.write(
    "Explore how noise affects quantum circuit reliability."
)

st.sidebar.header("Experiment Controls")


noise_model = st.sidebar.selectbox(
    "Noise Model",
    [
        "bit_flip",
        "phase_flip",
        "depolarizing",
        "readout",
        "thermal"
    ]
)


qubits = st.sidebar.number_input(
    "Number of Qubits",
    min_value=2,
    max_value=6,
    value=3,
    step=1
)


depth = st.sidebar.selectbox(
    "Circuit Depth",
    [1, 2, 4, 8, 16, 32],
    index=3
)


noise_probability = st.sidebar.selectbox(
    "Noise Strength",
    [
        0.000,
        0.001,
        0.002,
        0.005,
        0.010,
        0.020,
        0.050,
        0.100
    ],
    index=4,
    format_func=lambda x: f"{x:.3f}"
)

st.divider()


run_button = st.button(
    "Run Experiment",
    type="primary",
    use_container_width=True
)


if run_button:

    with st.spinner("Running quantum simulation..."):

        result = run_experiment(
            num_qubits=qubits,
            depth=depth,
            noise_model=noise_model,
            noise_probability=noise_probability,
            shots=1000,
            seed=1
        )

    st.session_state["result"] = result


st.subheader("Experiment Results")


if "result" not in st.session_state:

    st.info(
        "Configure the experiment and click **Run Experiment**."
    )

else:

    result = st.session_state["result"]

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Success Probability",
        f"{result['success_probability']:.2%}"
    )


    col2.metric(
        "Error Rate",
        f"{result['error_rate']:.2%}"
    )


    col3.metric(
        "Fidelity",
        f"{result['fidelity']:.2%}"
    )


    col4.metric(
        "Gate Count",
        result["gate_count"]
    )

st.divider()

st.subheader("Success Probability vs Noise Strength")

df = pd.read_csv(
    "results/processed/statistical_results.csv"
)

plot_data = df[
    (df["noise_model"] == noise_model)
    & (df["qubits"] == qubits)
    & (df["depth"] == depth)
]

fig = px.line(
    plot_data,
    x="noise_probability",
    y="mean_success",
    markers=True,
    labels={
        "noise_probability": "Noise Strength",
        "mean_success": "Mean Success Probability"
    },
    title=(
        f"{noise_model.replace('_', ' ').title()} "
        f"— {qubits} Qubits, Depth {depth}"
    )
)

fig.update_yaxes(
    tickformat=".0%",
    range=[0, 1]
)

fig.update_xaxes(
    tickformat=".3f"
)

fig.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Success Probability vs Circuit Depth")

depth_data = df[
    (df["noise_model"] == noise_model)
    & (df["qubits"] == qubits)
    & (df["noise_probability"] == noise_probability)
]

fig_depth = px.line(
    depth_data,
    x="depth",
    y="mean_success",
    markers=True,
    labels={
        "depth": "Circuit Depth",
        "mean_success": "Mean Success Probability"
    },
    title=(
        f"{noise_model.replace('_', ' ').title()} "
        f"— {qubits} Qubits, "
        f"Noise {noise_probability:.3f}"
    )
)

fig_depth.update_yaxes(
    tickformat=".0%",
    range=[0, 1]
)

fig_depth.update_xaxes(
    type="category"
)

fig_depth.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_depth,
    use_container_width=True
)