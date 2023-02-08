import os

# REDIS
# Queue name
REDIS_QUEUE = 'service_queue'

# Port
REDIS_PORT = 6379

# DB Id
REDIS_DB_ID = 0

# Host IP
REDIS_IP = os.getenv('REDIS_IP', 'redis')

# Sleep parameters which manages the
# interval between requests to our redis queue
SERVER_SLEEP = 0.05
