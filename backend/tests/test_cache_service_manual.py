import os
import sys

LAMBDA_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "lambda-functions")
)
sys.path.insert(0, LAMBDA_FOLDER)

from cache_service import (
    delete_cached_value,
    get_cached_json,
    set_cached_json,
)


cache_key = "dashboard:metrics:user_123"

metrics = {
    "applicationsSent": 5,
    "dsaDone": 12,
    "followUpsDue": 2,
}

delete_cached_value(cache_key)

print("Before cache:", get_cached_json(cache_key))

set_cached_json(cache_key, metrics, ttl_seconds=300)

print("After cache:", get_cached_json(cache_key))