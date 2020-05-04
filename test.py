import git

repo = git.Repo("/home/goprogg/PA_goprogg/")
origin = repo.remotes.origin
origin.pull()

'''
testing pulls
'''