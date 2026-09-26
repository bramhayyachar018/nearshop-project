from typing import Any, Optional, Dict

def standard_response(success: bool, data: Any = None, error: Optional[str] = None) -> Dict[str, Any]:
    """
    Standardize all API responses so the frontend can handle state predictably.
    """
    return {
        "success": success,
        "data": data,
        "error": error
    }
