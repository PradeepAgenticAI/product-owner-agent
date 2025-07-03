#!/usr/bin/env python
"""
Export Product State Script.

This script exports feature and story data from the product state markdown document
to CSV files for use in other tools.
"""

import csv
import os
import re
from typing import Dict, List, Any, Tuple

# Configuration
FEATURES_CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "features.csv")
STORIES_CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "stories.csv")
PRODUCT_STATE_PATH = os.path.join(os.path.dirname(__file__), "docs", "09_product_state.md")

# Ensure data directory exists
os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)


def read_markdown_file(file_path: str) -> str:
    """Read the content of a markdown file.

    Args:
        file_path: Path to the markdown file

    Returns:
        Content of the file as a string
    """
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return ""

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def parse_markdown_tables(content: str) -> Dict[str, List[Dict[str, str]]]:
    """Parse markdown tables into structured data.

    Args:
        content: Markdown content as a string

    Returns:
        Dictionary with tables data
    """
    tables = {}
    
    # Parse completed features table
    completed_pattern = r"### Completed Features\s*\n([\s\S]*?)(?=###|$)"
    completed_match = re.search(completed_pattern, content)
    if completed_match:
        tables['completed_features'] = parse_table(completed_match.group(1))
    
    # Parse in-progress features table
    in_progress_pattern = r"### In-Progress Features\s*\n([\s\S]*?)(?=###|$)"
    in_progress_match = re.search(in_progress_pattern, content)
    if in_progress_match:
        tables['in_progress_features'] = parse_table(in_progress_match.group(1))
    
    # Parse planned features table
    planned_pattern = r"### Planned Features \(Next Up\)\s*\n([\s\S]*?)(?=##|$)"
    planned_match = re.search(planned_pattern, content)
    if planned_match:
        tables['planned_features'] = parse_table(planned_match.group(1))
    
    # Parse feature-to-story mapping
    stories = []
    feature_story_pattern = r"### Feature: ([\w\d]+) - ([^\n]+)\s*\n\s*\*\*Description\*\*: ([^\n]+)\s*\n\s*\*\*User Stories\*\*:\s*\n((?:- [\w\d]+ - [^\n]+\s*\n)*)"
    
    for match in re.finditer(feature_story_pattern, content):
        feature_id = match.group(1)
        feature_name = match.group(2)
        story_lines = match.group(4).strip().split('\n')
        
        for line in story_lines:
            if line.strip() and not line.strip().startswith('- No stories'):
                # Extract story ID and description from line like "- S001 - Description"
                story_match = re.match(r'- ([\w\d]+) - (.*)', line.strip())
                if story_match:
                    story_id = story_match.group(1)
                    story_desc = story_match.group(2)
                    stories.append({
                        'StoryID': story_id,
                        'FeatureID': feature_id,
                        'Description': story_desc
                    })
    
    tables['stories'] = stories
    
    return tables


def parse_table(table_content: str) -> List[Dict[str, str]]:
    """Parse a markdown table into a list of dictionaries.

    Args:
        table_content: Markdown table content

    Returns:
        List of dictionaries representing rows in the table
    """
    lines = table_content.strip().split('\n')
    
    # Check if we have at least a header and separator row
    if len(lines) < 2 or 'No ' in lines[0]:
        return []
    
    # Extract headers
    header_match = re.match(r'\|\s*(.+?)\s*\|', lines[0])
    if not header_match:
        return []
    
    headers = [h.strip() for h in header_match.group(1).split('|')]
    
    # Skip the separator row
    rows = []
    for i in range(2, len(lines)):
        line = lines[i].strip()
        if not line or line.startswith('No '):
            continue
            
        # Extract cell values
        cells_match = re.match(r'\|\s*(.+?)\s*\|', line)
        if cells_match:
            cells = [c.strip() for c in cells_match.group(1).split('|')]
            
            # Create a dictionary for this row
            row_dict = {}
            for j, header in enumerate(headers):
                if j < len(cells):
                    row_dict[header] = cells[j]
                else:
                    row_dict[header] = ''
            
            rows.append(row_dict)
    
    return rows


def convert_to_features_csv(tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    """Convert parsed tables to features CSV format.

    Args:
        tables: Dictionary with parsed tables

    Returns:
        List of feature dictionaries in CSV format
    """
    features = []
    
    # Process completed features
    for row in tables.get('completed_features', []):
        feature = {
            'FeatureID': row.get('Feature ID', ''),
            'Name': row.get('Feature Name', ''),
            'Description': row.get('Description', ''),
            'Status': 'Completed',
            'CompletionDate': row.get('Completion Date', ''),
            'RelatedStories': row.get('Related Stories', ''),
            'Progress': '100'
        }
        features.append(feature)
    
    # Process in-progress features
    for row in tables.get('in_progress_features', []):
        feature = {
            'FeatureID': row.get('Feature ID', ''),
            'Name': row.get('Feature Name', ''),
            'Description': row.get('Description', ''),
            'Status': 'In Progress',
            'TargetCompletion': row.get('Target Completion', ''),
            'Progress': row.get('Progress (%)', '').replace('%', ''),
            'RelatedStories': row.get('Related Stories', '')
        }
        features.append(feature)
    
    # Process planned features
    for row in tables.get('planned_features', []):
        feature = {
            'FeatureID': row.get('Feature ID', ''),
            'Name': row.get('Feature Name', ''),
            'Description': row.get('Description', ''),
            'Status': 'Planned',
            'Priority': row.get('Priority', ''),
            'TargetStart': row.get('Target Start', ''),
            'RelatedStories': row.get('Related Stories', '')
        }
        features.append(feature)
    
    return features


def write_csv_file(file_path: str, data: List[Dict[str, str]], fieldnames: List[str]) -> None:
    """Write data to a CSV file.

    Args:
        file_path: Path to the CSV file
        data: List of dictionaries to write
        fieldnames: List of field names for the CSV
    """
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def export_to_csv_files() -> None:
    """Export data from the markdown document to CSV files."""
    # Read markdown content
    markdown_content = read_markdown_file(PRODUCT_STATE_PATH)
    if not markdown_content:
        print("Error: Could not read product state document.")
        return
    
    # Parse markdown tables
    tables = parse_markdown_tables(markdown_content)
    
    # Convert to CSV format
    features = convert_to_features_csv(tables)
    stories = tables.get('stories', [])
    
    # Define fieldnames for CSV files
    feature_fieldnames = ['FeatureID', 'Name', 'Description', 'Status', 'Priority', 
                         'CompletionDate', 'TargetCompletion', 'TargetStart', 'Progress', 'RelatedStories']
    
    story_fieldnames = ['StoryID', 'FeatureID', 'Description', 'Status', 'StoryPoints', 'Sprint', 'Assignee']
    
    # Write to CSV files
    write_csv_file(FEATURES_CSV_PATH, features, feature_fieldnames)
    print(f"Exported {len(features)} features to {FEATURES_CSV_PATH}")
    
    write_csv_file(STORIES_CSV_PATH, stories, story_fieldnames)
    print(f"Exported {len(stories)} stories to {STORIES_CSV_PATH}")


def main() -> None:
    """Main function to run the script."""
    print("Product State Export Script")
    print("==========================")
    
    export_to_csv_files()
    
    print("\nDone!")


if __name__ == "__main__":
    main()
