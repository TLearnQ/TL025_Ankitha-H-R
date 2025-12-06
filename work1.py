log = []
results = []

pages = [
    {"page": 1, "data": [1,2,3]},
    {"page": 2, "data": [4,5,6]},
    None 
    
]

index = 0

while index < len(pages):
    page = pages[index]

    if page is None:
        log.append("No more pages. Ending.")
        break

    results.extend(page["data"])
    log.append(f"Fetched Page {page['page']}")
    
    index += 1

print("Final Data:", results)
print("Log:", log)
