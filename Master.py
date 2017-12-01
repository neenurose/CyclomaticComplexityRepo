import web
import os
import Web_Changed
from git import Repo
import shelve
import requests as req

urls = (
'/master/', 'master'
'/register/', 'register'
'/result', 'done_work'
)

class master:
    def GET(self):
        return 0
    def POST(self):
        # get the passed parameters host and port from the url
        worker_details = web.input(host='',port='')
        # get the git commit hex and filename from commit_files dictionary
        (commithex,filename) = commit_files[pointer]
        # call the worker webservice for doing work by passing commit hex and filename
        url = "http://"+worker_details.host+":"+worker_details.port+"/worker?commithex="+commithex+"&filename="+filename
        pointer = pointer+1
        response = req.get(url)
        return "Assigned"


class register:
    def POST(self):
        # To register the worker who is active.
        worker_num = worker_num+1
        return "Active"

class done_work:
    def POST(self):
        # get the passed result after cyclomatic complexity calculation
        worker_result = web.input(result='')
        counter = counter+1
        result_sum = result_sum + worker_result.result
        if counter==pointer:
            complexity_avg = result_sum/counter
        return "Work done!"


# count of no:of workers
worker_num = 0
# iterator through global dictionary commit_files
pointer = 1
# dictionary that stores id(integers) as key and (commt hex,filename) as value
commit_files={}
# count the number of distributed respose_ask_task
counter = 0
# for adding the cyclomatic complexity result from worker_result
result_sum = 0

if __name__=="__main__":
    # get the local git repo
    repo = Repo("C:/Users/meenuneenu/Documents/GitHub/mlframework")
    # get the list of commits
    commit_list = list(repo.iter_commits('master'))
    # get the files in each commit
    i=0
    for each_commit in commit_list:
        #commit_files[each_commit.hexsha]=(list(each_commit.stats.files.keys()))
        # Create a dictionary with id as key and (commit hex,filename) as value
        for filename in (list(each_commit.stats.files.keys())):
            commit_files[i+1] = (each_commit.hexsha,filename)
            i=i+1
    print(commit_files)

    #app = Web_Changed.MyWebApp(urls,globals())
    #app.run(port=8081)
