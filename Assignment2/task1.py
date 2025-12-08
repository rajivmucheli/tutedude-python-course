from decimal import Decimal, ROUND_HALF_UP
from typing import Optional


class InsufficientFundsError(Exception):
    """Raised when a withdrawal amount exceeds the account balance."""


class BankAccount:
    """Simple bank account supporting check_balance, deposit, and withdraw.

    Balances are stored as `Decimal` (two decimal places) to avoid
    floating-point rounding issues with money.
    """

    def __init__(self, owner: str, initial_balance: Optional[Decimal] = None) -> None:
        self.owner = owner
        self._balance = (Decimal(initial_balance) if initial_balance is not None else Decimal('0.00'))
        self._balance = self._quantize(self._balance)

    @staticmethod
    def _quantize(amount: Decimal) -> Decimal:
        return amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def check_balance(self) -> Decimal:
        """Return the current account balance as Decimal (two places)."""
        return self._balance

    def deposit(self, amount: Decimal) -> Decimal:
        """Deposit `amount` into the account and return the new balance.

        `amount` may be a Decimal or a number convertible to Decimal.
        """
        amt = self._quantize(Decimal(amount))
        if amt <= Decimal('0.00'):
            raise ValueError('Deposit amount must be positive.')
        self._balance = self._quantize(self._balance + amt)
        return self._balance

    def withdraw(self, amount: Decimal) -> Decimal:
        """Withdraw `amount` from the account and return the new balance.

        Raises `InsufficientFundsError` if funds are insufficient.
        """
        amt = self._quantize(Decimal(amount))
        if amt <= Decimal('0.00'):
            raise ValueError('Withdrawal amount must be positive.')
        if amt > self._balance:
            raise InsufficientFundsError('Insufficient funds for this withdrawal.')
        self._balance = self._quantize(self._balance - amt)
        return self._balance


def _demo_and_selftest() -> None:
    acct = BankAccount('Alice', initial_balance=Decimal('100.00'))
    print(f"Created account for {acct.owner} with balance {acct.check_balance()}")

    # Deposit
    new_bal = acct.deposit(Decimal('25.50'))
    print(f"After deposit of 25.50: balance = {new_bal}")
    assert new_bal == Decimal('125.50')

    # Withdraw
    new_bal = acct.withdraw(Decimal('20.75'))
    print(f"After withdrawal of 20.75: balance = {new_bal}")
    assert new_bal == Decimal('104.75')

    # Withdraw exact remaining funds check
    acct.deposit(Decimal('0.25'))
    assert acct.check_balance() == Decimal('105.00')

    # Insufficient funds
    try:
        acct.withdraw(Decimal('200.00'))
    except InsufficientFundsError:
        print('InsufficientFundsError raised as expected for large withdrawal')
    else:
        raise AssertionError('InsufficientFundsError not raised')

    print('All self-tests passed.')


def _print_help() -> None:
    print('Commands:')
    print('  balance | b                 Show current balance')
    print('  deposit AMOUNT | d AMOUNT   Deposit AMOUNT (e.g. 10.50)')
    print('  withdraw AMOUNT | w AMOUNT  Withdraw AMOUNT')
    print('  owner NAME                  Set account owner name')
    print('  help | h                    Show this help')
    print('  quit | exit | q             Exit the interactive prompt')


def run_interactive(owner: str = 'User', initial: Decimal = Decimal('0.00')) -> None:
    acct = BankAccount(owner, initial_balance=initial)
    print(f"Interactive banking for {acct.owner}. Type 'help' for commands.")

    while True:
        try:
            line = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nExiting.')
            break

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()

        if cmd in ('quit', 'exit', 'q'):
            print('Goodbye.')
            break
        if cmd in ('help', 'h', '?'):
            _print_help()
            continue

        if cmd in ('balance', 'b'):
            print(f'Balance: {acct.check_balance()}')
            continue

        if cmd in ('deposit', 'd'):
            if len(parts) < 2:
                print("Usage: deposit AMOUNT")
                continue
            try:
                amt = Decimal(parts[1])
                new_bal = acct.deposit(amt)
                print(f'Deposited {amt}, new balance: {new_bal}')
            except Exception as e:
                print('Error:', e)
            continue

        if cmd in ('withdraw', 'w'):
            if len(parts) < 2:
                print("Usage: withdraw AMOUNT")
                continue
            try:
                amt = Decimal(parts[1])
                new_bal = acct.withdraw(amt)
                print(f'Withdrew {amt}, new balance: {new_bal}')
            except InsufficientFundsError as e:
                print('Error:', e)
            except Exception as e:
                print('Error:', e)
            continue

        if cmd == 'owner':
            if len(parts) < 2:
                print('Usage: owner NAME')
                continue
            acct.owner = ' '.join(parts[1:])
            print(f"Owner set to: {acct.owner}")
            continue

        print(f"Unknown command: {cmd}. Type 'help' for commands.")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Simple interactive banking demo')
    parser.add_argument('--test', action='store_true', help='Run non-interactive self-tests and exit')
    parser.add_argument('--owner', default='User', help='Owner name for interactive session')
    parser.add_argument('--initial', default='0.00', help='Initial balance for interactive session (e.g. 100.00)')
    args = parser.parse_args()

    if args.test:
        _demo_and_selftest()
    else:
        try:
            init = Decimal(args.initial)
        except Exception:
            print('Invalid --initial amount; defaulting to 0.00')
            init = Decimal('0.00')
        run_interactive(owner=args.owner, initial=init)

