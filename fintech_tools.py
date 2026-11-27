

"""
Mock FinTech tools for the Local AI Chatbot.

These functions use dummy data only.
They do not connect to real banking systems.
"""


# --------------------------------------------------
# MOCK ACCOUNT DATA
# --------------------------------------------------

MOCK_ACCOUNTS = {
    "ACC1001": {
        "account_id": "ACC1001",
        "customer_id": "CUST1001",
        "account_type": "SAVINGS",
        "currency": "INR",
        "available_balance": "45000.00",
        "account_status": "ACTIVE"
    },
    "ACC1002": {
        "account_id": "ACC1002",
        "customer_id": "CUST1002",
        "account_type": "CURRENT",
        "currency": "INR",
        "available_balance": "125000.00",
        "account_status": "ACTIVE"
    }
}


# --------------------------------------------------
# MOCK TRANSACTION DATA
# --------------------------------------------------

MOCK_TRANSACTIONS = {
    "TXN1001": {
        "transaction_id": "TXN1001",
        "account_id": "ACC1001",
        "amount": "1500.00",
        "currency": "INR",
        "transaction_type": "UPI",
        "status": "SUCCESS",
        "description": "Electricity bill payment"
    },
    "TXN1002": {
        "transaction_id": "TXN1002",
        "account_id": "ACC1001",
        "amount": "2500.00",
        "currency": "INR",
        "transaction_type": "IMPS",
        "status": "PENDING",
        "description": "Money transfer"
    },
    "TXN1003": {
        "transaction_id": "TXN1003",
        "account_id": "ACC1002",
        "amount": "5000.00",
        "currency": "INR",
        "transaction_type": "NEFT",
        "status": "FAILED",
        "description": "Vendor payment"
    }
}


# --------------------------------------------------
# TOOL 1: GET ACCOUNT SUMMARY
# --------------------------------------------------

def get_account_summary(account_id):

    if not isinstance(account_id, str) or not account_id.strip():
        raise ValueError("A valid account ID is required.")

    account_id = account_id.strip().upper()

    account = MOCK_ACCOUNTS.get(account_id)

    if not account:
        raise ValueError(f"Account {account_id} was not found.")

    return account.copy()


# --------------------------------------------------
# TOOL 2: GET TRANSACTION STATUS
# --------------------------------------------------

def get_transaction_status(transaction_id):

    if not isinstance(transaction_id, str) or not transaction_id.strip():
        raise ValueError("A valid transaction ID is required.")

    transaction_id = transaction_id.strip().upper()

    transaction = MOCK_TRANSACTIONS.get(transaction_id)

    if not transaction:
        raise ValueError(
            f"Transaction {transaction_id} was not found."
        )

    return transaction.copy()


# --------------------------------------------------
# TOOL 3: GET RECENT TRANSACTIONS
# --------------------------------------------------

def get_recent_transactions(account_id, limit=5):

    if not isinstance(account_id, str) or not account_id.strip():
        raise ValueError("A valid account ID is required.")

    if isinstance(limit, bool) or not isinstance(limit, int):
        raise ValueError("Limit must be an integer.")

    if limit < 1 or limit > 10:
        raise ValueError("Limit must be between 1 and 10.")

    account_id = account_id.strip().upper()

    if account_id not in MOCK_ACCOUNTS:
        raise ValueError(f"Account {account_id} was not found.")

    transactions = [
        transaction.copy()
        for transaction in MOCK_TRANSACTIONS.values()
        if transaction["account_id"] == account_id
    ]

    return transactions[:limit]


# --------------------------------------------------
# ALLOWLISTED TOOL REGISTRY
# --------------------------------------------------

AVAILABLE_TOOLS = {
    "get_account_summary": get_account_summary,
    "get_transaction_status": get_transaction_status,
    "get_recent_transactions": get_recent_transactions
}


# --------------------------------------------------
# TOOL EXECUTION CONTROLLER
# --------------------------------------------------

def execute_tool(tool_name, arguments):

    if tool_name not in AVAILABLE_TOOLS:
        raise ValueError(f"Tool '{tool_name}' is not allowed.")

    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be a dictionary.")

    tool_function = AVAILABLE_TOOLS[tool_name]

    return tool_function(**arguments)
