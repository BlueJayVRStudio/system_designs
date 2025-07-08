import redis
import json

r = redis.Redis()

presence = {
    "status": "online",
    "space_id": "world_98",
    "last_seen": 1720090000
}

r.setex(f"presence:user:jay", 15, json.dumps(presence))


# Read it back
raw_value = r.get("presence:user:jay")

if raw_value:
    parsed = json.loads(raw_value)
    print(parsed["status"])       # "online"
    print(parsed["space_id"])     # "world_98"
    print(parsed["last_seen"])
else:
    print("User is offline or key expired.")