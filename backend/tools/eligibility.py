"""
Eligibility Checker Tool
Deterministic logic to check if a user qualifies for a scheme.
"""

import json
from pathlib import Path
from typing import Dict, Any


def load_scheme(scheme_id: str) -> Dict[str, Any]:
    """
    Load scheme data from knowledge base.
    In production, this would query a database or load from JSON files.
    """
    # Path to scheme definitions
    schemes_path = Path(__file__).parent.parent / "knowledge" / "schemes"
    scheme_file = schemes_path / f"{scheme_id}.json"
    
    if scheme_file.exists():
        with open(scheme_file, 'r') as f:
            return json.load(f)
    
    # Fallback: Return a minimal mock scheme
    # TODO: Replace with actual scheme database
    return {
        "id": scheme_id,
        "name": scheme_id.replace("-", " ").title(),
        "eligibility": {
            "min_age": 0,
            "max_age": 150,
            "max_annual_income": float('inf'),
            "allowed_categories": ["General", "OBC", "SC", "ST", "EWS"],
            "min_disability_percentage": 0,
        }
    }


def check_eligibility(scheme_id: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if user is eligible for a scheme based on their profile.
    
    Args:
        scheme_id: Unique identifier for the scheme
        user_profile: User's profile data
        
    Returns:
        Dictionary with eligibility result and reasons
    """
    try:
        # Load scheme criteria
        scheme = load_scheme(scheme_id)
        eligibility_rules = scheme.get("eligibility", {})
        
        # Track eligibility checks
        checks = []
        eligible = True
        
        # 1. Age check
        user_age = user_profile.get("age", 0)
        min_age = eligibility_rules.get("min_age", 0)
        max_age = eligibility_rules.get("max_age", 150)
        
        if min_age <= user_age <= max_age:
            checks.append({
                "criterion": "age",
                "passed": True,
                "message": f"Age {user_age} is within required range ({min_age}-{max_age})"
            })
        else:
            eligible = False
            checks.append({
                "criterion": "age",
                "passed": False,
                "message": f"Age {user_age} is outside required range ({min_age}-{max_age})"
            })
        
        # 2. Income check
        user_income = user_profile.get("annual_family_income", 0)
        max_income = eligibility_rules.get("max_annual_income", float('inf'))
        
        if user_income <= max_income:
            checks.append({
                "criterion": "income",
                "passed": True,
                "message": f"Annual income ₹{user_income:,.0f} is within limit (₹{max_income:,.0f})"
            })
        else:
            eligible = False
            checks.append({
                "criterion": "income",
                "passed": False,
                "message": f"Annual income ₹{user_income:,.0f} exceeds limit (₹{max_income:,.0f})"
            })
        
        # 3. Category/Caste check
        user_category = user_profile.get("caste_category")
        allowed_categories = eligibility_rules.get("allowed_categories", [])
        
        if not allowed_categories or user_category in allowed_categories:
            checks.append({
                "criterion": "category",
                "passed": True,
                "message": f"Category '{user_category}' is eligible for this scheme"
            })
        else:
            eligible = False
            checks.append({
                "criterion": "category",
                "passed": False,
                "message": f"Category '{user_category}' is not eligible. Allowed: {', '.join(allowed_categories)}"
            })
        
        # 4. Disability percentage check (if applicable)
        min_disability = eligibility_rules.get("min_disability_percentage", 0)
        if min_disability > 0:
            user_disability = user_profile.get("disability_percentage", 0)
            if user_disability >= min_disability:
                checks.append({
                    "criterion": "disability",
                    "passed": True,
                    "message": f"Disability {user_disability}% meets minimum requirement ({min_disability}%)"
                })
            else:
                eligible = False
                checks.append({
                    "criterion": "disability",
                    "passed": False,
                    "message": f"Disability {user_disability}% is below minimum requirement ({min_disability}%)"
                })
        
        # 5. State-specific check
        allowed_states = eligibility_rules.get("allowed_states", [])
        if allowed_states:
            user_state = user_profile.get("state", "")
            if user_state in allowed_states:
                checks.append({
                    "criterion": "state",
                    "passed": True,
                    "message": f"Scheme is available in {user_state}"
                })
            else:
                eligible = False
                checks.append({
                    "criterion": "state",
                    "passed": False,
                    "message": f"Scheme is not available in {user_state}. Available in: {', '.join(allowed_states)}"
                })
        
        # 6. Occupation check
        allowed_occupations = eligibility_rules.get("allowed_occupations", [])
        if allowed_occupations:
            user_occupation = user_profile.get("occupation", "")
            if user_occupation in allowed_occupations:
                checks.append({
                    "criterion": "occupation",
                    "passed": True,
                    "message": f"Occupation '{user_occupation}' is eligible"
                })
            else:
                eligible = False
                checks.append({
                    "criterion": "occupation",
                    "passed": False,
                    "message": f"Occupation '{user_occupation}' is not eligible. Allowed: {', '.join(allowed_occupations)}"
                })
        
        # 7. BPL card check (if required)
        requires_bpl = eligibility_rules.get("requires_bpl", False)
        if requires_bpl:
            has_bpl = user_profile.get("is_bpl", False)
            if has_bpl:
                checks.append({
                    "criterion": "bpl",
                    "passed": True,
                    "message": "BPL card requirement satisfied"
                })
            else:
                eligible = False
                checks.append({
                    "criterion": "bpl",
                    "passed": False,
                    "message": "BPL card is required for this scheme"
                })
        
        return {
            "eligible": eligible,
            "scheme_id": scheme_id,
            "scheme_name": scheme.get("name", scheme_id),
            "checks": checks,
            "summary": "You are eligible for this scheme!" if eligible else "You do not meet all eligibility criteria.",
            "next_steps": eligibility_rules.get("application_link", "Visit the official portal to apply") if eligible else "Please check other schemes you may qualify for."
        }
        
    except Exception as e:
        return {
            "eligible": False,
            "scheme_id": scheme_id,
            "error": str(e),
            "message": "Error checking eligibility. Please verify scheme ID and try again."
        }


__all__ = ['check_eligibility']
