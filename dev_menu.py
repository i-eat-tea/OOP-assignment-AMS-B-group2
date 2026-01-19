"""
Developer menu for comprehensive testing
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test import *
from main import interactive_main

def dev_menu():
    """Developer menu for comprehensive testing"""
    bank = None
    
    while True:
        print("\n" + "="*60)
        print("DEVELOPER TEST MENU - COMPREHENSIVE TESTING")
        print("="*60)
        print("1. Run Comprehensive Test (all features)")
        print("2. Quick Test (basic functionality)")
        print("3. Create Demo Bank (pre-populated for manual testing)")
        print("4. Test Exception Handling")
        print("5. Run Normal Interactive System")
        print("6. Exit")
        print("-"*60)
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            print("\nStarting comprehensive test...")
            bank = run_comprehensive_test()
            input("\nPress Enter to continue...")
        elif choice == "2":
            print("\nStarting quick test...")
            bank = quick_test()
            input("\nPress Enter to continue...")
        elif choice == "3":
            print("\nCreating demo bank...")
            bank = create_demo_bank()
            input("\nPress Enter to continue...")
        elif choice == "4":
            print("\nTesting exception handling...")
            test_all_exceptions()
            input("\nPress Enter to continue...")
        elif choice == "5":
            print("\nLaunching interactive system...")
            interactive_main()
        elif choice == "6":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice! Please enter 1-6.")

if __name__ == "__main__":
    dev_menu()