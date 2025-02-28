# Mock data for Toyota service and test drive slots

SERVICE_SLOTS = [
   {
        "date": "2024-03-01",
        "time": "09:00",
        "location": "Downtown Toyota Service",
        "available": True
    },
    {
        "date": "2024-03-01",
        "time": "11:00",
        "location": "Downtown Toyota Service",
        "available": True
    },
    {
        "date": "2024-03-02",
        "time": "10:00",
        "location": "Downtown Toyota Service",
        "available": True
    },
    
    # Eastside Toyota Service Slots
    {
        "date": "2024-03-01",
        "time": "10:30",
        "location": "Eastside Toyota Service",
        "available": True
    },
    {
        "date": "2024-03-02",
        "time": "13:45",
        "location": "Eastside Toyota Service",
        "available": True
    },
    {
        "date": "2024-03-03",
        "time": "11:15",
        "location": "Eastside Toyota Service",
        "available": True
    },
    
    # Westside Toyota Service Slots
    {
        "date": "2024-03-01",
        "time": "13:00",
        "location": "Westside Toyota Service",
        "available": True
    },
    {
        "date": "2024-03-02",
        "time": "09:45",
        "location": "Westside Toyota Service",
        "available": True
    },
    {
        "date": "2024-03-02",
        "time": "16:30",
        "location": "Westside Toyota Service",
        "available": True
    },
    {
        "date": "2024-03-03",
        "time": "12:45",
        "location": "Westside Toyota Service",
        "available": True
    },
    
    # Northside Toyota Service Slots
    {
        "date": "2024-03-01",
        "time": "15:15",
        "location": "Northside Toyota Service",
        "available": True
    },
    {
        "date": "2024-03-02",
        "time": "11:30",
        "location": "Northside Toyota Service",
        "available": True
    },
    {
        "date": "2024-03-03",
        "time": "09:15",
        "location": "Northside Toyota Service",
        "available": True
    },
]


# Optional: Helper functions to manage mock data
def get_available_service_slots():
    return [slot for slot in SERVICE_SLOTS if slot["available"]]
