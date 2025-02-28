TEST_DRIVE_SLOTS = [
    # Downtown Area
    {
        "dealership": "Downtown Toyota",
        "location": "123 Main St, Downtown",
        "available_models": ["Camry", "Corolla", "RAV4", "Highlander"]
    },
    {
        "dealership": "Central City Toyota",
        "location": "456 Urban Plaza, Downtown Core",
        "available_models": ["Prius", "Camry Hybrid", "C-HR"]
    },
    
    # Eastside Area
    {
        "dealership": "Eastside Toyota",
        "location": "456 East Ave, Eastside",
        "available_models": ["RAV4", "Tacoma", "4Runner"]
    },
    {
        "dealership": "Eastside Tech Toyota",
        "location": "789 Innovation Way, Eastside Tech Park",
        "available_models": ["Prius Prime", "Mirai", "Corolla Hybrid"]
    },
    
    # Westside Area
    {
        "dealership": "Westside Premium Toyota",
        "location": "210 Luxury Lane, Westside",
        "available_models": ["Lexus RX", "Land Cruiser", "Sequoia"]
    },
    {
        "dealership": "Westside Community Toyota",
        "location": "345 Suburban Rd, Westside Suburbs",
        "available_models": ["Corolla", "Camry", "Sienna"]
    },
    
    # Northside Area
    {
        "dealership": "Northside Adventure Toyota",
        "location": "678 Mountain View Dr, Northside",
        "available_models": ["4Runner", "Tacoma", "Highlander"]
    },
    {
        "dealership": "Northside Urban Toyota",
        "location": "901 Riverside Blvd, Northside",
        "available_models": ["Camry", "RAV4", "Venza"]
    },
    
    # Suburban Area
    {
        "dealership": "Suburban Family Toyota",
        "location": "234 Family Circle, Suburban Heights",
        "available_models": ["Sienna", "Highlander", "RAV4"]
    },
    {
        "dealership": "Green Valley Toyota",
        "location": "567 Eco Park, Green Valley",
        "available_models": ["Prius", "Corolla Hybrid", "RAV4 Hybrid"]
    }
]

def get_available_test_drive_slots():
    return TEST_DRIVE_SLOTS.copy()

