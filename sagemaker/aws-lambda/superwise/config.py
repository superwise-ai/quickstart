import os
 

class Config:
    FRONTEGG_URL = os.environ.get("FRONTEGG_SUPERWISE_URL", "https://auth.superwise.ai")
    SUPERWISE_HOST = os.environ.get("SUPERWISE_HOST", "portal.superwise.ai")
    POOLING_INTERVAL_SEC = 15
