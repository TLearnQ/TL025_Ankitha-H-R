import os
import json
import yaml
import logging
import sys
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "code": getattr(record, 'exception_code', 'INFO')
        })

def setup_logger():
    logger = logging.getLogger("3GPP")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    return logger
logger = setup_logger()


def parse_yaml_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
            logger.info(f"Loaded: {os.path.basename(file_path)}")
            return data
    except Exception as e:
        logger.error(f"Failed to load {file_path}: {e}", extra={'exception_code': 'FILE-ERR'})
        return None
def extract_api_details(data, filename):
    
    if not data: return None
    
    info_section = data.get('info', {})
    paths_section = data.get('paths', {})
    
    result = {
        "filename": filename,
        "title": info_section.get('title', 'No Title'),
        "version": info_section.get('version', '0.0.0'),
        "endpoints": []
    }
    for path, methods in paths_section.items():
        for method, details in methods.items():
            if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                security = details.get('security', [])
                auth_type = list(security[0].keys()) if security else ["None"]
                responses = details.get('responses', {})
                
                result["endpoints"].append({
                    "path": path,
                    "method": method.upper(),
                    "auth": auth_type,
                    "response_codes": list(responses.keys()),
                    "has_response": len(responses) > 0
                })
    return result

def calculate_stats(all_api_data):
    stats = {
        "total_apis": len(all_api_data),
        "total_endpoints": 0,
        "methods": {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0},
        "coverage": 0.0
    }
    
    valid_responses_count = 0

    for api in all_api_data:
        for ep in api['endpoints']:
            stats["total_endpoints"] += 1
            m = ep['method']
            stats['methods'][m] = stats['methods'].get(m, 0) + 1

            if ep['has_response']:
                valid_responses_count += 1

    if stats["total_endpoints"] > 0:
        stats["coverage"] = round((valid_responses_count / stats["total_endpoints"]) * 100, 2)
        
    return stats


def main():
    folder = "ankithayaml"
    all_data = []

    if not os.path.exists(folder):
        print(f"ERROR: Folder '{folder}' missing. Please create it and add .yaml files.")
        return
    
    files = [f for f in os.listdir(folder) if f.endswith(('.yaml', '.yml'))]
    
    if not files:
        print(f"ERROR: No .yaml files found in '{folder}'.")
        return
    for file in files:
        full_path = os.path.join(folder, file)
        raw_yaml = parse_yaml_file(full_path)
        
        if raw_yaml:
            details = extract_api_details(raw_yaml, file)
            all_data.append(details)
    with open("metadata.json", "w") as f:
        json.dump(all_data, f, indent=4)
    logger.info("Created metadata.json")

    summary_stats = calculate_stats(all_data)
    with open("summary.json", "w") as f:
        json.dump(summary_stats, f, indent=4)
    logger.info("Created summary.json")
    
    print("Check metadata.json and summary.json for your results.")

if __name__ == "__main__":
    main()