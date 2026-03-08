import redis

#  create a redis client
r = redis.Redis(host="localhost", port=6379, db=0)


# store a key value pair
r.set("name", "Christian")
# print(r.get("name").decode())

# SIMULATE STORING A TOKEN
token = "abc123"
user_id = "user_42"
r.set(f"token:{token}", user_id, ex=60)

while r.get(f"token:{token}"):
    # keep printing it
    val = r.get(f"token:{token}")
    ttl = r.ttl(f"token:{token}")
    print(f"token value is {val} and ttl is {ttl}")
