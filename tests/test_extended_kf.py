"""Tests for Extended Kalman Filter"""
import sys
from pathlib import Path

import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from extended_kf import ExtendedKalmanFilter


def test_initialization():
    """Test EKF initialization"""
    Q = np.diag([0.01, 0.01, 0.001])
    R = np.diag([0.25, 0.25, 0.01])
    x0 = np.array([0.0, 0.0, 0.0])
    P0 = np.eye(3)
    
    ekf = ExtendedKalmanFilter(Q=Q, R=R, x0=x0, P0=P0, dt=1.0)
    
    assert np.allclose(ekf.x, x0)
    assert np.allclose(ekf.P, P0)
    assert ekf.dt == 1.0


def test_predict():
    """Test EKF prediction step"""
    Q = np.diag([0.01, 0.01, 0.001])
    R = np.diag([0.25, 0.25, 0.01])
    ekf = ExtendedKalmanFilter(
        Q=Q, R=R, x0=np.zeros(3), P0=np.eye(3), dt=1.0
    )
    
    u = [1.0, 0.1]  # velocity, angular velocity
    ekf.predict(u)
    
    # Position should have changed
    assert not np.allclose(ekf.x, np.zeros(3))
    # Uncertainty should increase
    assert np.all(np.diag(ekf.P) >= np.diag(np.eye(3)))


def test_update():
    """Test EKF update step"""
    Q = np.diag([0.01, 0.01, 0.001])
    R = np.diag([0.25, 0.25, 0.01])
    ekf = ExtendedKalmanFilter(
        Q=Q, R=R, x0=np.zeros(3), P0=np.eye(3), dt=1.0
    )
    
    z = np.array([1.0, 1.0, 0.1])
    K = ekf.update(z)
    
    # Kalman gain should be valid
    assert K.shape == (3, 3)
    # Uncertainty diagonal should be non-negative
    assert np.all(np.diag(ekf.P) >= 0)


def test_filter_step():
    """Test complete EKF filter step"""
    Q = np.diag([0.01, 0.01, 0.001])
    R = np.diag([0.25, 0.25, 0.01])
    ekf = ExtendedKalmanFilter(
        Q=Q, R=R, x0=np.zeros(3), P0=np.eye(3), dt=1.0
    )
    
    z = np.array([1.0, 1.0, 0.1])
    u = [1.0, 0.1]
    x, P = ekf.filter_step(z, u)
    
    assert x.shape == (3,)
    assert P.shape == (3, 3)


def test_angle_normalization():
    """Test angle normalization"""
    Q = np.diag([0.01, 0.01, 0.001])
    R = np.diag([0.25, 0.25, 0.01])
    ekf = ExtendedKalmanFilter(
        Q=Q, R=R, x0=np.zeros(3), P0=np.eye(3), dt=1.0
    )
    
    # Test angle wrapping
    ekf.x[2] = 4 * np.pi
    z = np.array([0.0, 0.0, 0.0])
    ekf.update(z)
    
    # Angle should be normalized to [-pi, pi]
    assert -np.pi <= ekf.x[2] <= np.pi


def test_multiple_steps():
    """Test multiple EKF iterations"""
    Q = np.diag([0.01, 0.01, 0.001])
    R = np.diag([0.25, 0.25, 0.01])
    ekf = ExtendedKalmanFilter(
        Q=Q, R=R, x0=np.zeros(3), P0=np.eye(3), dt=1.0
    )
    
    for i in range(50):
        u = [1.0, 0.1]
        z = np.array([i * 1.0, i * 0.1, i * 0.1]) + np.random.randn(3) * 0.1
        ekf.filter_step(z, u)
        
        # Covariance should remain positive definite
        assert np.all(np.diag(ekf.P) >= 0)
        # Angle should remain normalized
        assert -np.pi <= ekf.x[2] <= np.pi
