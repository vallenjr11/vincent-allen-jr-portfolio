#!/bin/bash

echo "[+] Generating test data in Redis..."

# Insert some keys
docker exec redis redis-cli SET user:1 "Bits"
docker exec redis redis-cli SET user:2 "Datadogs"
docker exec redis redis-cli SET session:123 "xyz"
docker exec redis redis-cli EXPIRE session:123 60

# Run some reads
docker exec redis redis-cli GET user:1
docker exec redis redis-cli GET user:2

# Simulate counter activity
for i in {1..5}; do
  docker exec redis redis-cli INCR pageviews
done

# Create a hash
docker exec redis redis-cli HSET config theme "dark"
docker exec redis redis-cli HSET config lang "en"

echo "[+] Done. Redis activity simulated. You should now see dynamic metrics in Datadog."
