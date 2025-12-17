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
    plt.plot(steps, positions, 'bo-', label='Robot Position', linewidth=2, markersize=6)
    
    plt.xlabel('Time Step')
    plt.ylabel('Position (m)')
    plt.title('1D Robot Movement')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
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
    plt.plot(steps, true_positions, 'g-', label='True Position', linewidth=2)
    plt.plot(steps, observations, 'rx', label='Observations', markersize=8, alpha=0.6)
    
    plt.xlabel('Time Step')
    plt.ylabel('Position (m)')
    plt.title('Robot Position with Sensor Noise')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
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
    plt.plot(steps, true_positions, 'g-', label='True Position', linewidth=2)
    plt.plot(steps, observations, 'rx', label='Observations', markersize=8, alpha=0.5)
    plt.plot(steps, estimates, 'b-', label='Estimates (Average)', linewidth=2)
    
    plt.xlabel('Time Step')
    plt.ylabel('Position (m)')
    plt.title('Position Estimation using Average')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()
    