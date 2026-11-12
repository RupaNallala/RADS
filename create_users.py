"""
Quick script to create test users for AI Road Accident Detection System.
Run: python create_users.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'road_accident.settings')
django.setup()

from django.contrib.auth.models import User

def create_accounts():
    # 1. Administrator Account (Admin Role)
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print(" Successfully created Admin account: username='admin', password='admin123'")
    else:
        print("ℹ️ Admin account 'admin' already exists.")

    # 2. Standard User Account (User Role)
    if not User.objects.filter(username='user1').exists():
        normal_user = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='user123'
        )
        print(" Successfully created Standard User account: username='user1', password='user123'")
    else:
        print("ℹ️ User account 'user1' already exists.")

if __name__ == '__main__':
    create_accounts()
