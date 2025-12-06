values = [45, 67, 89, 23, 56]

for v in values:
    if v >= 80:
        label = "High"
    elif v >= 50:
        label = "Medium"
    else:
        label = "Low"
    
    print(v, "→", label)
    