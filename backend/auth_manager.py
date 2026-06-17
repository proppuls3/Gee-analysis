import os
import json
import ee

# Paths for storing credentials
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, "credentials.json")

def initialize_gee():
    """
    Attempts to initialize Google Earth Engine.
    First tries default user credentials, then checks for a local service account key file.
    Returns (success, message).
    """
    try:
        # Check if local service account key file exists
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'r') as f:
                key_data = json.load(f)
            
            # Initialize with service account
            email = key_data.get("client_email")
            if not email:
                return False, "Invalid credentials.json: missing client_email"
                
            # GEE Service Account Credentials
            credentials = ee.ServiceAccountCredentials(email, key_data=json.dumps(key_data))
            ee.Initialize(credentials)
            return True, f"Authenticated successfully via Service Account: {email}"
        else:
            # Try default initialization (uses local user credentials from 'earthengine authenticate')
            ee.Initialize()
            return True, "Authenticated successfully via local user credentials"
            
    except Exception as e:
        error_msg = str(e)
        # Detailed help depending on the error
        if "credential" in error_msg.lower() or "authenticate" in error_msg.lower():
            return False, "Earth Engine credentials not found. Please authenticate or provide a Service Account key."
        return False, f"GEE Initialization failed: {error_msg}"

def save_service_account_key(key_content_str):
    """
    Validates and saves the service account key contents to config/credentials.json.
    Returns (success, message).
    """
    try:
        key_data = json.loads(key_content_str)
        
        # Basic validation
        required_keys = ["type", "project_id", "private_key", "client_email"]
        for key in required_keys:
            if key not in key_data:
                return False, f"Missing required key in JSON: '{key}'"
        
        # Ensure config directory exists
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        # Write file
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(key_data, f, indent=4)
            
        # Try initializing with this new key to verify
        success, message = initialize_gee()
        if not success:
            # Delete file if it's invalid and doesn't authenticate
            if os.path.exists(CREDENTIALS_FILE):
                os.remove(CREDENTIALS_FILE)
            return False, f"Key saved but initialization failed: {message}"
            
        return True, "Service account key saved and successfully authenticated."
        
    except json.JSONDecodeError:
        return False, "Invalid JSON format. Please paste a valid JSON key file contents."
    except Exception as e:
        return False, f"Failed to save credentials: {str(e)}"

def get_auth_status():
    """
    Checks if GEE is currently initialized and working.
    Returns dict with status details.
    """
    success, message = initialize_gee()
    if success:
        try:
            # Perform a lightweight test query to ensure connection works
            # Fetch a single pixel from SRTM elevation dataset
            test_img = ee.Image("USGS/SRTMGL1_003")
            test_img.getInfo() # Triggers request
            return {
                "authenticated": True,
                "mode": "Live GEE Mode",
                "message": message,
                "api_active": True
            }
        except Exception as e:
            return {
                "authenticated": True,
                "mode": "Live GEE Mode (Error)",
                "message": f"Authenticated, but test query failed: {str(e)}",
                "api_active": False
            }
    else:
        return {
            "authenticated": False,
            "mode": "Demo Mode (Offline)",
            "message": f"Using pre-loaded database. GEE status: {message}",
            "api_active": False
        }
