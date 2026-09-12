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

st.divider()

st.subheader("Success Probability vs Number of Qubits")

qubit_data = df[
    (df["noise_model"] == noise_model)
    & (df["depth"] == depth)
    & (df["noise_probability"] == noise_probability)
]

fig_qubits = px.line(
    qubit_data,
    x="qubits",
    y="mean_success",
    markers=True,
    labels={
        "qubits": "Number of Qubits",
        "mean_success": "Mean Success Probability"
    },
    title=(
        f"{noise_model.replace('_', ' ').title()} "
        f"— Depth {depth}, "
        f"Noise {noise_probability:.3f}"
    )
)

fig_qubits.update_yaxes(
    tickformat=".0%",
    range=[0, 1]
)

fig_qubits.update_xaxes(
    dtick=1
)

fig_qubits.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_qubits,
    use_container_width=True
)

st.divider()

st.subheader("Noise Model Comparison")

comparison_data = df[
    (df["qubits"] == qubits)
    & (df["depth"] == depth)
    & (df["noise_probability"] == noise_probability)
]

fig_comparison = px.bar(
    comparison_data,
    x="noise_model",
    y="mean_success",
    labels={
        "noise_model": "Noise Model",
        "mean_success": "Mean Success Probability"
    },
    title=(
        f"Noise Model Comparison — "
        f"{qubits} Qubits, Depth {depth}, "
        f"Noise {noise_probability:.3f}"
    )
)

fig_comparison.update_yaxes(
    tickformat=".0%",
    range=[0, 1]
)

fig_comparison.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_comparison,
    use_container_width=True
)

st.divider()

st.subheader("Fidelity vs Circuit Depth")

fidelity_data = df[
    (df["noise_model"] == noise_model)
    & (df["qubits"] == qubits)
    & (df["noise_probability"] == noise_probability)
]

fig_fidelity = px.line(
    fidelity_data,
    x="depth",
    y="mean_fidelity",
    markers=True,
    labels={
        "depth": "Circuit Depth",
        "mean_fidelity": "Mean Fidelity"
    },
    title=(
        f"{noise_model.replace('_', ' ').title()} "
        f"— {qubits} Qubits, "
        f"Noise {noise_probability:.3f}"
    )
)

fig_fidelity.update_yaxes(
    tickformat=".0%",
    range=[0, 1]
)

fig_fidelity.update_xaxes(
    type="category"
)

fig_fidelity.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_fidelity,
    use_container_width=True
)

st.divider()

st.subheader("Depth × Noise Strength")

heatmap_data = df[
    (df["noise_model"] == noise_model)
    & (df["qubits"] == qubits)
]

heatmap = heatmap_data.pivot(
    index="depth",
    columns="noise_probability",
    values="mean_success"
)

fig_heatmap = px.imshow(
    heatmap,
    labels={
        "x": "Noise Strength",
        "y": "Circuit Depth",
        "color": "Mean Success Probability"
    },
    x=heatmap.columns,
    y=heatmap.index,
    text_auto=".1%",
    aspect="auto",
    title=(
        f"{noise_model.replace('_', ' ').title()} "
        f"— {qubits} Qubits"
    )
)

fig_heatmap.update_xaxes(
    tickformat=".3f"
)

fig_heatmap.update_yaxes(
    dtick=1
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

st.divider()

st.subheader("Success Probability with Uncertainty")

error_data = df[
    (df["noise_model"] == noise_model)
    & (df["qubits"] == qubits)
]

fig_error = px.line(
    error_data,
    x="noise_probability",
    y="mean_success",
    error_y="success_ci",
    markers=True,
    labels={
        "noise_probability": "Noise Strength",
        "mean_success": "Mean Success Probability"
    },
    title=(
        f"{noise_model.replace('_', ' ').title()} "
        f"— {qubits} Qubits"
    )
)

fig_error.update_yaxes(
    tickformat=".0%",
    range=[0, 1]
)

fig_error.update_xaxes(
    tickformat=".3f"
)

fig_error.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_error,
    use_container_width=True
)

st.divider()

st.subheader("Measurement Outcome Distribution")

