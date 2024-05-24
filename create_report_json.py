import json
import os

def create_report_json(audio_path,report):
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    json_path = f"reports/{base_name}_report.json"
    with open(json_path, 'w') as json_file:
        json.dump(report, json_file, indent=4)
    print(f"Report saved to {json_path}")