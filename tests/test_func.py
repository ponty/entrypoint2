from typing import List

from entrypoint2 import PY39PLUS, _listLike


def test_listLike():
    assert _listLike(List[str], str)
    if PY39PLUS:
        assert _listLike(list[str], str)
