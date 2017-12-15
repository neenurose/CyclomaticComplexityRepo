import requests as req

url_client_stats = "http://localhost:8080/graph_stats"

response = req.get(url_client_stats)
print("Response: ",response.text)
