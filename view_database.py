"""Script to view all data stored in the SQLite database."""
import sqlite3
import json
from datetime import datetime

def view_database():
    """Display all data from the SQLite database."""
    
    # Connect to database
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("📄 DOCUMENTS TABLE")
    print("=" * 80)
    
    # Get documents
    cursor.execute("SELECT * FROM documents")
    documents = cursor.fetchall()
    
    if documents:
        print(f"\nFound {len(documents)} document(s):\n")
        for doc in documents:
            print(f"  Document ID: {doc[0]}")
            print(f"  Filename: {doc[1]}")
            print(f"  Upload Time: {doc[2]}")
            print(f"  Chunk Count: {doc[3]}")
            print(f"  Strategy: {doc[4]}")
            print("-" * 80)
    else:
        print("\n  No documents found.\n")
    
    print("\n" + "=" * 80)
    print("📅 BOOKINGS TABLE")
    print("=" * 80)
    
    # Get bookings
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    
    if bookings:
        print(f"\nFound {len(bookings)} booking(s):\n")
        for booking in bookings:
            print(f"  Booking ID: {booking[0]}")
            print(f"  Session ID: {booking[1]}")
            print(f"  Name: {booking[2]}")
            print(f"  Email: {booking[3]}")
            print(f"  Date: {booking[4]}")
            print(f"  Time: {booking[5]}")
            print(f"  Created At: {booking[6]}")
            print("-" * 80)
    else:
        print("\n  No bookings found.\n")
    
    conn.close()
    print("\n✅ Database check complete!\n")

if __name__ == "__main__":
    view_database()
