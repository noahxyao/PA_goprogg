import git

repo = git.Repo("/home/goprogg/PA_goprogg/")
origin = repo.remotes.origin
print(origin)
origin.pull()