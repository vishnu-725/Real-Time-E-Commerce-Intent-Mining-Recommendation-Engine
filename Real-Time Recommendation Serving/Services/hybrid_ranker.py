def rank_scores(cf, cb, tr):
    final = {}

    for item in set(list(cf.keys()) + list(cb.keys()) + list(tr.keys())):
        final[item] = (
            cf.get(item, 0) * 0.55 +
            cb.get(item, 0) * 0.35 +
            tr.get(item, 0) * 0.10
        )

    return final
