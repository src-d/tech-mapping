import itertools


def head_iterator(repo):
    commit = repo.head.commit
    while True:
        yield commit
        if not commit.parents:
            break
        commit = commit.parents[0]


def filter_descending_iterator_dates(iter, lower, upper):
    drop_greater_upper = itertools.dropwhile(
        lambda commit: commit.committed_datetime > upper, iter
    )
    drop_less_lower = itertools.takewhile(
        lambda commit: commit.committed_datetime > lower, drop_greater_upper
    )
    return drop_less_lower
