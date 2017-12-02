import web
import os
import Web_Changed
from git import Repo
import sys
import lizard
import requests as req
import threading



class worker(threading.Thread):
    def run(self):
        urls = (
        '/worker', 'worker'
        )
        app = Web_Changed.MyWebApp(urls,globals())
        app.run(port=port)
    def GET(self):
        # get the passed parameters commit hex and filename from the url
        worker_input = web.input(commithex='',filename='')
        repo = Repo("C:/Users/meenuneenu/Documents/GitHub/mlframework")
        # Take the file content at the time of passed commit and save it in a .py file
        file_content = repo.git.show("%s:%s" % (worker_input.commithex, worker_input.filename))

        #with tempfile.NamedTemporaryFile(suffix='.py',delete=True) as tmp:
        #    tmp.write(file_content.encode())

        with open(worker_input.filename,'w+') as fp:
            fp.write(file_content)
        fp.close()
        # Calculate the cyclomatic complexity of the file
        cyclomatic_complexity = lizard.analyze_file(worker_input.filename).average_cyclomatic_complexity
        os.remove(worker_input.filename)
        print("CC: ",cyclomatic_complexity)
        # Pass the result to master
        url = "http://localhost:8080/result?result="+str(cyclomatic_complexity)
        print(url)
        result = req.post(url)
        print("From Master after result",result.text)
        #return (cyclomatic_complexity)



    def POST(self):
        return 0


if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Please provide host and port number")
        exit()
    host = sys.argv[1]
    port = int(sys.argv[2])
    first_time = 1


    while(True):
        worker().start()
        # To register the worker in master
        url = "http://localhost:8080/register/"
        response = req.get(url)
        print("Response: ",response.text)
        # if the response is "Active", ask for the task
        if response.text == "Active":
            respose_ask_task = req.post("http://localhost:8080/master?host="+host+"&port="+str(port))
            print("Response ask task: ",respose_ask_task.text)
            if respose_ask_task.text == "No task to assign!":
                break;
    sys.exit(0)
