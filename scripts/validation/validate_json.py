#!/usr/bin/env python3
"""
JSON Validation Script for Business Knowledge Repository
Validates JSON files according to established formatting standards
"""

import os
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

class JSONValidator:
    def __init__(self, workspace_path: str = "/workspace"):
        self.workspace_path = Path(workspace_path)
        self.errors = []
        self.warnings = []
        
    def validate_timestamp(self, timestamp_str: str) -> bool:
        """Validate ISO 8601 UTC timestamp format"""
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
        return bool(re.match(iso_pattern, timestamp_str))
    
    def check_required_metadata(self, data: Dict, file_path: str) -> List[str]:
        """Check if required metadata fields are present"""
        errors = []
        
        if 'metadata' not in data:
            errors.append(f"Missing 'metadata' section in {file_path}")
            return errors
            
        metadata = data['metadata']
        required_fields = ['version', 'created_at', 'updated_at', 'last_modified_by', 'file_type', 'encoding']
        
        for field in required_fields:
            if field not in metadata:
                errors.append(f"Missing required metadata field '{field}' in {file_path}")
        
        # Validate timestamp fields
        for timestamp_field in ['created_at', 'updated_at']:
            if timestamp_field in metadata:
                if not self.validate_timestamp(metadata[timestamp_field]):
                    errors.append(f"Invalid timestamp format for '{timestamp_field}' in {file_path}")
        
        return errors
    
    def check_property_order(self, data: Dict, file_path: str) -> List[str]:
        """Check if properties are in the recommended order"""
        warnings = []
        keys = list(data.keys())
        
        # Metadata should be last
        if 'metadata' in keys and keys[-1] != 'metadata':
            warnings.append(f"'metadata' should be the last property in {file_path}")
        
        # Check if id comes first (if present)
        if 'id' in keys and keys[0] != 'id':
            warnings.append(f"'id' should be the first property in {file_path}")
        
        return warnings
    
    def check_json_syntax(self, file_path: str) -> Tuple[bool, Any, str]:
        """Check if JSON file has valid syntax"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return True, data, ""
        except json.JSONDecodeError as e:
            return False, None, str(e)
        except Exception as e:
            return False, None, f"Error reading file: {str(e)}"
    
    def check_formatting(self, file_path: str) -> List[str]:
        """Check JSON formatting (indentation, spacing)"""
        warnings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for tabs (should use spaces)
            if '\t' in content:
                warnings.append(f"Found tabs in {file_path}, should use 2 spaces for indentation")
            
            # Check for trailing commas (basic check)
            if re.search(r',\s*[}\]]', content):
                warnings.append(f"Possible trailing comma detected in {file_path}")
                
        except Exception as e:
            warnings.append(f"Error checking formatting for {file_path}: {str(e)}")
        
        return warnings
    
    def validate_file(self, file_path: str) -> Dict[str, List[str]]:
        """Validate a single JSON file"""
        file_errors = []
        file_warnings = []
        
        # Check JSON syntax
        is_valid, data, error_msg = self.check_json_syntax(file_path)
        
        if not is_valid:
            file_errors.append(f"JSON syntax error: {error_msg}")
            return {"errors": file_errors, "warnings": file_warnings}
        
        # Check required metadata
        file_errors.extend(self.check_required_metadata(data, file_path))
        
        # Check property order
        file_warnings.extend(self.check_property_order(data, file_path))
        
        # Check formatting
        file_warnings.extend(self.check_formatting(file_path))
        
        return {"errors": file_errors, "warnings": file_warnings}
    
    def find_json_files(self) -> List[str]:
        """Find all JSON files in the workspace"""
        json_files = []
        
        for root, dirs, files in os.walk(self.workspace_path):
            # Skip certain directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'test_venv']]
            
            for file in files:
                if file.endswith('.json'):
                    json_files.append(os.path.join(root, file))
        
        return json_files
    
    def validate_all(self) -> Dict[str, Any]:
        """Validate all JSON files in the workspace"""
        json_files = self.find_json_files()
        results = {
            "total_files": len(json_files),
            "valid_files": 0,
            "files_with_errors": 0,
            "files_with_warnings": 0,
            "file_results": {}
        }
        
        for file_path in json_files:
            relative_path = os.path.relpath(file_path, self.workspace_path)
            file_result = self.validate_file(file_path)
            results["file_results"][relative_path] = file_result
            
            if file_result["errors"]:
                results["files_with_errors"] += 1
            elif file_result["warnings"]:
                results["files_with_warnings"] += 1
            else:
                results["valid_files"] += 1
        
        return results
    
    def format_json_file(self, file_path: str, add_metadata: bool = True) -> bool:
        """Format a JSON file according to standards"""
        try:
            is_valid, data, error_msg = self.check_json_syntax(file_path)
            
            if not is_valid:
                print(f"Cannot format {file_path}: {error_msg}")
                return False
            
            # Add metadata if missing and requested
            if add_metadata and 'metadata' not in data:
                current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                data['metadata'] = {
                    "version": "1.0",
                    "created_at": current_time,
                    "updated_at": current_time,
                    "last_modified_by": "Claude AI Assistant",
                    "file_type": "data",
                    "encoding": "UTF-8"
                }
            
            # Write formatted JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')  # Add trailing newline
            
            return True
            
        except Exception as e:
            print(f"Error formatting {file_path}: {str(e)}")
            return False
    
    def print_report(self, results: Dict[str, Any]):
        """Print validation report"""
        print("=" * 80)
        print("JSON VALIDATION REPORT")
        print("=" * 80)
        print(f"Total JSON files found: {results['total_files']}")
        print(f"Valid files: {results['valid_files']}")
        print(f"Files with errors: {results['files_with_errors']}")
        print(f"Files with warnings: {results['files_with_warnings']}")
        print()
        
        # Show files with errors
        if results['files_with_errors'] > 0:
            print("FILES WITH ERRORS:")
            print("-" * 40)
            for file_path, file_result in results['file_results'].items():
                if file_result['errors']:
                    print(f"\n📁 {file_path}")
                    for error in file_result['errors']:
                        print(f"  ❌ {error}")
        
        # Show files with warnings
        if results['files_with_warnings'] > 0:
            print("\nFILES WITH WARNINGS:")
            print("-" * 40)
            for file_path, file_result in results['file_results'].items():
                if file_result['warnings'] and not file_result['errors']:
                    print(f"\n📁 {file_path}")
                    for warning in file_result['warnings']:
                        print(f"  ⚠️ {warning}")
        
        print("\n" + "=" * 80)

def main():
    """Main function to run validation"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        validator = JSONValidator()
        
        if command == "validate":
            results = validator.validate_all()
            validator.print_report(results)
            
            # Exit with error code if there are errors
            if results['files_with_errors'] > 0:
                sys.exit(1)
                
        elif command == "format":
            json_files = validator.find_json_files()
            formatted_count = 0
            
            for file_path in json_files:
                if validator.format_json_file(file_path):
                    formatted_count += 1
                    relative_path = os.path.relpath(file_path, validator.workspace_path)
                    print(f"✅ Formatted: {relative_path}")
            
            print(f"\nFormatted {formatted_count} JSON files")
            
        elif command == "check":
            if len(sys.argv) > 2:
                file_path = sys.argv[2]
                result = validator.validate_file(file_path)
                
                print(f"Validation results for {file_path}:")
                if result['errors']:
                    print("Errors:")
                    for error in result['errors']:
                        print(f"  ❌ {error}")
                
                if result['warnings']:
                    print("Warnings:")
                    for warning in result['warnings']:
                        print(f"  ⚠️ {warning}")
                
                if not result['errors'] and not result['warnings']:
                    print("✅ File is valid!")
            else:
                print("Usage: python validate_json.py check <file_path>")
        else:
            print("Usage:")
            print("  python validate_json.py validate    - Validate all JSON files")
            print("  python validate_json.py format     - Format all JSON files")
            print("  python validate_json.py check <file> - Check specific file")
    else:
        print("Usage:")
        print("  python validate_json.py validate    - Validate all JSON files")
        print("  python validate_json.py format     - Format all JSON files")
        print("  python validate_json.py check <file> - Check specific file")

if __name__ == "__main__":
    main()