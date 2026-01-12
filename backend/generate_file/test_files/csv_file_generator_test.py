import csv
import time
import os
from datetime import datetime

def create_csv_file():
    start_time = time.time()

    # Fake data for testing
    combinations = [
        {"compound_number": 1, "materials": ["A", "B"]},
        {"compound_number": 2, "materials": ["A", "D"]},
        {"compound_number": 3, "materials": ["B", "E"]},
    ]

    job_id = "1234"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    seconds = round(time.time() - start_time, 4)
    combos = "Generated 6 combinations in 0.0001s at 2026-01-11 04:51 AM EST"

    # ---------- PATH TO DESKTOP ----------
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = f"combinations_{job_id}.csv"
    filepath = os.path.join(desktop_path, filename)
    # ------------------------------------

    try:
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            seconds = str(seconds)
            created_at = str(created_at)
            job_id = str(job_id)

            # Metadata rows
            writer.writerow(["Id: "+ job_id + ""])
            writer.writerow(["Created_at: "+ created_at+ ""])
            writer.writerow(["Details: " +combos+ ""])
            writer.writerow([])

            # Column header
            writer.writerow(["compound_number", "materials"])

            # Data rows
            for row in combinations:
                compound_number = row["compound_number"]
                materials_str = " | ".join(row["materials"])
                writer.writerow([compound_number, materials_str])

        print(f"CSV saved to: {filepath}")

    except Exception as e:
        print("Error while saving CSV:", e)

if __name__ == "__main__":
    create_csv_file()
