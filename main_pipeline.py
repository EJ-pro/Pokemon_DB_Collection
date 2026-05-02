import subprocess
import sys
import os

def run_script(script_path):
    print(f"\n--- Running {script_path} ---")
    try:
        # Use current python executable to run the scripts
        result = subprocess.run([sys.executable, script_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")
        return False

def main():
    print("Starting Pokemon Data Pipeline Update...")
    
    scripts = [
        "collectors/api_collector.py",
        "processing/data_processor.py",
        "database/db_loader.py"
    ]
    
    for script in scripts:
        if not run_script(script):
            print(f"Pipeline failed at {script}. Aborting.")
            return
            
    print("\n✅ Pokemon Data Pipeline Update Complete!")

if __name__ == "__main__":
    main()
