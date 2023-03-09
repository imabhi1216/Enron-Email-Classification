import os
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# Define the directory paths
input_dir_path = r"C:\Users\Abhishek\Desktop\Vlabs_assessment\enron_with_categories\6"
output_dir_path = r"C:\Users\Abhishek\Desktop\Vlabs_assessment\processed\6"

header_pattern = re.compile(r'^From:.*\n|^Subject:.*\n|^Mime-Version:.*\n|^Content-Type:.*\n|^Content-Transfer-Encoding:.*\n|^X-From:.*\n|^X-To:.*\n|^X-cc:.*\n|^X-bcc:.*\n|^X-Folder:.*\n|^X-Origin:.*\n|^X-FileName:.*\n|^Message-ID:.*\n|^Date:.*\n|^Email:', re.MULTILINE)
footer_pattern = re.compile(r'^Forwarded by.*\n|^From:.*\n|^To:.*\n|^Cc:.*\n|^Subject:.*\n', re.MULTILINE)
signature_pattern = re.compile(r'\n\n(Thanks|Regards|Best|Sincerely|Cheers),?\n.*\n*$')
contact_number_pattern = re.compile(r'((\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4})|(\(\d{3}\)\s*\d{3}[-\.\s]??\d{4})|(\d{3}[-\.\s]??\d{4}))(\s*(ext|x|ext.)\s*\d{2,5})?', re.IGNORECASE)
email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
# Define regular expressions to match phone numbers, fax numbers, and email addresses
phone_number_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
fax_number_pattern = re.compile(r'\bfax[: ]*\d{3}[-.]?\d{3}[-.]?\d{4}\b')
# email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
# Define a function to preprocess the text
def preprocess_text(text):
    # Remove header, footer, and signature patterns from text
    to_section_regex = re.compile(r'To:(.*?)Subject:', re.DOTALL)
    to_section_match = to_section_regex.search(text)

    if to_section_match:
        to_section = to_section_match.group(1)
        # Match email addresses
        email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        # Remove emails from "To:" section
        to_section_no_emails = email_regex.sub('', to_section)
        # Remove the original "To:" section from the text and replace it with the filtered version
        text = text.replace(to_section, to_section_no_emails)
        
    cc_section_regex = re.compile(r'Cc:(.*?)Subject:', re.DOTALL)
    cc_section_match = cc_section_regex.search(text)

    if cc_section_match:
        cc_section = cc_section_match.group(1)
        # Remove emails from "Cc:" section
        cc_section_no_emails = email_pattern.sub('', cc_section)
        # Remove the original "Cc:" section from the text and replace it with the filtered version
        text = text.replace(cc_section, cc_section_no_emails)
        
    bcc_section_regex = re.compile(r'Bcc:(.*?)Subject:', re.DOTALL)
    bcc_section_match = bcc_section_regex.search(text)

    if bcc_section_match:
        bcc_section = bcc_section_match.group(1)
        # Remove emails from "Cc:" section
        bcc_section_no_emails = email_pattern.sub('', bcc_section)
        # Remove the original "Cc:" section from the text and replace it with the filtered version
        text = text.replace(bcc_section, bcc_section_no_emails)

    
    # Remove phone numbers, fax numbers, and email addresses
    text = phone_number_pattern.sub('', text)
    text = fax_number_pattern.sub('', text)
    text = email_pattern.sub('', text)
    
    text = header_pattern.sub('', text)
    text = footer_pattern.sub('', text)
    text = signature_pattern.sub('\n', text)

    # Remove all punctuation marks
    # text = text.translate(str.maketrans('', '', string.punctuation))

    # Convert all text to lowercase
    # text = text.lower()
    
    
    # Remove contact numbers
    text = contact_number_pattern.sub('', text)

    # Remove the text after the "Attachment" section
    attachment_section_regex = re.compile(r'attachment(s|)\b', re.IGNORECASE)
    attachment_section_match = attachment_section_regex.search(text)
    if attachment_section_match:
        text = text[:attachment_section_match.start()]

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords
    # stop_words = set(stopwords.words('english'))
    # filtered_tokens = [token for token in tokens if token not in stop_words]

    # # Lemmatize the tokens
    # lemmatizer = WordNetLemmatizer()
    # lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Join the tokens back into a string
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

# Iterate over the files in the input directory
for root, dirs, files in os.walk(input_dir_path):
    for file in files:
        # Check if the file is a text file
        if file.endswith(".txt"):
            # Define the input and output file paths
            input_file_path = os.path.join(root, file)
            output_file_path = os.path.join(output_dir_path, file)
            # Read the input file
            with open(input_file_path, "r") as input_file:
                text = input_file.read()
                # Apply the preprocessing function to the text
                preprocessed_text = preprocess_text(text)
                # Write the preprocessed text to the output file
                with open(output_file_path, "w") as output_file:
                    output_file.write(preprocessed_text)
