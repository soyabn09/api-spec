import yaml

with open("immo.yaml", "r", encoding="utf-8") as f:
    spec = yaml.safe_load(f)

item = spec["components"]["schemas"]["Item"]
print("OAS Item keys:", sorted(item.get("properties", {}).keys()))
