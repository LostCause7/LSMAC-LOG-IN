#!/usr/bin/env python3
"""
LSMAC Member Check-In System
A barcode scanning application for member check-ins with local database storage.
"""

import sys
import os
from gui import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1) 