import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

try:
    numerator = float(input("Enter the numerator: "))
    denominator = float(input("Enter the denominator: "))
    result = numerator / denominator
    logging.info(f"The result is {result:.2f}")

except ValueError:
    logging.error("Numerator and Denominator must be numbers")

except ZeroDivisionError:
    logging.error("Denominator cannot be zero")


my_list = [1, 6, 7]

try:
    index = int(input("Enter the index: "))
    logging.info(f"The value from my_list[{index}] is {my_list[index]}")

except ValueError:
    logging.error("Index must be an integer")

except IndexError:
    logging.error("Index is out of range")


finally:
    logging.info("Processing Done!")