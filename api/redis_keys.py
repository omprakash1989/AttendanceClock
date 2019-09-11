"""
Add all redis keys over here.

The key type in comment is a must.

all key prefix: `clock_app:`

Please follow the standard of adding prefix to every key added to this app to prevent collision in keys (Staging, UAT)
till namespace is supported in redis.

"""

# Key to store last allocated lender.
# Set value in <key>, <value> pair.
