"""
Common loss functions for algorithms used in this workspace.
Includes examples for linear regression, logistic regression, KNN (zero-one loss),
and helpers for regularized losses and gradients used in gradient descent.
"""

import numpy as np
from typing import Optional


def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean squared error (MSE).

    Formula: MSE = (1/n) * sum_i (y_i - yhat_i)^2

    Working: measures average squared difference between true and predicted values.
    Sensitive to outliers because errors are squared.

    y_true, y_pred: shape (n_samples,)
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return float(np.mean((y_true - y_pred) ** 2))


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root mean squared error (RMSE).

    Formula: RMSE = sqrt(MSE)

    Working: same units as target; penalizes larger errors more strongly.
    """
    return float(np.sqrt(mse(y_true, y_pred)))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean absolute error (MAE).

    Formula: MAE = (1/n) * sum_i |y_i - yhat_i|

    Working: average absolute difference; more robust to outliers than MSE.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return float(np.mean(np.abs(y_true - y_pred)))


def mse_gradient(X: np.ndarray, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """Gradient of MSE w.r.t. linear model weights (no bias term).

    If predictions = X @ w, then
    gradient = (2/n) * X^T (X w - y)

    X shape: (n_samples, n_features), predictions = X @ w
    Returns gradient shape (n_features,)
    """
    n = X.shape[0]
    return (2.0 / n) * X.T @ (y_pred - y_true)


def binary_cross_entropy(y_true: np.ndarray, y_prob: np.ndarray, eps: float = 1e-15) -> float:
    """Binary cross-entropy / log loss.

    Formula: -(1/n) * sum_i [ y_i * log(p_i) + (1 - y_i) * log(1 - p_i) ]

    Working: penalizes confident wrong predictions heavily. Used for binary
    logistic regression where `p` is predicted probability for class 1.
    """
    y_true = np.asarray(y_true)
    p = np.clip(np.asarray(y_prob), eps, 1 - eps)
    return float(-np.mean(y_true * np.log(p) + (1 - y_true) * np.log(1 - p)))


def multiclass_cross_entropy(y_true: np.ndarray, y_prob: np.ndarray, eps: float = 1e-15) -> float:
    """Multiclass cross-entropy (categorical cross-entropy).

    Formula: -(1/n) * sum_i log p_{i, y_i}

    y_true: integer labels shape (n,)
    y_prob: array shape (n, n_classes) with predicted probabilities
    Working: generalization of binary log-loss; high penalty for low prob
    assigned to the true class.
    """
    y_true = np.asarray(y_true).astype(int)
    p = np.clip(np.asarray(y_prob), eps, 1 - eps)
    idx = (np.arange(p.shape[0]), y_true)
    return float(-np.mean(np.log(p[idx])))


def zero_one_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Zero-one loss (classification error).

    Formula: (1/n) * sum_i I[y_i != yhat_i]

    Working: simple discrete loss equal to 1 - accuracy; non-differentiable,
    typically used for evaluation only (not optimization).
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return float(np.mean(y_true != y_pred))


def hinge_loss(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Hinge loss used by support vector machines (SVM).

    Formula: (1/n) * sum_i max(0, 1 - y_i * s_i), where y_i in {-1,+1} and
    s_i is the raw score (w^T x + b).

    Working: encourages margin >= 1 for correct classifications; zero loss
    when margin is satisfied. Convex but not differentiable at margin = 1.
    """
    y_true = np.asarray(y_true)
    margins = 1 - y_true * y_score
    return float(np.mean(np.maximum(0, margins)))


def l2_regularized_mse(y_true: np.ndarray, y_pred: np.ndarray, w: np.ndarray, alpha: float) -> float:
    """MSE with L2 regularization (ridge).

    Formula: MSE + alpha * ||w||_2^2

    Working: adds penalty on weight magnitude to reduce overfitting; alpha
    (regularization strength) trades off bias vs variance.
    """
    return mse(y_true, y_pred) + float(alpha) * float(np.sum(w ** 2))


# --- Examples / quick demos -------------------------------------------------
if __name__ == "__main__":
    # Linear regression example
    print("--- Linear regression losses ---")
    y_true = np.array([3.0, -0.5, 2.0, 7.0])
    y_pred = np.array([2.5, 0.0, 2.1, 7.8])
    print("MSE:", mse(y_true, y_pred))
    print("RMSE:", rmse(y_true, y_pred))
    print("MAE:", mae(y_true, y_pred))

    # Gradient example for linear model y = X @ w
    X = np.array([[1.0, 2.0], [1.0, -1.0], [2.0, 0.5], [0.0, 1.0]])
    w = np.array([0.5, 1.0])
    y_pred_lin = X @ w
    print("MSE grad:", mse_gradient(X, y_true, y_pred_lin))

    # Logistic regression example (binary)
    print("\n--- Logistic regression losses ---")
    # simple logistic sigmoid
    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    y_true_bin = np.array([0, 1, 1, 0])
    scores = np.array([-1.2, 2.0, 0.8, -0.5])
    probs = sigmoid(scores)
    print("Binary cross-entropy:", binary_cross_entropy(y_true_bin, probs))

    # Multiclass example
    print("\n--- Multiclass cross-entropy ---")
    y_true_multi = np.array([0, 2, 1])
    y_prob = np.array([[0.7, 0.2, 0.1], [0.1, 0.2, 0.7], [0.2, 0.6, 0.2]])
    print("Multiclass CE:", multiclass_cross_entropy(y_true_multi, y_prob))

    # KNN / classification example (zero-one loss)
    print("\n--- Classification (zero-one) ---")
    y_true_cls = np.array([0, 1, 1, 2, 2])
    y_pred_cls = np.array([0, 1, 0, 2, 2])
    print("Zero-one loss (1 - accuracy):", zero_one_loss(y_true_cls, y_pred_cls))

    # Hinge loss example (binary labels -1/+1)
    print("\n--- Hinge loss ---")
    y_true_h = np.array([1, -1, 1, -1])
    y_score_h = np.array([2.0, -0.5, 0.2, -1.0])
    print("Hinge loss:", hinge_loss(y_true_h, y_score_h))

    # Regularized loss example
    print("\n--- Regularized MSE ---")
    print("L2 regularized MSE:", l2_regularized_mse(y_true, y_pred, w, alpha=0.1))
