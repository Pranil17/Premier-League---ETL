import os
import json
import pandas as pd
import importlib.util

# Constants
DATA_DIR = "../data"
OUTPUT_DIR = "../output"
TRANSFORMATIONS_DIR = "transformations"

def extract_data(data_dir):
    """Extract data from all JSON files in the data directory."""
    all_data = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            
            # Extract season from filename (e.g., "season-0910.json" → "09-10")
            season_code = filename.split("-")[-1].split(".")[0]  # "0910"
            season = f"{season_code[:2]}-{season_code[2:]}"  # "09-10"
            
            with open(filepath, "r") as file:
                data = json.load(file)
                df = pd.DataFrame(data)
                df["Season"] = season
                all_data.append(df)
    
    return pd.concat(all_data, ignore_index=True)

def load_transformation_logic(transformation_name):
    """Dynamically load transformation logic from a file."""
    transformation_path = os.path.join(TRANSFORMATIONS_DIR, f"{transformation_name}.py")
    spec = importlib.util.spec_from_file_location(transformation_name, transformation_path)
    transformation_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(transformation_module)
    return transformation_module.transform

def load_data(output_data, output_dir, output_filename):
    """Save the results to a file."""
    os.makedirs(output_dir, exist_ok=True)
    output_data.to_csv(os.path.join(output_dir, output_filename), index=False)

def main(transformation_name):
    # ETL Pipeline
    df = extract_data(DATA_DIR)
    
    # Load transformation logic
    transform_function = load_transformation_logic(transformation_name)
    
    # Apply transformation
    transformed_data = transform_function(df)
    
    # Load data
    output_filename = f"{transformation_name}.csv"
    load_data(transformed_data, OUTPUT_DIR, output_filename)

if __name__ == "__main__":
    import argparse
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run ETL job with specified transformation.")
    parser.add_argument("--transformation", required=True, help="Name of the transformation to apply.")
    args = parser.parse_args()
    
    # Run ETL job
    main(args.transformation)