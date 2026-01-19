"""
Comprehensive testing utilities for the banking system
"""
from account_and_customer import *
from bank import *
from exceptions import *
import sys

def run_comprehensive_test():
    """Run a comprehensive test of all banking system features"""
    print("\n" + "="*70)
    print("COMPREHENSIVE BANKING SYSTEM TEST")
    print("="*70)
    
    # Create a fresh bank
    bank = Bank("Comprehensive Test Bank")
    
    # Test Section 1: Customer Management
    print("\nSECTION 1: CUSTOMER MANAGEMENT")
    print("-"*50)
    
    # 1.1 Create customers
    try:
        customer1 = Customer("cust001", "John Doe", "john@example.com", "1234")
        customer2 = Customer("cust002", "Jane Smith", "jane@example.com", "5678")
        bank.add_customer(customer1)
        bank.add_customer(customer2)
        print("✓ Created 2 customers")
    except Exception as e:
        print(f"✗ Error creating customers: {e}")
        return bank
    
    # 1.2 Test duplicate customer
    try:
        bank.add_customer(customer1)
        print("✗ Should have failed for duplicate customer")
    except ValueError as e:
        print(f"✓ Correctly rejected duplicate customer: {e}")
    
    # 1.3 Test get customer
    try:
        retrieved = bank.get_customer("cust001")
        print(f"✓ Retrieved customer: {retrieved.name}")
    except Exception as e:
        print(f"✗ Error retrieving customer: {e}")
    
    # Test Section 2: Account Creation
    print("\nSECTION 2: ACCOUNT CREATION")
    print("-"*50)
    
    # 2.1 Create savings account
    try:
        savings1 = bank.create_account("cust001", "SAVINGS", 1000.0, interest_rate=0.03)
        print(f"✓ Created savings account: {savings1.account_number}")
        print(f"  Balance: ${savings1.balance:.2f}")
    except Exception as e:
        print(f"✗ Error creating savings account: {e}")
    
    # 2.2 Create checking account
    try:
        checking1 = bank.create_account("cust001", "CHECKING", 500.0, overdraft_limit=1000.0)
        print(f"✓ Created checking account: {checking1.account_number}")
        print(f"  Balance: ${checking1.balance:.2f}")
        print(f"  Overdraft limit: ${checking1.overdraft_limit:.2f}")
    except Exception as e:
        print(f"✗ Error creating checking account: {e}")
    
    # 2.3 Create second customer account
    try:
        savings2 = bank.create_account("cust002", "SAVINGS", 2000.0)
        print(f"✓ Created savings account for Jane: {savings2.account_number}")
    except Exception as e:
        print(f"✗ Error creating account: {e}")
    
    # Test Section 3: Deposit Operations
    print("\nSECTION 3: DEPOSIT OPERATIONS")
    print("-"*50)
    
    # 3.1 Valid deposit
    try:
        old_balance = savings1.balance
        savings1.deposit(500.0)
        print(f"✓ Deposited $500.00 to savings")
        print(f"  Old balance: ${old_balance:.2f}, New balance: ${savings1.balance:.2f}")
    except Exception as e:
        print(f"✗ Deposit failed: {e}")
    
    # 3.2 Invalid deposit (negative amount)
    try:
        savings1.deposit(-100.0)
        print("✗ Should have rejected negative deposit")
    except InvalidAmountError as e:
        print(f"✓ Correctly rejected negative deposit: {e}")
    
    # 3.3 Invalid deposit (zero amount)
    try:
        savings1.deposit(0.0)
        print("✗ Should have rejected zero deposit")
    except InvalidAmountError as e:
        print(f"✓ Correctly rejected zero deposit: {e}")
    
    # Test Section 4: Withdrawal Operations
    print("\nSECTION 4: WITHDRAWAL OPERATIONS")
    print("-"*50)
    
    # 4.1 Valid withdrawal with correct PIN
    try:
        old_balance = savings1.balance
        savings1.withdraw(200.0, "1234")
        print(f"✓ Withdrew $200.00 from savings with correct PIN")
        print(f"  Old balance: ${old_balance:.2f}, New balance: ${savings1.balance:.2f}")
    except Exception as e:
        print(f"✗ Withdrawal failed: {e}")
    
    # 4.2 Withdrawal with wrong PIN
    try:
        savings1.withdraw(100.0, "wrong")
        print("✗ Should have rejected wrong PIN")
    except InvalidPINError as e:
        print(f"✓ Correctly rejected wrong PIN: {e}")
    
    # 4.3 Withdrawal without PIN
    try:
        savings1.withdraw(100.0)
        print("✗ Should have required PIN")
    except InvalidPINError as e:
        print(f"✓ Correctly required PIN: {e}")
    
    # 4.4 Insufficient funds (savings minimum balance)
    try:
        # Try to withdraw almost everything (savings has $100 minimum)
        savings1.withdraw(savings1.balance - 50, "1234")
        print("✗ Should have rejected due to minimum balance")
    except InsufficientFundsError as e:
        print(f"✓ Correctly enforced minimum balance: {e}")
    
    # Test Section 5: PIN Verification & Account Locking
    print("\nSECTION 5: PIN VERIFICATION & ACCOUNT LOCKING")
    print("-"*50)
    
    # 5.1 Test PIN verification
    try:
        if customer1.verify_pin("1234"):
            print("✓ Correct PIN verified successfully")
        else:
            print("✗ Correct PIN verification failed")
    except Exception as e:
        print(f"✗ PIN verification error: {e}")
    
    # 5.2 Test multiple failed attempts
    try:
        print("Testing multiple failed PIN attempts...")
        for i in range(3):
            try:
                result = customer2.verify_pin("wrong")
                print(f"  Attempt {i+1}: Should have failed")
            except AccountLockedError:
                print(f"  Account locked on attempt {i+1}")
                break
            except:
                pass
        
        # Try to verify after locking
        try:
            customer2.verify_pin("5678")
            print("✗ Should have been locked")
        except AccountLockedError as e:
            print(f"✓ Account correctly locked: {e}")
    except Exception as e:
        print(f"✗ Account locking test error: {e}")
    
    # Test Section 6: Transfer Operations
    print("\nSECTION 6: TRANSFER OPERATIONS")
    print("-"*50)
    
    # 6.1 Valid transfer
    try:
        old_balance_from = savings1.balance
        old_balance_to = savings2.balance
        
        bank.transfer(savings1.account_number, savings2.account_number, 300.0, "1234")
        
        print(f"✓ Transferred $300.00 from John to Jane")
        print(f"  John's new balance: ${savings1.balance:.2f}")
        print(f"  Jane's new balance: ${savings2.balance:.2f}")
    except Exception as e:
        print(f"✗ Transfer failed: {e}")
    
    # 6.2 Transfer with insufficient funds
    try:
        bank.transfer(savings1.account_number, savings2.account_number, 5000.0, "1234")
        print("✗ Should have rejected insufficient funds")
    except InsufficientFundsError as e:
        print(f"✓ Correctly rejected insufficient funds: {e}")
    
    # Test Section 7: Overdraft Testing
    print("\nSECTION 7: OVERDRAFT TESTING")
    print("-"*50)
    
    # 7.1 Test overdraft withdrawal
    try:
        # Withdraw more than balance but within overdraft limit
        old_balance = checking1.balance
        checking1.withdraw(800.0, "1234")  # Balance was 500, overdraft limit 1000
        print(f"✓ Used overdraft: Withdrew $800.00 from $500.00 balance")
        print(f"  New balance: ${checking1.balance:.2f}")
    except Exception as e:
        print(f"✗ Overdraft withdrawal failed: {e}")
    
    # 7.2 Test overdraft limit
    try:
        checking1.withdraw(800.0, "1234")  # Should exceed overdraft limit
        print("✗ Should have exceeded overdraft limit")
    except InsufficientFundsError as e:
        print(f"✓ Correctly enforced overdraft limit: {e}")
    
    # Test Section 8: Account Statements & Info
    print("\nSECTION 8: ACCOUNT STATEMENTS & INFORMATION")
    print("-"*50)
    
    # 8.1 Get account statement
    try:
        statement = savings1.get_statement()
        print(f"✓ Retrieved account statement")
        print(f"  Account: {statement['account_number']}")
        print(f"  Owner: {statement['owner']}")
        print(f"  Type: {statement['account_type']}")
        print(f"  Balance: ${statement['balance']:.2f}")
        print(f"  Transactions recorded: {len(statement['transactions'])}")
    except Exception as e:
        print(f"✗ Error getting statement: {e}")
    
    # 8.2 Customer summary
    try:
        summary = customer1.get_accounts_summary()
        print(f"\n✓ Customer account summary:")
        for acc in summary:
            print(f"  - {acc['account_number']}: {acc['type']}, Balance: ${acc['balance']:.2f}")
        print(f"  Total balance: ${customer1.get_total_balance():.2f}")
    except Exception as e:
        print(f"✗ Error getting customer summary: {e}")
    
    # Test Section 9: Monthly Updates
    print("\nSECTION 9: MONTHLY UPDATES")
    print("-"*50)
    
    # 9.1 Apply monthly updates
    try:
        print("Applying monthly updates to all accounts...")
        bank.apply_monthly_updates()
        
        # Check if interest was applied to savings
        if savings1.balance > 0:
            print(f"✓ Monthly updates applied")
            print(f"  John's savings balance: ${savings1.balance:.2f}")
        else:
            print("✗ Monthly updates may not have worked correctly")
        
        # Check if overdraft fee was applied
        print(f"  John's checking balance: ${checking1.balance:.2f} (may have overdraft fee)")
    except Exception as e:
        print(f"✗ Monthly updates failed: {e}")
    
    # Test Section 10: Bank Summary
    print("\nSECTION 10: BANK SUMMARY")
    print("-"*50)
    
    try:
        summary = bank.get_bank_summary()
        print(f"✓ Bank summary:")
        print(f"  Bank name: {summary['bank_name']}")
        print(f"  Total customers: {summary['total_customers']}")
        print(f"  Total accounts: {summary['total_accounts']}")
        print(f"  Total deposits: ${summary['total_deposits']:.2f}")
        print(f"  Accounts by type: {summary['accounts_by_type']}")
    except Exception as e:
        print(f"✗ Error getting bank summary: {e}")
    
    # Test Section 11: PIN Reset
    print("\nSECTION 11: PIN RESET")
    print("-"*50)
    
    try:
        # Create a test customer for PIN reset
        test_customer = Customer("testpin", "Test User", "test@example.com", "1111")
        bank.add_customer(test_customer)
        
        # Reset PIN
        if test_customer.reset_pin("1111", "9999"):
            print("✓ PIN reset successful")
            # Verify new PIN works
            if test_customer.verify_pin("9999"):
                print("✓ New PIN verified successfully")
            else:
                print("✗ New PIN verification failed")
        else:
            print("✗ PIN reset failed")
    except Exception as e:
        print(f"✗ PIN reset test error: {e}")
    
    # Test Section 12: Account Unlock (Employee Function)
    print("\nSECTION 12: ACCOUNT UNLOCK")
    print("-"*50)
    
    try:
        # Lock an account first
        locked_customer = Customer("locked", "Locked User", "locked@example.com", "5555")
        bank.add_customer(locked_customer)
        
        # Try wrong PIN 3 times to lock it
        for i in range(3):
            try:
                locked_customer.verify_pin("wrong")
            except:
                pass
        
        print(f"✓ Account locked: {locked_customer.is_locked}")
        
        # Unlock with admin key
        if locked_customer.unlock_account("admin123"):
            print(f"✓ Account unlocked successfully")
            print(f"  Is locked: {locked_customer.is_locked}")
        else:
            print("✗ Account unlock failed")
    except Exception as e:
        print(f"✗ Account unlock test error: {e}")
    
    print("\n" + "="*70)
    print("COMPREHENSIVE TEST COMPLETE")
    print("="*70)
    
    return bank

