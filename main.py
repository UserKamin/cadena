#!/usr/bin/env python3
"""
Combat Simulator - Main Entry Point

A turn-based combat simulation system with character management,
enemy creation, and various game modes.

Author: Combat Simulator Team
Version: 1.0
"""

from user_interface import UserInterface


def main():
    """Main entry point for the Combat Simulator application"""
    print("Starting Combat Simulator...")
    try:
        ui = UserInterface()
        ui.main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting Combat Simulator...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please report this issue.")


if __name__ == "__main__":
    main()
