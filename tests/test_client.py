from client.api_client import APIClient
from client.keys import KeyManager

client=APIClient()

username="bo"
password="123"


result=client.login(
    username,password
)
print(result)

print("\nCurrent user:")

print(
    client.getMe()
)