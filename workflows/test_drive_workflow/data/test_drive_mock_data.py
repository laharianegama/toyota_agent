
TEST_DRIVE_SLOTS = [
    {
        "dealership": "Toyota Downtown",
        "location": "123 Main Street, Downtown",
        "hours": "Mon-Fri: 9am-7pm, Sat: 10am-5pm, Sun: Closed",
        "phone": "555-123-4567",
        "available_models": ["Camry", "Corolla", "RAV4", "Highlander", "Prius"],
        "test_drive_availability": True,
        "region": "Downtown"
    },
    {
        "dealership": "Toyota Eastside",
        "location": "456 Oak Avenue, East Hills",
        "hours": "Mon-Fri: 8am-8pm, Sat: 9am-6pm, Sun: 11am-4pm",
        "phone": "555-234-5678",
        "available_models": ["Camry", "Corolla", "RAV4", "4Runner", "Tacoma", "Tundra"],
        "test_drive_availability": True,
        "region": "Eastside"
    },
    {
        "dealership": "Toyota Westside",
        "location": "789 Sunset Boulevard, West End",
        "hours": "Mon-Fri: 9am-7pm, Sat: 10am-6pm, Sun: Closed",
        "phone": "555-345-6789",
        "available_models": ["Camry", "Corolla", "RAV4", "Sienna", "Venza", "Supra", "GR86"],
        "test_drive_availability": True,
        "region": "Westside"
    },
    {
        "dealership": "Toyota Northside",
        "location": "101 Pine Road, North Hills",
        "hours": "Mon-Sat: 9am-7pm, Sun: 11am-5pm",
        "phone": "555-456-7890",
        "available_models": ["Camry", "Corolla", "RAV4", "Tacoma", "Tundra", "Land Cruiser"],
        "test_drive_availability": True,
        "region": "Northside"
    },
    {
        "dealership": "Toyota Southside",
        "location": "202 Palm Drive, South Bay",
        "hours": "Mon-Fri: 8:30am-7:30pm, Sat: 9am-6pm, Sun: Closed",
        "phone": "555-567-8901",
        "available_models": ["Camry", "Corolla", "RAV4", "Highlander", "C-HR", "Avalon"],
        "test_drive_availability": True,
        "region": "Southside"
    },
    {
        "dealership": "Toyota Midtown",
        "location": "303 Maple Street, Midtown",
        "hours": "Mon-Fri: 9am-8pm, Sat: 10am-7pm, Sun: 11am-5pm",
        "phone": "555-678-9012",
        "available_models": ["Camry", "Corolla", "RAV4", "Prius", "Highlander", "Sequoia"],
        "test_drive_availability": True,
        "region": "Midtown"
    },
    {
        "dealership": "Toyota Harbor",
        "location": "404 Beach Road, Harbor District",
        "hours": "Mon-Sat: 8am-7pm, Sun: 10am-4pm",
        "phone": "555-789-0123",
        "available_models": ["Camry", "Corolla", "RAV4", "4Runner", "Tacoma", "Tundra"],
        "test_drive_availability": True,
        "region": "Harbor District"
    },
    {
        "dealership": "Toyota Valley",
        "location": "505 River Lane, Pleasant Valley",
        "hours": "Mon-Fri: 9am-7pm, Sat: 9am-6pm, Sun: Closed",
        "phone": "555-890-1234",
        "available_models": ["Camry", "Corolla", "RAV4", "Sienna", "Venza"],
        "test_drive_availability": True,
        "region": "Valley"
    }
]

# For testing/debugging
if __name__ == "__main__":
    import random
    
    # Print a random dealership
    random_dealership = random.choice(TEST_DRIVE_SLOTS)
    print(f"Random dealership: {random_dealership['dealership']} in {random_dealership['location']}")