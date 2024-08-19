import os
import random
import json
from faker import Faker

# Initialize Faker for generating fake data
fake = Faker()

# Generate sample hotels
def generate_sample_hotels(num_hotels):
    hotels = []
    for _ in range(num_hotels):
        hotel = {
            "_id": fake.uuid4(),
            "name": fake.company(),
            "location": f"{fake.city()}, {fake.state_abbr()}",
            "rating": round(random.uniform(1, 5), 1),
            "description": fake.paragraph(nb_sentences=2),
            "price_per_night": random.randint(100, 500),
            "amenities": random.sample(["Free Wi-Fi", "Pool", "Spa", "Gym", "Restaurant", "Bar"], k=3),
            "contact_info": {
                "phone": fake.phone_number(),
                "email": fake.email(),
                "website": fake.url()
            },
            "images": [f"image{i}.jpg" for i in range(1, 4)],
            "reviews": [
                {
                    "reviewer_name": fake.name(),
                    "rating": round(random.uniform(1, 5), 1),
                    "comment": fake.sentence()
                } for _ in range(random.randint(1, 5))
            ],
            "policies": {
                "check_in": f"{random.randint(12, 15)}:00 PM",
                "check_out": f"{random.randint(10, 12)}:00 AM",
                "cancellation": "Free cancellation up to 24 hours before check-in."
            },
            "available_rooms": random.randint(5, 30)
        }
        hotels.append(hotel)
    return hotels

# Generate sample rooms
def generate_sample_rooms(hotels, num_rooms):
    rooms = []
    for _ in range(num_rooms):
        room = {
            "_id": fake.uuid4(),
            "hotel_id": random.choice(hotels)["_id"],
            "room_type": random.choice(["Deluxe Suite", "Standard Room", "Executive Room", "Suite"]),
            "price_per_night": random.randint(100, 500),
            "availability": random.choice([True, False]),
            "description": fake.paragraph(nb_sentences=1),
            "bed_type": random.choice(["King Bed", "Queen Bed", "Double Bed", "Single Bed"]),
            "max_occupancy": random.randint(1, 4),
            "amenities": random.sample(["Mini Bar", "Flat Screen TV", "Jacuzzi", "Balcony", "Air Conditioning"], k=3),
            "images": [f"room{i}.jpg" for i in range(1, 3)],
            "status": random.choice(["Available", "Booked", "Under Maintenance"]),
            "size": f"{random.randint(20, 60)} sqm"
        }
        rooms.append(room)
    return rooms

# Generate and save the sample data
def generate_and_save_sample_data():
    num_hotels = 10
    num_rooms = 30

    # Generate sample hotels and rooms
    hotels = generate_sample_hotels(num_hotels)
    rooms = generate_sample_rooms(hotels, num_rooms)

    # Create JSON directory structure
    json_dir = 'JSON'
    hotels_dir = os.path.join(json_dir, 'hotels')
    rooms_dir = os.path.join(json_dir, 'rooms')

    os.makedirs(hotels_dir, exist_ok=True)
    os.makedirs(rooms_dir, exist_ok=True)

    # Save the data to JSON files
    with open(os.path.join(hotels_dir, 'sample_hotels.json'), 'w') as f:
        json.dump(hotels, f, indent=4)

    with open(os.path.join(rooms_dir, 'sample_rooms.json'), 'w') as f:
        json.dump(rooms, f, indent=4)

if __name__ == "__main__":
    generate_and_save_sample_data()
    print("Sample data generated and saved to 'JSON/hotels/sample_hotels.json' and 'JSON/rooms/sample_rooms.json'.")
