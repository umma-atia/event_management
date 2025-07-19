import os
import django
from faker import Faker
import random
from event.models import Category, Event, Participant

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')  # Replace 'your_project_name' accordingly
django.setup()

  # Replace 'your_app_name' with your app's name

def populate_db():
    fake = Faker()

    # Clear existing data (optional)
    Category.objects.all().delete()
    Event.objects.all().delete()
    Participant.objects.all().delete()

    # Create some categories
    categories = []
    for _ in range(5):
        category = Category.objects.create(
            name=fake.word().capitalize(),
            description=fake.catch_phrase()
        )
        categories.append(category)
    print(f"Created {len(categories)} categories.")

    # Create events
    events = []
    for _ in range(15):
        category = random.choice(categories)
        event = Event.objects.create(
            name=fake.company(),
            description=fake.paragraph(),
            date=fake.date_between(start_date='-30d', end_date='+30d'),
            time=fake.time(),
            location=fake.address(),
            category=category
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # Create participants
    participants = []
    for _ in range(20):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.email()
        )
        participants.append(participant)
    print(f"Created {len(participants)} participants.")

    # Assign participants to events randomly
    for event in events:
        num_participants = random.randint(1, 5)
        selected_participants = random.sample(participants, num_participants)
        for participant in selected_participants:
            participant.events.add(event)
    print("Assigned participants to events.")

    print("Database populated successfully!")

if __name__ == '__main__':
    populate_db()