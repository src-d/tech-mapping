import argparse
import datetime

import git


def head_iterator(repo):
    commit = repo.head.commit
    while True:
        yield commit
        if not commit.parents:
            break
        commit = commit.parents[0]


def extract_tm(repo_path):
    repo = git.Repo(repo_path)

    begin = datetime.datetime(2019, 11, 1, tzinfo=datetime.timezone.utc)
    end = datetime.datetime(2019, 7, 1, tzinfo=datetime.timezone.utc)
    period = datetime.timedelta(days=7)

    last_snap = None

    for commit in head_iterator(repo):
        if commit.committed_datetime > begin:
            continue
        if commit.committed_datetime < end:
            break
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_path")
    args = parser.parse_args()
    extract_tm(args.repo_path)


if __name__ == "__main__":
    main()
