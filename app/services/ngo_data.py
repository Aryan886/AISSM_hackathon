"""
NGO Database - Fixed list for Gemini API recommendations

TODO: Replace this with your actual NGO data
You can later switch this to load from:
- JSON file
- CSV file  
- API endpoint from Node.js
- MongoDB query
"""

NGOS = [
    {
        "name": "CleanWater Foundation",
        "category": "Water",
        "area": "Kothrud"
    },
    {
        "name": "GreenCity NGO",
        "category": "Waste",
        "area": "All Pune"
    },
    {
        "name": "SafeWomen NGO",
        "category": "Women Safety",
        "area": "All Pune"
    },
    {
        "name": "AnimalCare",
        "category": "Animal Rescue",
        "area": "Kothrud"
    },
    {
        "name": "Urban Relief NGO",
        "category": "Infrastructure",
        "area": "All Pune"
    },
    {
        "name": "CommunityAid Trust",
        "category": "General",
        "area": "All Pune"
    },
    {
        "name": "RoadSafety Initiative",
        "category": "Roads",
        "area": "Pune Central"
    },
    {
        "name": "HealthFirst Foundation",
        "category": "Healthcare",
        "area": "All Pune"
    },
    {
        "name": "EcoWarriors Pune",
        "category": "Environment",
        "area": "All Pune"
    },
    {
        "name": "StreetLight Campaign",
        "category": "Electricity",
        "area": "Kothrud"
    }
]


def get_ngo_list():
    """
    Returns the list of NGOs
    
    Returns:
        List of NGO dictionaries
    """
    return NGOS


def format_ngos_for_prompt():
    """
    Format NGO list for Gemini prompt
    
    Returns:
        Formatted string representation of NGOs
    """
    formatted = "Available NGOs:\n\n"
    for idx, ngo in enumerate(NGOS, 1):
        formatted += f"{idx}. {ngo['name']} — {ngo['category']} — {ngo['area']}\n"
    return formatted