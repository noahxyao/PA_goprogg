import git

repo = git.Repo("./")
origin = repo.remotes.origin
print(origin)
origin.pull()