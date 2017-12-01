import web
import os
import Web_Changed
from git import Repo
import sys
import lizard

urls = (
'/worker', 'worker'
)

class worker:
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
        cyclomatic_complexity = lizard.analyze_file(worker_input.filename)
        os.remove(worker_input.filename)
        return (cyclomatic_complexity.nloc)



    def POST(self):
        return 0




if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Please provide host and port number")
        exit()
    host = sys.argv[1]
    port = int(sys.argv[2])

    app = Web_Changed.MyWebApp(urls,globals())
    app.run(port=port)