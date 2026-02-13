# security/rate_limiter.py
"""
Rate limiting to prevent abuse
Limits tool calls per time window
"""

import time
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

# In-memory rate limit tracker
_rate_limit_store = defaultdict(list)

def rate_limit(
    tool_name: str,
    max_requests: int = 10,
    time_window: int = 60
) -> bool:
    """
    Check if tool call is within rate limit
    
    Args:
        tool_name: Name of tool
        max_requests: Max requests allowed
        time_window: Time window in seconds
    
    Returns:
        True if within limit, False if exceeded
    """
    current_time = time.time()
    
    # Clean old requests outside time window
    _rate_limit_store[tool_name] = [
        req_time for req_time in _rate_limit_store[tool_name]
        if current_time - req_time < time_window
    ]
    
    # Check if limit exceeded
    if len(_rate_limit_store[tool_name]) >= max_requests:
        logger.warning(f"Rate limit exceeded for {tool_name}")
        return False
    
    # Record new request
    _rate_limit_store[tool_name].append(current_time)
    return True

# ========== EXPLOIT TEST ==========

def test_rate_limit():
    """Test that rate limiting blocks excessive calls"""
    tool = "test_tool"
    
    # Make 11 rapid calls (limit is 10)
    results = []
    for i in range(11):
        results.append(rate_limit(tool, max_requests=10, time_window=60))
    
    if results[-1] == False:  # 11th call should fail
        print("✓ PASSED: Rate limit enforced (11th call blocked)")
        return True
    else:
        print("❌ FAILED: Rate limit NOT enforced")
        return False

if __name__ == "__main__":
    test_rate_limit()