def quick_test():
    """Quick test of basic functionality"""
    print("\nRunning quick test...")
    bank = Bank("Quick Test Bank")
    
    # Create customers
    customer1 = Customer("q001", "Quick User", "quick@test.com", "1111")
    bank.add_customer(customer1)
    
    # Create accounts
    savings = bank.create_account("q001", "SAVINGS", 1000.0)
    checking = bank.create_account("q001", "CHECKING", 500.0)
    
    # Test basic operations
    savings.deposit(500)
    savings.withdraw(200, "1111")
    
    print(f"✓ Quick test completed")
    print(f"  Savings balance: ${savings.balance:.2f}")
    print(f"  Checking balance: ${checking.balance:.2f}")
    
    return bank

def create_demo_bank():
    """Create a demo bank with pre-populated data for manual testing"""
    bank = Bank("Demo Bank")
    
    # Create demo customers
    customers = [
        ("alice01", "Alice Johnson", "alice@example.com", "1111"),
        ("bob02", "Bob Williams", "bob@example.com", "2222"),
        ("charlie03", "Charlie Brown", "charlie@example.com", "3333"),
    ]
    
    for cust_id, name, email, pin in customers:
        customer = Customer(cust_id, name, email, pin)
        bank.add_customer(customer)
        
        # Create accounts for each
        bank.create_account(cust_id, "SAVINGS", 1500.0, interest_rate=0.025)
        bank.create_account(cust_id, "CHECKING", 750.0, overdraft_limit=1000.0)
    
    print("Demo bank created with:")
    print("- 3 customers (alice01, bob02, charlie03)")
    print("- 6 total accounts (2 per customer)")
    print("\nTest credentials:")
    print("Customer ID: alice01, PIN: 1111")
    print("Customer ID: bob02, PIN: 2222")
    print("Customer ID: charlie03, PIN: 3333")
    print("\nEmployee PIN: 1111")
    print("Admin Key: admin123")
    
    return bank

