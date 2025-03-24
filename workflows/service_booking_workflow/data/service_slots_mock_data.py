# # Mock data for Toyota service and test drive slots

# SERVICE_SLOTS = [
#    {
#         "date": "2024-03-01",
#         "time": "09:00",
#         "location": "Downtown Toyota Service",
#         "available": True
#     },
#     {
#         "date": "2024-03-01",
#         "time": "11:00",
#         "location": "Downtown Toyota Service",
#         "available": True
#     },
#     {
#         "date": "2024-03-02",
#         "time": "10:00",
#         "location": "Downtown Toyota Service",
#         "available": True
#     },
    
#     # Eastside Toyota Service Slots
#     {
#         "date": "2024-03-01",
#         "time": "10:30",
#         "location": "Eastside Toyota Service",
#         "available": True
#     },
#     {
#         "date": "2024-03-02",
#         "time": "13:45",
#         "location": "Eastside Toyota Service",
#         "available": True
#     },
#     {
#         "date": "2024-03-03",
#         "time": "11:15",
#         "location": "Eastside Toyota Service",
#         "available": True
#     },
    
#     # Westside Toyota Service Slots
#     {
#         "date": "2024-03-01",
#         "time": "13:00",
#         "location": "Westside Toyota Service",
#         "available": True
#     },
#     {
#         "date": "2024-03-02",
#         "time": "09:45",
#         "location": "Westside Toyota Service",
#         "available": True
#     },
#     {
#         "date": "2024-03-02",
#         "time": "16:30",
#         "location": "Westside Toyota Service",
#         "available": True
#     },
#     {
#         "date": "2024-03-03",
#         "time": "12:45",
#         "location": "Westside Toyota Service",
#         "available": True
#     },
    
#     # Northside Toyota Service Slots
#     {
#         "date": "2024-03-01",
#         "time": "15:15",
#         "location": "Northside Toyota Service",
#         "available": True
#     },
#     {
#         "date": "2024-03-02",
#         "time": "11:30",
#         "location": "Northside Toyota Service",
#         "available": True
#     },
#     {
#         "date": "2024-03-03",
#         "time": "09:15",
#         "location": "Northside Toyota Service",
#         "available": True
#     },
# ]


# # Optional: Helper functions to manage mock data
# def get_available_service_slots():
#     return [slot for slot in SERVICE_SLOTS if slot["available"]]

from datetime import datetime, timedelta
import random

# Generate mock service appointment slots
def generate_service_slots():
    # Service locations
    locations = [
        "Downtown Toyota Service",
        "Eastside Toyota Service",
        "Westside Toyota Service",
        "Northside Toyota Service",
        "Southside Toyota Service"
    ]
    
    # Service types
    service_types = [
        "Regular Maintenance",
        "Oil Change",
        "Tire Service",
        "Brake Service",
        "Battery Replacement",
        "Engine Diagnostics"
    ]
    
    # Generate dates for the next 7 days
    today = datetime.now()
    slots = []
    
    for i in range(1, 8):  # Next 7 days
        date = today + timedelta(days=i)
        date_str = date.strftime("%A, %B %d, %Y")
        
        # Generate time slots
        times = ["09:00", "10:30", "11:15", "13:00", "14:30", "15:15", "16:30"]
        
        for location in locations:
            # Not all locations have all times
            available_times = random.sample(times, k=random.randint(3, len(times)))
            
            for time in available_times:
                # 70% chance of being available
                is_available = random.random() < 0.7
                
                slot = {
                    "date": date_str,
                    "time": time,
                    "location": location,
                    "available": is_available,
                    "duration": random.choice([30, 45, 60, 90, 120]),
                    "services_available": random.sample(service_types, k=random.randint(3, len(service_types)))
                }
                
                slots.append(slot)
    
    return slots

# Generate the mock service slots
SERVICE_SLOTS = generate_service_slots()

# For debugging
if __name__ == "__main__":
    print(f"Generated {len(SERVICE_SLOTS)} service slots")
    available_slots = [slot for slot in SERVICE_SLOTS if slot["available"]]
    print(f"Available slots: {len(available_slots)}")