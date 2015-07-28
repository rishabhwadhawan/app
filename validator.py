import requests
from mongo import ValidatorTable
import json

def make_mock_requests():
	table = ValidatorTable()
	logged_requests = table.see_log()
	json_logs = []
	for logged_request in logged_requests:
		json_logs.append(json.loads(logged_request['log']))
	for x in json_logs:
		mock_request(x)

def parse_request_data(data):
	#DoCoolStuffToData, based on content...!
	return {}, data

def parse_response_data(data):
	return data

def compare_responses(new, old):
	#Do better compares, based on content...! PLS
	return new != old

def mock_request(x):
	method = x['type']
	url = x['url']
	headers, data = parse_request_data(x['reqData'])
	body = json.dumps(data)
	logged_response = parse_response_data(x['respData'])
	if method == "GET":
		new_response = requests.get(url)
	elif method == "PATCH":
		data = json.dumps(data)
		new_response = requests.patch(url, headers=headers, data=data)
	elif method == "PUT":
		new_response = requests.put(url, headers=headers, data=data)
	elif method == "DELETE":
		new_response = requests.delete(url, headers=headers, data=data)

	if compare_responses(new_response, logged_response):
		return ("Responses differ.", x, new_response, logged_response)
		print("Error, responses differ.")
		print("___REQUEST___")
		print(x)
		print("___V1 RESPONSE___")
		print(logged_response)
		print("___NEW RESPONSE___")
		print(new_response)
 
if __name__ == "__main__":
	make_mock_requests()
