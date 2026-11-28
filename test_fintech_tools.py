

from fintech_tools import (
    get_account_summary,
    get_transaction_status,
    get_recent_transactions,
    execute_tool
)


def test_account_summary():

    print("\n========== TEST 1: ACCOUNT SUMMARY ==========")

    result = get_account_summary("ACC1001")

    print(result)

    assert result["account_id"] == "ACC1001"
    assert result["account_status"] == "ACTIVE"

    print("PASS: Account summary test")


def test_transaction_status():

    print("\n========== TEST 2: TRANSACTION STATUS ==========")

    result = get_transaction_status("TXN1002")

    print(result)

    assert result["transaction_id"] == "TXN1002"
    assert result["status"] == "PENDING"

    print("PASS: Transaction status test")


def test_recent_transactions():

    print("\n========== TEST 3: RECENT TRANSACTIONS ==========")

    result = get_recent_transactions("ACC1001", limit=5)

    for transaction in result:
        print(transaction)

    assert len(result) == 2
    assert all(
        transaction["account_id"] == "ACC1001"
        for transaction in result
    )

    print("PASS: Recent transactions test")


def test_invalid_account():

    print("\n========== TEST 4: INVALID ACCOUNT ==========")

    try:
        get_account_summary("ACC9999")
    except ValueError as exc:
        print("Expected error:", exc)
    else:
        raise AssertionError("Invalid account was not rejected")


def test_invalid_transaction():

    print("\n========== TEST 5: INVALID TRANSACTION ==========")

    try:
        get_transaction_status("TXN9999")
    except ValueError as exc:
        print("Expected error:", exc)
    else:
        raise AssertionError("Invalid transaction was not rejected")


def test_unauthorized_tool():

    print("\n========== TEST 6: UNAUTHORIZED TOOL ==========")

    try:
        execute_tool(
            "delete_bank_account",
            {"account_id": "ACC1001"}
        )
    except ValueError as exc:
        print("Expected error:", exc)
    else:
        raise AssertionError("Unauthorized tool was not rejected")


def main():

    test_account_summary()
    test_transaction_status()
    test_recent_transactions()
    test_invalid_account()
    test_invalid_transaction()
    test_unauthorized_tool()

    print("\n====================================")
    print("ALL FINTECH TOOL TESTS COMPLETED")
    print("====================================")


if __name__ == "__main__":
    main()
