import pytest

from terrain import erosion as mod

CASES = [
    ('normalize_neighborhood', [[1, 1, 2]], [0.25, 0.25, 0.5], True),
    ('normalize_neighborhood', [[0, 0, 0]], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], True),
    ('rainfall_to_unit', [[0, 127.5, 255, -5, 300]], [0.0, 0.5, 1.0, 0.0, 1.0], True),
    ('enforce_min_slope', [[10, 5, 9, 0], 3], [10, 7, 9, 6], False),
    ('enforce_min_slope', [[2, 2, 2], 1], [2, 2, 2], False),
    ('split_sediment', [100, [1, 3]], [25.0, 75.0], True),
    ('split_sediment', [9, [0, 0]], [4.5, 4.5], True),
    ('align_tile_seam', [[1, 2], [4, 8]], ([1, 3.0], [3.0, 8]), False),
    ('recompute_normals', [[0, 2, 5]], [2, 3], False),
    ('fill_basins', [[5, 1, 5]], [5, 5, 5], False),
    ('fill_basins', [[3, 0, 3, 0, 3]], [3, 3, 3, 3, 3], False),
    ('clamp_erosion', [5, 2], 2, False),
    ('clamp_erosion', [-5, 2], -2, False),
    ('cache_is_fresh', ['v1', 'v1'], True, False),
    ('commit_tiles', [[True, False]], False, False),
]


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_erosion_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert result == pytest.approx(expected)
    else:
        assert result == expected
