import pytest
from services.hybrid_ranker import rank_scores

def test_rank_scores_basic():
    cf = {1: 0.5, 2: 0.3}
    cb = {2: 0.4, 3: 0.6}
    tr = {1: 0.2, 3: 0.3}
    result = rank_scores(cf, cb, tr)
    assert isinstance(result, dict)
    assert set(result.keys()) == {1,2,3}
    # Check weighted sum
    assert result[1] == 0.5*0.55 + 0.2*0.1
    assert result[2] == 0.3*0.55 + 0.4*0.35
