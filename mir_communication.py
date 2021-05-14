import requests

host = 'http://192.168.12.20/api/v2.0.0/'

# Headers:

headers = {'Content-Type': 'application/json',
           'Authorization': 'Basic OmUzYjBjNDQyOThmYzFjMTQ5YWZiZjRjODk5NmZiOTI0MjdhZTQxZTQ2NDliOTM0Y2E0OTU5OTFiNzg1MmI4NTU=',
           'Host' : '192.168.12.20:8080'}

# Body:

body = {'mission_id' : '5e794de3-6dfe-11eb-b44a-0001299df20a' }

send_mission = requests.post(host + 'mission_queue', headers = headers, body = body)

print(send_mission)