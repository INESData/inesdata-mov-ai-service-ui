# -*- coding: utf-8 -*-
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def add(first_term: int, second_term: int) -> int:
    """Función para sumar dos números.

    Args:
        first_term (int): primer número
        second_term (int): seguno número

    Returns: devuelve la suma de first_term + second_term

    """
    return first_term + second_term