if "result" in st.session_state:

    counts = st.session_state["result"]["counts"]

    st.write("DEBUG COUNTS:", counts)

    if counts:

        outcome_data = pd.DataFrame(
            {
                "Outcome": list(counts.keys()),
                "Count": list(counts.values())
            }
        )

        fig_outcomes = px.bar(
            outcome_data,
            x="Outcome",
            y="Count",
            labels={
                "Outcome": "Measured State",
                "Count": "Number of Shots"
            },
            title="Measured Quantum States"
        )

        fig_outcomes.update_layout(
            xaxis_type="category"
        )

        st.plotly_chart(
            fig_outcomes,
            use_container_width=True
        )

    else:

        st.info("No measurement data available.")

else:

    st.info(
        "Run an experiment to see measurement outcomes."
    )

# -------------------------
# Statistical Summary
# -------------------------

st.divider()

st.subheader("Statistical Summary")

summary_data = df[
    (df["noise_model"] == noise_model)
    & (df["qubits"] == qubits)
    & (df["depth"] == depth)
    & (df["noise_probability"] == noise_probability)
]

if not summary_data.empty:

    summary = summary_data.iloc[0]

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Mean Success",
        f"{summary['mean_success']:.2%}"
    )

    col2.metric(
        "Std. Deviation",
        f"{summary['std_success']:.2%}"
    )

    col3.metric(
        "95% CI",
        f"±{summary['success_ci']:.2%}"
    )

    col4.metric(
        "Mean Error Rate",
        f"{summary['mean_error_rate']:.2%}"
    )

    col5.metric(
        "Mean Fidelity",
        f"{summary['mean_fidelity']:.2%}"
    )

st.divider()

st.subheader("Statistical Summary")

summary_data = df[
    (df["noise_model"] == noise_model)
    & (df["qubits"] == qubits)
    & (df["depth"] == depth)
    & (df["noise_probability"] == noise_probability)
]

if not summary_data.empty:

    summary = summary_data.iloc[0]

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Mean Success",
        f"{summary['mean_success']:.2%}"
    )

    col2.metric(
        "Std. Deviation",
        f"{summary['std_success']:.2%}"
    )

    col3.metric(
        "95% CI",
        f"±{summary['success_ci']:.2%}"
    )

    col4.metric(
        "Mean Error Rate",
        f"{summary['mean_error_rate']:.2%}"
    )

    col5.metric(
        "Mean Fidelity",
        f"{summary['mean_fidelity']:.2%}"
    )

st.divider()

st.subheader("Noise Sensitivity")

sensitivity_data = df[
    (df["noise_model"] == noise_model)
    & (df["qubits"] == qubits)
    & (df["depth"] == depth)
].copy()

if not sensitivity_data.empty:

    baseline = sensitivity_data[
        sensitivity_data["noise_probability"] == 0
    ]["mean_success"].iloc[0]

    sensitivity_data["performance_loss"] = (
        baseline - sensitivity_data["mean_success"]
    )

    fig_sensitivity = px.line(
        sensitivity_data,
        x="noise_probability",
        y="performance_loss",
        markers=True,
        labels={
            "noise_probability": "Noise Strength",
            "performance_loss": "Performance Loss"
        },
        title=(
            f"{noise_model.replace('_', ' ').title()} "
            f"— Performance Loss"
        )
    )

    fig_sensitivity.update_yaxes(
        tickformat=".0%",
        range=[0, 1]
    )

    fig_sensitivity.update_xaxes(
        tickformat=".3f"
    )

    fig_sensitivity.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_sensitivity,
        use_container_width=True
    )

st.divider()

st.subheader("Overall Noise Model Ranking")

ranking_data = pd.read_csv(
    "results/processed/noise_model_comparison_results.csv"
)

ranking_data = ranking_data.sort_values(
    "mean_success",
    ascending=False
)

fig_ranking = px.bar(
    ranking_data,
    x="noise_model",
    y="mean_success",
    labels={
        "noise_model": "Noise Model",
        "mean_success": "Average Success Probability"
    },
    title="Average Performance Across Experimental Conditions"
)

fig_ranking.update_yaxes(
    tickformat=".0%",
    range=[0, 1]
)

fig_ranking.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_ranking,
    use_container_width=True
)

st.subheader("Noise Model Performance")

table_data = ranking_data[
    ["noise_model", "mean_success"]
].copy()

table_data["noise_model"] = (
    table_data["noise_model"]
    .str.replace("_", " ")
    .str.title()
)

table_data["mean_success"] = (
    table_data["mean_success"] * 100
)

table_data = table_data.rename(
    columns={
        "noise_model": "Noise Model",
        "mean_success": "Average Success (%)"
    }
)

st.dataframe(
    table_data,
    hide_index=True,
    use_container_width=True
)