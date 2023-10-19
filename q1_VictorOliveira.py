balance_amount: float = 1000

# Functions
# - Messages
question_title = lambda: print("QUESTION 01 BY VICTOR KAUAN LIMA DE OLIVEIRA")
invalid_operation_message = lambda: print("[ERROR] Invalid operation")

check_account = lambda: print(f"[SUCCESS] Your current balance is: {format_currency(balance_amount)}")
withdraw_success_message = lambda amount: print(f"[SUCCESS] You have withdrawn R$ {format_currency(amount)}")
withdraw_error_message = lambda amount: print(f"[ERROR] Withdraw not allowed for R$ {format_currency(amount)}")
deposit_success_message = lambda amount: print(f"[SUCCESS] You have deposited R$ {format_currency(amount)}")
deposit_error_message = lambda amount: print(f"[ERROR] Deposit not allowed for R$ {format_currency(amount)}")

# - Utilities
is_valid_amount = lambda amount: amount > 0
get_amount = lambda message: float(input(message))
get_operation = lambda: input("Choose an option: ")
format_currency = lambda amount: "R$ {:2,.2f}".format(amount)
value_if_in_iterable = lambda value, iterable: value if value in iterable else None

# - Operations
invalid_operation = lambda: invalid_operation_message() or balance_amount

withdraw = lambda amount: (
    withdraw_success_message(amount) or (balance_amount - amount)
    if amount <= balance_amount and is_valid_amount(amount)
    else withdraw_error_message(amount) or balance_amount
)

deposit = lambda amount: (
    deposit_success_message(amount) or (balance_amount + amount)
    if is_valid_amount(amount)
    else deposit_error_message(amount) or balance_amount
)

withdraw_operation = lambda: withdraw(get_amount("Enter the amount to withdraw: "))
deposit_operation = lambda: deposit(get_amount("Enter the amount to deposit: "))

operation_dict = lambda: {
    None: {"title": "Invalid operation", "function": invalid_operation},
    "1": {"title": "Withdraw", "function": withdraw_operation},
    "2": {"title": "Deposit", "function": deposit_operation},
}

show_menu = lambda: all([
    print(f"{key} - {value['title']}")
    for key, value in operation_dict().items()
    if key is not None
])
run_operation = lambda: operation_dict()[value_if_in_iterable(get_operation(), operation_dict().keys())]["function"]()

if __name__ == "__main__":
    question_title() or print() or show_menu() or print() or check_account() or print()
    balance_amount = run_operation()
    print() or check_account()
