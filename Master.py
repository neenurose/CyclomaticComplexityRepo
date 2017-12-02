import web
import os
import Web_Changed
from git import Repo
import requests as req
import threading

urls = (
'/master', "master",
'/register/', "register",
'/result', "done_work"
)

class master:
    def GET(self):
        return "hello"
    def POST(self):
        # get the passed parameters host and port from the url
        worker_details = web.input(host='',port='')
        if web.config.pointer < len(web.config.commit_files):
            web.config.lock.acquire()
            # get the git commit hex and filename from commit_files dictionary
            #print(web.config.pointer)
            (commithex,filename) = web.config.commit_files[web.config.pointer]
            #print((commithex,filename))
            # call the worker webservice for doing work by passing commit hex and filename
            url = "http://"+worker_details.host+":"+worker_details.port+"/worker?commithex="+commithex+"&filename="+filename
            print(url)
            web.config.pointer = web.config.pointer+1
            web.config.lock.release()
            print("pointer: ",web.config.pointer)
            response = req.get(url)
            return "Done"


        else:
            return "No task to assign!"



class register:
    def GET(self):
        # To register the worker who is active.
        web.config.worker_num = web.config.worker_num+1
        return "Active"

class done_work:
    def POST(self):
        # get the passed result after cyclomatic complexity calculation
        print("Received Cyclomatic complexity")
        worker_result = web.input(result='')
        worker_result.result = float(worker_result.result)
        web.config.lock.acquire()
        web.config.counter = web.config.counter+1
        web.config.lock.release()
        web.config.result_sum = web.config.result_sum + worker_result.result
        print("counter: ",web.config.counter)
        if web.config.counter >= (web.config.pointer-1):
            complexity_avg = web.config.result_sum/web.config.counter
            print("Average", complexity_avg)
        return "Work done!"


# count of no:of workers
global worker_num
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

    app = Web_Changed.MyWebApp(urls,globals())
    web.config.update({"worker_num":0,"pointer":1,"counter":0,"result_sum":0,"commit_files":{},"lock":threading.Lock()})
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
            if os.path.splitext(filename)[1] not in [".txt",".csv",".pdf",".md","",".pyc"]:
                web.config.commit_files[i+1] = (each_commit.hexsha,filename)
                i=i+1
    print(len(web.config.commit_files))


    app.run(port=8080)
