import pandas as pd
import json
import os
from pathlib import Path

# Read the Excel file
excel_path = "assets/SPSJ Advising Biographies.xlsx"
df = pd.read_excel(excel_path)

# Initialize categories dictionary
categories = {
    "Dental": [],
    "Medical": [],
    "Pharmacy": [],
    "Architecture": [],
    "Occupational Therapy": [],
    "Biomedical Engineering": [],
    "Maths and Academia": [],
    "Military": [],
    "Biology/Academia": [],
    "Clinical Psychology": [],
    "Computer Sciences and AI": [],
    "Electrical Engineering": [],
    "Law": [],
    "Higher Education/Student Affairs": []
}

# Map disciplines to categories
discipline_to_category = {
    "Dentistry": "Dental",
    "Medicine": "Medical",
    "Pharmacy": "Pharmacy",
    "Architecture": "Architecture",
    "Occupational Therapy": "Occupational Therapy",
    "Biomedical Engineering": "Biomedical Engineering",
    "Mathematics": "Maths and Academia",
    "Military": "Military",
    "Biology": "Biology/Academia",
    "PhD": "Biology/Academia",
    "Clinical Psychology": "Clinical Psychology",
    "Psychology": "Clinical Psychology",
    "Computer Science": "Computer Sciences and AI",
    "AI": "Computer Sciences and AI",
    "Electrical Engineering": "Electrical Engineering",
    "Law": "Law",
    "Higher Education": "Higher Education/Student Affairs",
    "Student Affairs": "Higher Education/Student Affairs"
}

# Get list of advisor images
advisor_images_dir = Path("advisors")
image_files = [f.name for f in advisor_images_dir.glob("*") if f.is_file()]

# Process each advisor
advisors_data = []
for _, row in df.iterrows():
    if pd.isna(row.get('Name', '')):
        continue
        
    name = row.get('Name', '').strip()
    discipline = row.get('Industry/Discipline', '').strip() if not pd.isna(row.get('Industry/Discipline', '')) else ''
    bio = row.get('Biography', '').strip() if not pd.isna(row.get('Biography', '')) else ''
    
    # Find the matching image
    name_parts = name.lower().split()
    image_file = None
    for img in image_files:
        img_lower = img.lower()
        if all(part in img_lower for part in name_parts):
            image_file = img
            break
    
    # If no exact match, try partial match
    if not image_file:
        for img in image_files:
            img_lower = img.lower()
            first_name = name_parts[0] if name_parts else ""
            last_name = name_parts[-1] if len(name_parts) > 1 else ""
            if first_name in img_lower and last_name in img_lower:
                image_file = img
                break
    
    # Determine category
    category = None
    for key, value in discipline_to_category.items():
        if key.lower() in discipline.lower():
            category = value
            break
    
    if not category:
        # Default to "Other" if no category is found
        category = "Other"
    
    # Create advisor object
    advisor = {
        "name": name,
        "title": discipline,
        "category": category,
        "image": f"advisors/{image_file}" if image_file else "",
        "bio": bio,
        "email": f"{name.lower().replace(' ', '.')}@example.com",  # Placeholder
        "phone": "555-123-4567",  # Placeholder
        "twitter": name.lower().replace(' ', '')  # Placeholder
    }
    
    advisors_data.append(advisor)
    
    # Add to categories
    if category in categories:
        categories[category].append(advisor)

# Save the data as JSON
with open('advisors_data.json', 'w') as f:
    json.dump(advisors_data, f, indent=2)

# Print summary
print(f"Processed {len(advisors_data)} advisors")
for category, advisors in categories.items():
    print(f"{category}: {len(advisors)} advisors")
