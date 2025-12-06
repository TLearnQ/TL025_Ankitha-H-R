items = []

def get_items():
    if not items:
        return "No iteam found"
    return items

def add_item(payload=None):
    new = payload if payload else {"id": len(items)+1}
    items.append(new)
    return "Item added successfully"

def handle(request, payload=None):
    try:
        method, path = request.split()

        if method == "GET" and path == "/items":
            return get_items()

        elif method == "POST" and path == "/items":
            return add_item(payload)

        else:
            return f"Invalid route: {method} {path}"
    
    except Exception as e:
        return f"Error: {e}"

print(handle("POST /items", {"name":"Book1"}))
print(handle("POST /items", {"name":"Book2"}))
print(handle("GET /items"))
print(handle("GET /items"))

