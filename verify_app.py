import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=========================================================")
print("            APPLICATION VERIFICATION SCRIPT              ")
print("=========================================================")
print()

# Test Imports
print("[1/3] Testing backend imports...")
try:
    import fastapi
    import uvicorn
    import ee
    print("  - Standard libraries: OK")
except ImportError as e:
    print(f"  - [FAIL] Standard library import error: {e}")
    sys.exit(1)

try:
    from backend.auth_manager import initialize_gee, get_auth_status
    from backend.mock_database import get_communities_list, get_community_data, get_all_leads
    from backend.gee_analysis import run_gee_change_detection
    from backend.app import app
    print("  - Project modules: OK")
except Exception as e:
    print(f"  - [FAIL] Project module import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test Database Consistency
print("\n[2/3] Verifying database structure...")
try:
    comms = get_communities_list()
    leads = get_all_leads()
    print(f"  - Total communities loaded: {len(comms)}")
    print(f"  - Total leads loaded: {len(leads)}")
    
    # Check emirates represented
    emirates = set()
    for c in comms:
        if "Dubai" in c["name"]: emirates.add("Dubai")
        elif "Abu Dhabi" in c["name"]: emirates.add("Abu Dhabi")
        elif "Sharjah" in c["name"]: emirates.add("Sharjah")
        elif "Ras Al Khaimah" in c["name"]: emirates.add("Ras Al Khaimah")
        elif "Ajman" in c["name"]: emirates.add("Ajman")
    print(f"  - Emirates represented: {', '.join(emirates)}")
    
    if len(comms) < 5 or len(leads) < 5:
        print("  - [FAIL] Database contains insufficient test records.")
        sys.exit(1)
    print("  - Database verification: OK")
except Exception as e:
    print(f"  - [FAIL] Database query failed: {e}")
    sys.exit(1)

# Test FastAPI configuration
print("\n[3/3] Testing FastAPI router configuration...")
try:
    # Basic check to ensure routes are defined
    routes = [r.path for r in app.routes]
    expected_routes = ["/api/status", "/api/authenticate", "/api/communities", "/api/analyze", "/api/leads"]
    for er in expected_routes:
        if er not in routes:
            print(f"  - [FAIL] Expected route '{er}' not found in FastAPI app.")
            sys.exit(1)
    print(f"  - Found {len(routes)} active routes (including static routes).")
    print("  - FastAPI config verification: OK")
except Exception as e:
    print(f"  - [FAIL] FastAPI config failed: {e}")
    sys.exit(1)

print("\n=========================================================")
print("  VERIFICATION SUCCESS: All local systems operating OK!   ")
print("=========================================================")
