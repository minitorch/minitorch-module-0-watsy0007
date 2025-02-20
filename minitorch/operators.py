"""Collection of the core mathematical operators used throughout the code base."""

import math

# ## Task 0.1
from typing import Callable, Iterable

#
# Implementation of a prelude of elementary functions.

# Mathematical functions:
# - mul
# - id
# - add
# - neg
# - lt
# - eq
# - max
# - is_close
# - sigmoid
# - relu
# - log
# - exp
# - log_back
# - inv
# - inv_back
# - relu_back
#
# For sigmoid calculate as:
# $f(x) =  \frac{1.0}{(1.0 + e^e-x})}$ if x >=0 else $\frac{e^x}{(1.0 + e^{x})}$
# For is_close:
# $f(x) = |x - y| < 1e-2$


def mul(x: float, y: float) -> float:
    """$f(x, y) = x * y$"""
    return x * y


def id(x: float) -> float:
    """$f(x) = x$"""
    return x


def add(x: float, y: float) -> float:
    """$f(x, y) = x + y$"""
    return x + y


def neg(x: float) -> float:
    """$f(x) = -x$"""
    return -x


def lt(x: float, y: float) -> float:
    """$f(x) =$ 1.0 if x is less than y else 0.0"""
    if x < y:
        return 1.0
    return 0.0


def eq(x: float, y: float) -> float:
    """$f(x) =$ 1.0 if x is equal to y else 0.0"""
    return x == y


def max(x: float, y: float) -> float:
    """$f(x) =$ x if x is greater than y else y"""
    if x > y:
        return x
    return y


def is_close(x: float, y: float) -> bool:
    """$f(x) = |x - y| < 1e-2$"""
    return math.isclose(x, y, rel_tol=1e-2, abs_tol=1e-8)


def sigmoid(x: float) -> float:
    r"""$f(x) =  \frac{1.0}{(1.0 + e^{-x})}$

    (See https://en.wikipedia.org/wiki/Sigmoid_function )

    Calculate as

    $f(x) =  \frac{1.0}{(1.0 + e^{-x})}$ if x >=0 else $\frac{e^x}{(1.0 + e^{x})}$

    for stability.
    """
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-1.0 * x))
    return math.exp(x) / (1.0 + math.exp(x))


def relu(x: float) -> float:
    """$f(x) =$ x if x is greater than 0, else 0

    (See https://en.wikipedia.org/wiki/Rectifier_(neural_networks) .)
    """
    if x > 0:
        return x
    return 0.0


EPS = 1e-6


def log(x: float) -> float:
    """$f(x) = log(x)$"""
    return math.log(x + EPS)


def exp(x: float) -> float:
    """$f(x) = e^{x}$"""
    return math.exp(x)


def log_back(x: float, d: float) -> float:
    r"""If $f = log$ as above, compute $d \times f'(x)$"""
    if x <= 0:
        raise ValueError("x must be positive")
    return 1.0 / x * d


def inv(x: float) -> float:
    """$f(x) = 1/x$"""
    return 1.0 / x


def inv_back(x: float, d: float) -> float:
    r"""If $f(x) = 1/x$ compute $d \times f'(x)$"""
    return -1.0 / (x**2) * d


def relu_back(x: float, d: float) -> float:
    r"""If $f = relu$ compute $d \times f'(x)$"""
    if x > 0:
        return d * 1.0
    return 0.0


# ## Task 0.3

# Small practice library of elementary higher-order functions.

# Implement the following core functions
# - map
# - zipWith
# - reduce
#
# Use these to implement
# - negList : negate a list
# - addLists : add two lists together
# - sum: sum lists
# - prod: take the product of lists


# TODO: Implement for Task 0.3.


def map(fn: Callable[[float], float]) -> Callable[[Iterable[float]], Iterable[float]]:
    """Higher-order map.

    See https://en.wikipedia.org/wiki/Map_(higher-order_function)

    Args:
        fn: Function from one value to one value.

    Returns:
         A function that takes a list, applies `fn` to each element, and returns a
         new list

    """

    def wrapper(ls: Iterable[float]) -> Iterable[float]:
        for x in ls:
            yield fn(x)

    return wrapper


def negList(ls: Iterable[float]) -> Iterable[float]:
    """Use `map` and `neg` to negate each element in `ls`"""
    return map(neg)(ls)


def zipWith(
    fn: Callable[[float, float], float],
) -> Callable[[Iterable[float], Iterable[float]], Iterable[float]]:
    """Higher-order zipwith (or map2).

    See https://en.wikipedia.org/wiki/Map_(higher-order_function)

    Args:
        fn: combine two values

    Returns:
         Function that takes two equally sized lists `ls1` and `ls2`, produce a new list by
         applying fn(x, y) on each pair of elements.

    """

    def wrapper(ls1: Iterable[float], ls2: Iterable[float]) -> Iterable[float]:
        for x, y in zip(ls1, ls2):
            yield fn(x, y)

    return wrapper


def addLists(ls1: Iterable[float], ls2: Iterable[float]) -> Iterable[float]:
    """Add the elements of `ls1` and `ls2` using `zipWith` and `add`"""
    return zipWith(add)(ls1, ls2)


def reduce(
    fn: Callable[[float, float], float], start: float
) -> Callable[[Iterable[float]], float]:
    r"""Higher-order reduce.

    Args:
        fn: combine two values
        start: start value $x_0$

    Returns:
         Function that takes a list `ls` of elements
         $x_1 \ldots x_n$ and computes the reduction :math:`fn(x_3, fn(x_2,
         fn(x_1, x_0)))`

    """

    def wrapper(ls: Iterable[float]) -> float:
        acc = start
        for x in ls:
            acc = fn(acc, x)
        return acc

    return wrapper


def sum(ls: Iterable[float]) -> float:
    """Sum up a list using `reduce` and `add`."""
    return reduce(add, 0.0)(ls)


def prod(ls: Iterable[float]) -> float:
    """Product of a list using `reduce` and `mul`."""
    return reduce(mul, 1.0)(ls)
