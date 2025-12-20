import requests

api_url = "https://httpbin.org/put"

headers = {
    "Authorization": "Bearer mytoken",
    "Content-Type": "application/json"
}

payload = {
    "count": 5
}

# Send PUT request
response = requests.put(api_url, headers=headers, json=payload)

# Convert response to JSON
data = response.json()

# Extract numeric field
count_value = data["json"]["count"]

print(count_value)