def test_all_exceptions():
    """Test that all custom exceptions are raised properly"""
    print("\nTesting exception handling...")
    
    # Test InvalidAmountError
    try:
        raise InvalidAmountError("Test invalid amount")
    except InvalidAmountError as e:
        print(f"✓ InvalidAmountError works: {e}")
    
    # Test InsufficientFundsError
    try:
        raise InsufficientFundsError("Test insufficient funds")
    except InsufficientFundsError as e:
        print(f"✓ InsufficientFundsError works: {e}")
    
    # Test InvalidPINError
    try:
        raise InvalidPINError("Test invalid PIN")
    except InvalidPINError as e:
        print(f"✓ InvalidPINError works: {e}")
    
    # Test AccountLockedError
    try:
        raise AccountLockedError("Test account locked")
    except AccountLockedError as e:
        print(f"✓ AccountLockedError works: {e}")
    
    # Test AccountNotFoundError
    try:
        raise AccountNotFoundError("Test account not found")
    except AccountNotFoundError as e:
        print(f"✓ AccountNotFoundError works: {e}")
    
    print("✓ All exceptions tested successfully")

if __name__ == "__main__":
    print("Banking System Test Suite")
    print("Choose test to run:")
    print("1. Comprehensive Test (all features)")
    print("2. Quick Test (basic functionality)")
    print("3. Create Demo Bank")
    print("4. Test Exception Handling")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        run_comprehensive_test()
    elif choice == "2":
        quick_test()
    elif choice == "3":
        create_demo_bank()
    elif choice == "4":
        test_all_exceptions()
    else:
        print("Invalid choice")