import json
from pathlib import Path

p = Path("immo/items.json")
data = json.loads(p.read_text(encoding="utf-8"))
ip = data["properties"]["items"]["items"]["properties"]


def keys(d):
    return sorted(list(d.keys()))


print("Item keys:", keys(ip))
print("Item required:", ip.get("required"))

req = ip.get("requirements", {}).get("properties", {})
print("requirements keys:", keys(req))

stats = ip.get("stats", {}).get("properties", {})
print("stats keys:", keys(stats))

tmod = ip.get("tier_modifiers", {}).get("properties", {})
print("tier_modifiers keys:", keys(tmod))

if "effects" in ip and "items" in ip["effects"]:
    eff = ip["effects"]["items"]["properties"]
    print("effects item keys:", keys(eff))


# Newer fields to inspect
def summarize(node):
    if not isinstance(node, dict):
        return str(type(node))
    t = node.get("type")
    if t == "object":
        return {
            "type": t,
            "keys": keys(node.get("properties", {})),
            "required": node.get("required"),
        }
    if t == "array":
        it = node.get("items", {})
        if isinstance(it, dict) and it.get("type") == "object":
            return {
                "type": t,
                "item_keys": keys(it.get("properties", {})),
                "item_required": it.get("required"),
            }
        return {"type": t, "items_type": it.get("type")}
    return {"type": t}


for k in [
    "pet",
    "where_to_find",
    "upgrade_requirements",
    "health_restore",
    "hunger_restore",
    "recipe",
]:
    print(k, ":", summarize(ip.get(k)))

wtf = ip.get("where_to_find", {})
wtf_props = wtf.get("properties", {})
if wtf_props:
    print("where_to_find subkeys:", keys(wtf_props))
    for sk, sv in wtf_props.items():
        if sv.get("type") == "array":
            it = sv.get("items", {})
            print(
                f"  - {sk}: array of",
                it.get("type"),
                "props:",
                keys(it.get("properties", {})),
            )
        else:
            print(f"  - {sk}:", sv.get("type"))

rec = ip.get("recipes")
if rec and rec.get("type") == "object":
    rp = rec.get("properties", {})
    print("recipes keys:", keys(rp))
    exp = rp.get("experience", {})
    sp = exp.get("properties", {}).get("stats", {}).get("properties", {})
    sk = exp.get("properties", {}).get("skills", {}).get("properties", {})
    print("recipes.experience.stats keys:", keys(sp))
    print("recipes.experience.skills keys:", keys(sk))
    mat = rp.get("materials", {}).get("items", {}).get("properties", {})
    print("recipes.materials item keys:", keys(mat))
    res = rp.get("result", {}).get("properties", {})
    print("recipes.result keys:", keys(res))
