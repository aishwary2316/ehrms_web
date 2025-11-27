"""
Test script to verify sequential order number generation for Transfer, Leave, and Duty orders.
This will generate sample order numbers to demonstrate the numbering system.
"""

from extensions import mongo
from config import Config
from flask import Flask
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

def get_next_order_number(order_type, year):
    """Generate next sequential order number for the given type and year."""
    with app.app_context():
        # Get or create counter document
        counter = mongo.db.counters.find_one_and_update(
            {'_id': f'{order_type}_{year}'},
            {'$inc': {'sequence': 1}},
            upsert=True,
            return_document=True
        )
        
        sequence = counter.get('sequence', 1)
        
        # Format based on order type
        if order_type == 'transfer':
            return f"{sequence}/1/C-4/RO/{year}"
        elif order_type == 'leave':
            return f"{sequence}/3/D-6/RO/{year}"
        elif order_type == 'duty':
            return f"{sequence}/1/C-4/RO/{year}"
        else:
            return f"{sequence}/{order_type}/{year}"

def display_counters():
    """Display current counter values."""
    with app.app_context():
        print("\n" + "="*60)
        print("CURRENT ORDER NUMBER COUNTERS")
        print("="*60)
        
        counters = list(mongo.db.counters.find({}))
        if not counters:
            print("No counters found yet.")
        else:
            for counter in counters:
                print(f"{counter['_id']}: {counter.get('sequence', 0)}")
        print("="*60 + "\n")

def test_order_generation():
    """Test generating order numbers."""
    current_year = datetime.now().year
    
    print("\n" + "="*60)
    print("TESTING ORDER NUMBER GENERATION")
    print("="*60)
    
    print("\nGenerating 5 Transfer Order Numbers:")
    for i in range(5):
        order_num = get_next_order_number('transfer', current_year)
        print(f"  Transfer Order {i+1}: {order_num}")
    
    print("\nGenerating 5 Leave Order Numbers:")
    for i in range(5):
        order_num = get_next_order_number('leave', current_year)
        print(f"  Leave Order {i+1}: {order_num}")
    
    print("\nGenerating 5 Duty Order Numbers:")
    for i in range(5):
        order_num = get_next_order_number('duty', current_year)
        print(f"  Duty Order {i+1}: {order_num}")
    
    print("\n" + "="*60)

def reset_counters(year=None):
    """Reset all counters for a specific year or all years."""
    if year is None:
        year = datetime.now().year
    
    with app.app_context():
        print(f"\nResetting counters for year {year}...")
        
        result = mongo.db.counters.delete_many({
            '_id': {'$regex': f'.*_{year}$'}
        })
        
        print(f"Deleted {result.deleted_count} counter(s).")
        print("Counters reset successfully!")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("ORDER NUMBER GENERATION TEST SYSTEM")
    print("="*60)
    
    # Display current counters
    display_counters()
    
    # Ask user what to do
    print("\nOptions:")
    print("1. Test order number generation (generates 15 sample numbers)")
    print("2. Display current counters")
    print("3. Reset counters for current year")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        test_order_generation()
        display_counters()
    elif choice == '2':
        display_counters()
    elif choice == '3':
        confirm = input("Are you sure you want to reset counters? (yes/no): ").strip().lower()
        if confirm == 'yes':
            reset_counters()
            display_counters()
        else:
            print("Reset cancelled.")
    elif choice == '4':
        print("\nExiting...")
    else:
        print("\nInvalid choice!")
    
    print("\nDone!")
