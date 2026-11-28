

"""
Tool definitions for the Local AI FinTech Assistant.

These schemas describe the Python functions available
to the LLM through Ollama native tool calling.
"""

TOOLS = [

    # ----------------------------------------------
    # TOOL 1: ACCOUNT SUMMARY
    # ----------------------------------------------

    {
        "type": "function",
        "function": {
            "name": "get_account_summary",

            "description": (
                "Retrieve account information including "
                "account type, available balance, currency "
                "and account status. Use this when the user "
                "asks about an account balance or account details."
            ),

            "parameters": {
                "type": "object",

                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": (
                            "The account identifier, for example ACC1001."
                        )
                    }
                },

                "required": ["account_id"],
                "additionalProperties": False
            }
        }
    },

    # ----------------------------------------------
    # TOOL 2: TRANSACTION STATUS
    # ----------------------------------------------

    {
        "type": "function",
        "function": {
            "name": "get_transaction_status",

            "description": (
                "Retrieve the status and details of a specific "
                "payment transaction. Use this when the user "
                "asks whether a transaction is successful, "
                "pending or failed."
            ),

            "parameters": {
                "type": "object",

                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": (
                            "The transaction identifier, "
                            "for example TXN1002."
                        )
                    }
                },

                "required": ["transaction_id"],
                "additionalProperties": False
            }
        }
    },

    # ----------------------------------------------
    # TOOL 3: RECENT TRANSACTIONS
    # ----------------------------------------------

    {
        "type": "function",
        "function": {
            "name": "get_recent_transactions",

            "description": (
                "Retrieve recent transactions belonging to "
                "a specific account. Use this when the user "
                "asks for transaction history or recent payments."
            ),

            "parameters": {
                "type": "object",

                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": (
                            "The account identifier, "
                            "for example ACC1001."
                        )
                    },

                    "limit": {
                        "type": "integer",
                        "description": (
                            "Maximum number of transactions to retrieve. "
                            "Must be between 1 and 10."
                        ),
                        "default": 5
                    }
                },

                "required": ["account_id"],
                "additionalProperties": False
            }
        }
    }
]
