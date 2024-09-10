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
    dict_key_date_added = "Investor Date Added"
    dict_key_investor_type = "Investor Type"
    dict_key_investor_country = "Investor Country"

    try:
        for row in investor_data:
             # Check if the required keys exist in the row
            if dict_key_name in row and dict_key_amt in row:
                investor_name = row[dict_key_name]

                if investor_name not in investor_commitments:
                    investor_commitments[investor_name] = {
                    "total_commitment_amt": 0.0,
                    dict_key_date_added: row.get(dict_key_date_added, None),
                    dict_key_investor_type: row.get(dict_key_investor_type, None),
                    dict_key_investor_country: row.get(dict_key_investor_country, None)
                }
                try:
                    # Convert commitment amount to float; skip if conversion fails
                    commitment_amount = float(row[dict_key_amt])
                    investor_commitments[investor_name]["total_commitment_amt"] += commitment_amount

                except ValueError:
                    print(f"Warning: Skipping non-numeric commitment amount '{row[dict_key_amt]}' for {investor_name}.")
                    continue
            
          # Restructure the results into the desired format
        result = [
            {
                "investorName": name,
                "totalCommitmentAmt": details["total_commitment_amt"],
                "dateAdded": details[dict_key_date_added],
                "investorType": details[dict_key_investor_type],
                "investorCountry": details[dict_key_investor_country]
            }
            for name, details in investor_commitments.items()
        ]

        return result

    except KeyError as ke:
        print(f"Error: Missing key in the data - {ke}.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def get_investor_commitment_list (investor_name):
    try:
        # Load data using the previously defined function
        data = load_csv()

        # List to store commitment details for the specified investor
        commitment_details = []

        for row in data:
            # Check if the row belongs to the specified investor
            if row.get('Investor Name') == investor_name:
                # Extract relevant details
                commitment_detail = {
                    "commitmentAssetClass": row.get("Commitment Asset Class", None),
                    "commitmentCurrency": row.get("Commitment Currency", None),
                    "commitmentAmount": row.get("Commitment Amount", None)
                }


                # Add the detail to the list
                commitment_details.append(commitment_detail)

        # Check if any data was found for the investor
        if not commitment_details:
            print(f"No commitment details found for investor '{investor_name}'.")

        return commitment_details

    except KeyError as ke:
        print(f"Error: Missing key in the data - {ke}.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def filter_commitments_by_asset_class(asset_class, investor_name):
    
    commitment_details = get_investor_commitment_list(investor_name)

    try:
        if not asset_class:
            raise ValueError("Asset class argument cannot be empty.")

        # Filter the commitment details by the specified asset class
        filtered_commitments = [
            detail for detail in commitment_details
            if detail.get("commitmentAssetClass") == asset_class
        ]
        print(commitment_details)
        # Check if any commitments match the specified asset class
        if not filtered_commitments:
            print(f"No commitments found for {investor_name} of asset class '{asset_class}'.")

        return filtered_commitments

    except ValueError as ve:
        print(f"Error: {ve}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise