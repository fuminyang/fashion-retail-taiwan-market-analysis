import importlib.util
from pathlib import Path

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    scripts = Path("scripts")

    data_cleaning = load_module("data_cleaning", scripts / "01_data_cleaning.py")
    eda = load_module("eda", scripts / "02_exploratory_analysis.py")
    scoring = load_module("scoring", scripts / "03_taiwan_market_score.py")
    visualizations = load_module("visualizations", scripts / "04_visualizations.py")

    print("Step 1: Cleaning data")
    cleaned = data_cleaning.clean_data()
    print(f"Clean records used: {len(cleaned)}")

    print("Step 2: Creating EDA tables")
    eda.run_eda()

    print("Step 3: Calculating Taiwan Market Potential Score")
    scoring.run_scoring()

    print("Step 4: Creating visualizations")
    visualizations.run_visualizations()

    print("All Python workflow steps completed successfully.")

if __name__ == "__main__":
    main()
