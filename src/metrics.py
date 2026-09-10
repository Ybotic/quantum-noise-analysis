def calculate_success_probability(counts, expected_state):
    """
    Calculate the probability of measuring the expected state.
    """

    total_shots = sum(counts.values())
    successful_shots = counts.get(expected_state, 0)

    return successful_shots / total_shots


def get_ideal_distribution(counts):
    """
    Convert measurement counts into probabilities.
    """

    total_shots = sum(counts.values())

    return {
        state: count / total_shots
        for state, count in counts.items()
    }


def calculate_distribution_fidelity(ideal_counts, noisy_counts):
    """
    Calculate classical fidelity between ideal and noisy
    measurement probability distributions.

    Fidelity = (sum sqrt(P_i * Q_i))^2
    """

    ideal = get_ideal_distribution(ideal_counts)
    noisy = get_ideal_distribution(noisy_counts)

    all_states = set(ideal) | set(noisy)

    fidelity = sum(
        (ideal.get(state, 0) * noisy.get(state, 0)) ** 0.5
        for state in all_states
    ) ** 2

    return fidelity