import csv

def extract_text(html_content):
    """
    Extracts all text content from HTML.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def write_text_to_csv(text_content, output_file):
    """
    Writes extracted text content to a CSV file.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Text Content'])
        writer.writerow([text_content])

def process_data(html_content, output_file):
    """
    Processes HTML content to extract text and write it to a CSV file.
    """
    text_content = extract_text(html_content)
    write_text_to_csv(text_content, output_file)
    return text_content

# Example usage:
if __name__ == "__main__":
    example_html = """
    <html>
    <body>
    <p>This is a sample paragraph about Python programming.</p>
    <p>Another paragraph mentioning Python and data science.</p>
    </body>
    </html>
    """
    output_file = 'extracted_text.csv'
    extracted_text = process_data(example_html, output_file)
    print(f"Extracted text content has been written to '{output_file}' file.")
