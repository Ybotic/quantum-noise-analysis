def calculate_success_probability(counts, expected_state):
    total_shots = sum(counts.values())

    if total_shots == 0:
        return 0.0

    successful_shots = counts.get(expected_state, 0)

    return successful_shots / total_shots


def calculate_error_rate(success_probability):
    return 1 - success_probability


def get_probability_distribution(counts):
    total_shots = sum(counts.values())

    if total_shots == 0:
        return {}

    return {
        state: count / total_shots
        for state, count in counts.items()
    }


def calculate_distribution_fidelity(
    ideal_counts,
    noisy_counts
):
    ideal = get_probability_distribution(
        ideal_counts
    )

    noisy = get_probability_distribution(
        noisy_counts
    )

    all_states = set(ideal) | set(noisy)

    fidelity = sum(
        (
            ideal.get(state, 0)
            * noisy.get(state, 0)
        ) ** 0.5
        for state in all_states
    ) ** 2

    return fidelity


def calculate_metrics(
    ideal_counts,
    noisy_counts,
    expected_state
):
    success_probability = calculate_success_probability(
        noisy_counts,
        expected_state
    )

    error_rate = calculate_error_rate(
        success_probability
    )

    fidelity = calculate_distribution_fidelity(
        ideal_counts,
        noisy_counts
    )

    return {
        "success_probability": success_probability,
        "error_rate": error_rate,
        "fidelity": fidelity
    }