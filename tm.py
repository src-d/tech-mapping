import argparse
import datetime

import git

import zqx_git


class _SnapshotTracker:
    def __init__(self, snapshots):
        self.snapshots = sorted(snapshots)
        self.last_call = None

    def _peek_next_snapshot(self):
        return self.snapshots[-1] if self.snapshots else None

    def _pop_next_snapshot(self):
        if not self.snapshots:
            return
        return self.snapshots.pop()

    def snapshots_for_date(self, d):
        assert (
            not self.last_call or d < self.last_call
        ), "This method is stateful and can only be called with decreasing ds"
        self.last_call = d

        snaps = []
        while self._peek_next_snapshot():
            if d > self._peek_next_snapshot():
                break
            snap = self._pop_next_snapshot()
            snaps.append(snap)
        return snaps


def extract_tm(repo_path, lower, upper, snapshots):
    repo = git.Repo(repo_path)

    snapshot_tracker = _SnapshotTracker(snapshots)

    for commit in zqx_git.filter_descending_iterator_dates(
        zqx_git.head_iterator(repo), lower, upper
    ):
        commit_snapshots = snapshot_tracker.snapshots_for_date(
            commit.committed_datetime
        )
        if commit_snapshots:
            print(commit_snapshots, commit.committed_datetime)

            def traversal(o, _):
                if o.type == "blob":
                    print(o.path)
                return True

            print(len(list(commit.tree.traverse(traversal))))
        print(
            commit,
            commit.committed_datetime,
            commit.author.email,
            list(commit.stats.files.keys()),
        )


def make_snapshots(lower, upper, base, period):
    d = base
    while d < lower:
        d += period
    result = []
    while d < upper:
        result.append(d)
        d += period
    return result


def _utc_iso(s):
    return datetime.datetime.fromisoformat(s).replace(tzinfo=datetime.timezone.utc)


def _timedelta_days(s):
    return datetime.timedelta(days=int(s))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_path")
    parser.add_argument("lower", help="yyyy-mm-dd", type=_utc_iso)
    parser.add_argument("upper", help="yyyy-mm-dd", type=_utc_iso)
    parser.add_argument("snapshot_base", help="yyyy-mm-dd", type=_utc_iso)
    parser.add_argument("snapshot_days", type=_timedelta_days)
    args = parser.parse_args()
    snapshots = make_snapshots(
        args.lower, args.upper, args.snapshot_base, args.snapshot_days
    )
    extract_tm(args.repo_path, args.lower, args.upper, snapshots)


if __name__ == "__main__":
    main()
