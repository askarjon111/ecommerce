import requests

headers = {}
headers['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI5NTMxMDA0LCJqdGkiOiJmZDM5NDVjOTY3Yjg0M2ViODY2YzRjNjliNDYzZTFjYiIsInVzZXJfaWQiOjF9.3TxrOyXvmk9DuLlRfFGjA-wG_lq5j3OWlVN9NsLUn_s'

r = requests.get('http://127.0.0.1:8000/api/', headers=headers)
print(r.text)
