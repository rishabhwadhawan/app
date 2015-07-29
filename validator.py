import requests
from mongo import ValidatorTable
import json

def make_mock_requests():
	table = ValidatorTable()
	logged_requests = table.see_log()
	json_logs = []
	for logged_request in logged_requests:
		req_resp = (json.loads(logged_request['request']), json.loads(logged_request['response']))
		json_logs.append(req_resp)
	for x in json_logs:
		mock_request(x)

def compare_responses(new, old):
	#Do better compares, based on content...! PLS
	return new != old

def mock_request(x):

	headers = json.loads(x[0][0])
	logged_response = x[1]

	path = str(x[0][1]).replace('"', "")
	method = str(x[0][2]).replace('"', "")
	url = headers['origin'] + path
	data = json.loads(x[0][3])

	#print(headers)

	if method == 'GET':
		new_response = requests.get(url)
	elif method == 'PATCH':
		data = json.dumps(data)
		new_response = requests.patch(url, headers=headers, data=data)
	elif method == 'PUT' or method == 'POST':
		new_response = requests.put(url, headers=headers, data=data)
	elif method == 'DELETE':
		new_response = requests.delete(url, headers=headers, data=data)
	else:
		print("Hmm, method was %s"%(method))
	print(new_response)

	if new_response != logged_response:
		return ("Responses differ.", x, new_response, logged_response)
		print("Error, responses differ.")
		print("___REQUEST___")
		print(x)
		print("___V1 RESPONSE___")
		print(logged_response)
		print("___NEW RESPONSE___")
		print(new_response)
	else:
		print("No difference between responses for %s request at URL %s with body %s. The response was: %s."%(method, url, data, new_response))
 
if __name__ == "__main__":
	make_mock_requests()




 
