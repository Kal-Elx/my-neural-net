from enum import Enum
import numpy as np
from typing import List, Tuple, Callable
from random import shuffle
import pickle
import warnings
import time


class ActivationFunction(Enum):
    SIGMOID = 1
    TANH = 2
    LINEAR = 3


def get_activation_func(activation_func: ActivationFunction) -> Tuple[Callable, Callable]:
    """
    Returns the corresponding activation function and its derivative for the given enum.
    :param activation_func: Desired activation function.
    :return: Tuple of desired activation function and its derivative.
    """
    if activation_func == ActivationFunction.SIGMOID:
        return sigmoid, sigmoid_prime
    elif activation_func == ActivationFunction.TANH:
        return np.tanh, tanh_prime
    elif activation_func == ActivationFunction.LINEAR:
        return linear, linear_prime


class CostFunction(Enum):
    QUADRATIC_COST = 1
    CROSS_ENTROPY = 2


def get_cost_func(cost_func: CostFunction) -> Tuple[Callable, Callable]:
    """
    Returns the corresponding cost function and its derivative for the given enum.
    :param cost_func: Desired cost function.
    :return: Tuple of desired activation function and its derivative.
    """
    if cost_func == CostFunction.QUADRATIC_COST:
        return quadratic_cost, quadratic_cost_prime
    elif cost_func == CostFunction.CROSS_ENTROPY:
        return cross_entropy, cross_entropy_prime


class RegularizationTechnique(Enum):
    L1 = 1
    L2 = 2


def get_regularization_technique(regularization_technique: RegularizationTechnique) -> Callable:
    """
    Returns a corresponding function for the given enum.
    :param regularization_technique: Desired regularization technique.
    :return: Desired regularization function.
    """
    if regularization_technique == None:
        return no_regularization_technique
    elif regularization_technique == RegularizationTechnique.L1:
        return L1
    elif regularization_technique == RegularizationTechnique.L2:
        return L2


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def sigmoid_prime(x: float) -> float:
    return sigmoid(x) * (1 - sigmoid(x))


def tanh_prime(x: float) -> float:
    return (1 - np.tanh(x) ** 2)


def linear(x: float) -> float:
    return x


def linear_prime(x: float) -> float:
    return 1


def quadratic_cost(a: float, y: float) -> float:
    return (1.0 / 2.0) * np.linalg.norm(a - y) ** 2


def quadratic_cost_prime(a: np.ndarray, y: np.ndarray) -> np.ndarray:
    return a - y


def cross_entropy(a: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.sum(np.nan_to_num(-y * np.log(a) - (1 - y) * np.log(1 - a)))


def cross_entropy_prime(a: np.ndarray, y: np.ndarray) -> np.ndarray:
    return a - y


def no_ol_act_func_prime(arg):
    """
    Used in Equation 1 in backpropagation when the cost function is cross-entropy.
    :param arg: Arbitrary argument.
    :return: 1 (the multiplication property).
    """
    return 1


def no_regularization_technique(w: float) -> float:
    return 0.0


def L1(w: float) -> float:
    return np.sign(w)


def L2(w: float) -> float:
    return w


def rescale(curr_min: float, curr_max: float, new_min: float, new_max: float, x: float) -> float:
    """
    Rescales a value to a new interval. Used for rescaling values in data sets.
    :param curr_min: The current minimum value in the data set.
    :param curr_max: The current maximum value in the data set.
    :param new_min: The new minimum value in the data set.
    :param new_max: The new maximum value in the data set.
    :param x: Value to rescale.
    :return: x rescaled.
    """
    return ((x - curr_min) * ((new_max - new_min) / (curr_max - curr_min))) + new_min