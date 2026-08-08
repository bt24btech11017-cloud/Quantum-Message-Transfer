from quantum.superdense import transmit_message


def test_all_messages():

    messages = ["00", "01", "10", "11"]

    print("\n===== SUPERDENSE CODING TEST =====\n")

    all_passed = True

    for message in messages:

        circuit, counts, received = transmit_message(message)

        if received == message:
            status = "PASS ✓"
        else:
            status = "FAIL ✗"
            all_passed = False

        print(f"Alice sent   : {message}")
        print(f"Bob received : {received}")
        print(f"Results      : {counts}")
        print(f"Status       : {status}")
        print("-" * 40)

    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED!")


if __name__ == "__main__":
    test_all_messages()