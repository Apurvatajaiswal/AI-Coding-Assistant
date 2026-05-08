def analyze_code(code):
    if "srcobject" in code:
        return "Error: 'srcobject' should be 'srcObject'."

    if "useState" in code and "import React" not in code:
        return "Missing React import."

    return "No obvious errors found."