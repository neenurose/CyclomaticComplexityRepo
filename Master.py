import web
import os
import Web_Changed
from git import Repo

urls = (
'/master/', 'master'
)

class master:
    def GET(self):
        return 0
    def POST(self):
        return 0




if __name__=="__main__":
    # get the local git repo
    repo = Repo("C:/Users/meenuneenu/Documents/GitHub/mlframework")
    # get the list of commits
    commit_list = list(repo.iter_commits('master'))
    # get the files in each commit
    for each_commit in commit_list:
        print(each_commit.stats.files)


    #app = Web_Changed.MyWebApp(urls,globals())
    #app.run(port=8081)