import os
import json
import csv

# Directory containing the .jsonld files (change this to your actual directory)
jsonld_directory = "C:/Users/alif2/PycharmProjects/NanoPub"
book_data = []

for filename in os.listdir(jsonld_directory):
    if filename.endswith(".jsonld"):  # Only process .jsonld files
        file_path = os.path.join(jsonld_directory, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                # Extract page count and review score
                title = data.get('name', 'Unknown Title')  # Assuming book title is under 'name'
                pages = data.get('numberOfPages', 'N/A')  # Get numberOfPages or 'N/A' if not available
                rating = data.get('aggregateRating', {}).get('ratingValue', 'N/A')  # Get rating value

                book_data.append({
                    'Title': title,
                    'Pages': pages,
                    'Rating': rating
                })

        except Exception as e:
            print(f"Error reading {filename}: {e}")

if book_data:
    csv_filename = 'book_data.csv'

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Pages', 'Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for book in book_data:
            writer.writerow(book)

    print(f"Data saved to {csv_filename}")
else:
    print("No data extracted.")
