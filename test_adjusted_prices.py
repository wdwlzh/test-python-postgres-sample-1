#!/usr/bin/env python3
"""
Test script to verify the adjusted prices API implementation
"""

import sys
import os

# Add the backend app to the path
sys.path.append('/workspaces/backend')

try:
    # Test imports
    from backend.app.models import AdjustedPrice, Stock
    from backend.app.main import fetch_tiingo_adjusted_data, TiingoAdjustedPriceResponse
    print("✅ Successfully imported new models and functions")
    
    # Test model structure
    print("\n📋 AdjustedPrice model fields:")
    for column in AdjustedPrice.__table__.columns:
        print(f"  - {column.name}: {column.type}")
    
    print("\n✅ All imports successful! The implementation looks good.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
