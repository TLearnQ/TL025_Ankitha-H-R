log = []
max_retries = 3
attempt = 0
success = False

def mock_api():
    return "fail" if attempt < 2 else "success"

while attempt < max_retries and not success:
    attempt += 1
    response = mock_api()

    if response == "success":
        log.append(f"Success on attempt {attempt}")
        success = True
    else:
        log.append(f"Attempt {attempt} failed")

print(log)

