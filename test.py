"""
This is just a test script to test the functionality made.
Deleted later.
"""
from app import get_cam_feed
import asyncio

asyncio.get_event_loop().run_until_complete(get_cam_feed())