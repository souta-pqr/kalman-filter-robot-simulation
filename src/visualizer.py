import matplotlib.pyplot as plt


def plot_position(positions, save_path=None):
    """
    ロボットの位置をプロット

    Parameters
    ----------
    positions : list
        位置のリスト
    save_path : str, optional
        保存先のパス
    """
    steps = range(len(positions))

    plt.figure(figsize=(10, 6))
    plt.plot(steps, positions, "bo-", label="Robot Position", linewidth=2, markersize=6)

    plt.xlabel("Time Step")
    plt.ylabel("Position (m)")
    plt.title("1D Robot Movement")
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    plt.show()


def plot_with_observations(true_positions, observations, save_path=None):
    """
    真の位置と観測値を比較

    Parameters
    ----------
    true_positions : list
        真の位置のリスト
    observations : list
        観測値のリスト
    save_path : str, optional
        保存先のパス
    """
    steps = range(len(true_positions))

    plt.figure(figsize=(10, 6))
    plt.plot(steps, true_positions, "g-", label="True Position", linewidth=2)
    plt.plot(steps, observations, "rx", label="Observations", markersize=8, alpha=0.6)

    plt.xlabel("Time Step")
    plt.ylabel("Position (m)")
    plt.title("Robot Position with Sensor Noise")
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    plt.show()


def plot_with_estimates(true_positions, observations, estimates, save_path=None):
    """
    真の位置、観測値、推定値を比較

    Parameters
    ----------
    true_positions : list
        真の位置のリスト
    observations : list
        観測値のリスト
    estimates : list
        推定値のリスト
    save_path : str, optional
        保存先のパス
    """
    steps = range(len(true_positions))

    plt.figure(figsize=(10, 6))
    plt.plot(steps, true_positions, "g-", label="True Position", linewidth=2)
    plt.plot(steps, observations, "rx", label="Observations", markersize=8, alpha=0.5)
    plt.plot(steps, estimates, "b-", label="Estimates", linewidth=2)

    plt.xlabel("Time Step")
    plt.ylabel("Position (m)")
    plt.title("Position Estimation")
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    plt.show()


def plot_kalman_gain(kalman_gains, save_path=None):
    """
    カルマンゲインの推移を表示

    Parameters
    ----------
    kalman_gains : list
        カルマンゲインのリスト
    save_path : str, optional
        保存先のパス
    """
    steps = range(len(kalman_gains))

    plt.figure(figsize=(10, 5))
    plt.plot(steps, kalman_gains, "r-", linewidth=2, marker="o")

    plt.xlabel("Time Step")
    plt.ylabel("Kalman Gain")
    plt.title("Kalman Gain over Time")
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    plt.show()


def plot_parameter_comparison(true_positions, observations, estimates_dict, save_path=None):
    """
    複数のパラメータ設定での推定結果を比較

    Parameters
    ----------
    true_positions : list
        真の位置のリスト
    observations : list
        観測値のリスト
    estimates_dict : dict
        {ラベル: (推定値, エラー)} の辞書
    save_path : str, optional
        保存先のパス
    """
    steps = range(len(true_positions))
    colors = ["b", "m", "c", "orange", "purple"]
    linestyles = ["-", "--", "-.", ":", "-"]

    plt.figure(figsize=(12, 6))
    plt.plot(steps, true_positions, "g-", label="True Position", linewidth=2)
    plt.plot(steps, observations, "rx", label="Observations", markersize=8, alpha=0.5)

    for i, (label, (estimates, error)) in enumerate(estimates_dict.items()):
        plt.plot(
            steps,
            estimates,
            color=colors[i % len(colors)],
            linestyle=linestyles[i % len(linestyles)],
            label=f"{label} (error={error:.3f})",
            linewidth=2,
        )

    plt.xlabel("Time Step")
    plt.ylabel("Position (m)")
    plt.title("Effect of Q and R Parameters on Kalman Filter")
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    plt.show()

    plt.show()
