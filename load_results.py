import sys
import os
from util.storage import load_from_path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: No valid path provided. Results cannot be loaded.")
        sys.exit(1)
    
    path: str = sys.argv[1]

    if not os.path.isfile(path):
        click.echo("Error: Invalid path provided")
        sys.exit(1)

    result = load_from_path(path)
    print(f"The requested result has been loaded from {path}. It may be accessed through the `results` object")