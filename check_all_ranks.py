#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to check all existing user ranks and find test users
"""

from pymongo import MongoClient
from config import Config

def main():
    # Connect to MongoDB
    client = MongoClient(Config.MONGO_URI)
    db = client.get_database('EHRMS')
    users_collection = db.users
    
    print("="*80)
    print("ALL USER RANKS IN DATABASE")
    print("="*80)
    
    # Get all unique ranks
    ranks = users_collection.distinct('rank')
    print(f"\nFound ranks: {ranks}")
    
    print("\n" + "="*80)
    print("USERS BY RANK (First 3 of each)")
    print("="*80)
    
    for rank in sorted(ranks):
        print(f"\n{rank}:")
        users = users_collection.find({'rank': rank}).limit(3)
        count = 0
        for user in users:
            count += 1
            username = user.get('username', 'NO USERNAME')
            name = user.get('name', 'NO NAME')
            employee_id = user.get('employee_id', 'NO ID')
            has_password = 'password' in user and user['password']
            station = user.get('station_name', 'NO STATION')
            print(f"  {count}. Username: {username}")
            print(f"     Name: {name}")
            print(f"     Employee ID: {employee_id}")
            print(f"     Station: {station}")
            print(f"     Has Password: {'✓' if has_password else '✗'}")
    
    # Get total counts
    print("\n" + "="*80)
    print("RANK STATISTICS")
    print("="*80)
    for rank in sorted(ranks):
        count = users_collection.count_documents({'rank': rank})
        with_password = users_collection.count_documents({'rank': rank, 'password': {'$exists': True, '$ne': ''}})
        print(f"{rank}: {count} total, {with_password} with passwords")
    
    # Find users with specific roles that can approve leaves
    print("\n" + "="*80)
    print("USERS WHO CAN APPROVE LEAVES (Inspector, SDPO, SP, ASP)")
    print("="*80)
    
    approval_ranks = ['Inspector', 'SDPO', 'SP', 'ASP', 'inspector', 'sdpo', 'sp', 'asp']
    for rank in approval_ranks:
        users = users_collection.find({'rank': {'$regex': f'^{rank}$', '$options': 'i'}}).limit(2)
        for user in users:
            username = user.get('username', 'NO USERNAME')
            name = user.get('name', 'NO NAME')
            rank_val = user.get('rank', 'NO RANK')
            has_password = 'password' in user and user['password']
            print(f"\n  {rank_val}: {name}")
            print(f"    Username: {username}")
            print(f"    Has Password: {'✓' if has_password else '✗'}")
    
    # Find lower ranks who can apply for leave
    print("\n" + "="*80)
    print("USERS WHO CAN APPLY FOR LEAVE (Constable, HC, etc.)")
    print("="*80)
    
    lower_ranks = ['Constable', 'HC', 'ASI', 'SI', 'constable', 'hc', 'asi', 'si']
    for rank in lower_ranks:
        users = users_collection.find({'rank': {'$regex': f'^{rank}$', '$options': 'i'}}).limit(2)
        for user in users:
            username = user.get('username', 'NO USERNAME')
            name = user.get('name', 'NO NAME')
            rank_val = user.get('rank', 'NO RANK')
            has_password = 'password' in user and user['password']
            print(f"\n  {rank_val}: {name}")
            print(f"    Username: {username}")
            print(f"    Has Password: {'✓' if has_password else '✗'}")

if __name__ == '__main__':
    main()
