from Models.InvestorModel import Investor
import logging
import csv


def load_csv(file_path = './InvestData/data.csv'):
    data = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                raise ValueError("CSV file is empty or does not have a header row.")
            for row in reader:
                data.append(row)
        if not data:
            raise ValueError("CSV file contains only the header row or is empty.")
        return data
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
        raise
    except ValueError as ve:
        print(f"Error: {ve}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def sort_by_investor_name():
    investor_data = load_csv()
    investor_commitments = {}
    dict_key_name = "Investor Name"
    dict_key_amt = "Commitment Amount"

    try:
        for row in investor_data:
             # Check if the required keys exist in the row
            if dict_key_name in row and dict_key_amt in row:
                investor_name = row[dict_key_name]
                try:
                    # Convert commitment amount to float; skip if conversion fails
                    commitment_amount = float(row[dict_key_amt])
                except ValueError:
                    print(f"Warning: Skipping non-numeric commitment amount '{row[dict_key_amt]}' for {investor_name}.")
                    continue
                # Add commitment amount to the investor's total
                if investor_name in investor_commitments:
                    investor_commitments[investor_name] += commitment_amount
                else:
                    investor_commitments[investor_name] = commitment_amount


        result = [
            {"investor_name": name, "total_commitment_amt": amount}
            for name, amount in investor_commitments.items()
        ]

        return result
    except KeyError as ke:
        print(f"Error: Missing key in the data - {ke}.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise