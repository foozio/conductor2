#!/usr/bin/env python3
"""
Test script for OpenAI Codex Conductor (without API calls)
"""

import sys
from pathlib import Path

# Add the skill directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from conductor import OpenAICodexConductor

def test_basic_functionality():
    """Test basic functionality without API calls."""
    print("Testing OpenAI Codex Conductor...")
    
    # Create a test conductor (will fail on API calls but we can test structure)
    try:
        conductor = OpenAICodexConductor(api_key="test-key")
        print("✓ Conductor class instantiated successfully")
    except Exception as e:
        print(f"✗ Failed to create conductor: {e}")
        return
    
    # Test status when no conductor directory exists
    try:
        conductor.status()
        print("✓ Status command works (no conductor dir)")
    except Exception as e:
        print(f"✗ Status command failed: {e}")
    
    print("Basic structure test completed.")

if __name__ == "__main__":
    test_basic_functionality()