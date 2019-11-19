import argparse
import datetime

import git

import zqx_git


def extract_tm(repo_path, lower, upper):
    repo = git.Repo(repo_path)

    period = datetime.timedelta(days=7)

    last_snap = None

    for commit in zqx_git.filter_descending_iterator_dates(
        zqx_git.head_iterator(repo), lower, upper
    ):
        if (
            not last_snap
            or last_snap.committed_datetime - period > commit.committed_datetime
        ):
            last_snap = commit
            print(last_snap.committed_datetime)

            def traversal(o, _):
                if o.type == "blob":
                    print(o.path)
                return True

            print(len(list(last_snap.tree.traverse(traversal))))
        print(
            commit,
            commit.committed_datetime,
            commit.author.email,
            list(commit.stats.files.keys()),
        )


def _utc_iso(s):
    return datetime.datetime.fromisoformat(s).replace(tzinfo=datetime.timezone.utc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_path")
    parser.add_argument("lower", help="yyyy-mm-dd", type=_utc_iso)
    parser.add_argument("upper", help="yyyy-mm-dd", type=_utc_iso)
    args = parser.parse_args()
    extract_tm(
        args.repo_path, args.lower, args.upper,
    )


if __name__ == "__main__":
    main()
