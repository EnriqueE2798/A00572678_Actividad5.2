"""
Computer Sales
"""

import json
import sys
import time


def load_json(file_path):
    """Loads of the JSON files."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        return None


def compute_total_sales(price_catalogue, sales_record):
    """Computes the total sales cost based on the sales record and price catalogue."""
    total_cost = 0.0
    errors = []
    for sale in sales_record:
        try:
            product_name = sale["Product"]
            quantity = sale["Quantity"]
            product = next((item for item in price_catalogue
                        if item["title"]== product_name), None)
            if product:
                total_cost += product["price"]*quantity
            else:
                errors.append(f"Product '{product_name}' was not found in price catalogue.")
        except KeyError as e:
            errors.append(f"Invalid sale record: Missing key {e} in {sale}.")
        except TypeError:
            errors.append(f"Invalid sale record: Incorrect data type in {sale}.")
    return total_cost, errors


def write_results(total_cost, errors, execution_time):
    """Define de format of the result file"""
    result = f"Total cost sales: ${total_cost:.2f}\n"
    result += f"Execution Time: {execution_time:.6f} seconds\n"
    if errors:
        result += "\nErrors Encountered:\n"
        result += "\n".join(errors)
    print(result)
    with open("sales_results.txt", 'w', encoding='utf-8') as output_file:
        output_file.write(result)


def main():
    """Load JSON files, compute costs, and show results"""
    if len(sys.argv) != 3:
        print("Usage: python compute_sales.py price_catalog.json sales_record.json")
        sys.exit(1)
    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]
    start_time = time.time()
    price_catalogue = load_json(price_catalogue_file)
    sales_record = load_json(sales_record_file)
    total_cost, errors = compute_total_sales(price_catalogue, sales_record)
    execution_time = time.time() - start_time
    write_results(total_cost, errors, execution_time)

if __name__ == "__main__":
    main()
