def add(
    a: int,
    b: int,
) -> int:
    """
    >>> add(2, 7)
    9
    >>> add(3, -1)
    2
    """
    sum = a + b
    # sum *= -1  # アンコメントすることでテストが失敗するようになる
    return sum


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
