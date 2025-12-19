import matplotlib.pyplot as plt


def plot_trajectory(states, title="Robot Trajectory"):
    """ロボットの軌跡をプロット"""
    plt.figure(figsize=(8, 8))
    plt.plot(states[:, 0], states[:, 1], "g-", linewidth=2, label="Path")
    plt.plot(states[0, 0], states[0, 1], "go", markersize=10, label="Start")
    plt.plot(states[-1, 0], states[-1, 1], "rs", markersize=10, label="End")

    plt.xlabel("X Position (m)", fontsize=12)
    plt.ylabel("Y Position (m)", fontsize=12)
    plt.title(title, fontsize=14, fontweight="bold")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis("equal")
    plt.show()


def plot_with_observations(true_states, observations, title="Robot Trajectory with Observations"):
    """真の軌跡と観測値をプロット"""
    plt.figure(figsize=(10, 8))

    plt.plot(true_states[:, 0], true_states[:, 1], "g-", linewidth=2.5, label="True Path")
    plt.plot(
        observations[:, 0], observations[:, 1], "rx", markersize=6, alpha=0.6, label="Observations"
    )
    plt.plot(true_states[0, 0], true_states[0, 1], "go", markersize=12, label="Start")
    plt.plot(true_states[-1, 0], true_states[-1, 1], "rs", markersize=12, label="End")

    plt.xlabel("X Position (m)", fontsize=12)
    plt.ylabel("Y Position (m)", fontsize=12)
    plt.title(title, fontsize=14, fontweight="bold")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis("equal")
    plt.show()


def plot_with_estimates(true_states, observations, estimates, title="EKF Estimation"):
    """真の軌跡、観測値、推定値をプロット"""
    plt.figure(figsize=(12, 8))

    plt.plot(true_states[:, 0], true_states[:, 1], "g-", linewidth=2.5, label="True Path")
    plt.plot(
        observations[:, 0], observations[:, 1], "rx", markersize=6, alpha=0.5, label="Observations"
    )
    plt.plot(estimates[:, 0], estimates[:, 1], "b-", linewidth=2, label="EKF Estimate")
    plt.plot(true_states[0, 0], true_states[0, 1], "go", markersize=12, label="Start")
    plt.plot(true_states[-1, 0], true_states[-1, 1], "rs", markersize=12, label="End")

    plt.xlabel("X Position (m)", fontsize=12)
    plt.ylabel("Y Position (m)", fontsize=12)
    plt.title(title, fontsize=14, fontweight="bold")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis("equal")
    plt.show()
