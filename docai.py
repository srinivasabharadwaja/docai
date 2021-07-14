from google.cloud import documentai_v1beta3 as documentai
import os

# TODO(developer): Uncomment these variables before running the sample.
project_id= 'trainingproject-317506'
location = 'us' # Format is 'us' or 'eu'
processor_id = 'e86e251ceea67b81' #  Create processor in Cloud Console
file_path = 'Samples/inv_1.pdf'


def extract_document(project_id: str, location: str, processor_id: str, file_path: str):

    # You must set the api_endpoint if you use a location other than 'us', e.g.:
    opts = {}
    if location == "eu":
        opts = {"api_endpoint": "eu-documentai.googleapis.com"}

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    # Read the file into memory
    with open(file_path, "rb") as pdf:
        image_content = pdf.read()

    document = {"content": image_content, "mime_type": "application/pdf"}

    # Configure the process request
    request = {"name": name, "document": document}

    result = client.process_document(request=request)
    document = result.document

    document_pages = document.pages

    # For a full list of Document object attributes, please reference this page: https://googleapis.dev/python/documentai/latest/_modules/google/cloud/documentai_v1beta3/types/document.html#Document

    # Read the text recognition output from the processor
    print("The document contains the following paragraphs:")
    newdict={}
    for page in document_pages:
        paragraphs = page.form_fields
        for form_field in paragraphs:
            fieldName = get_text(form_field.field_name, document)
            fieldValue = get_text(form_field.field_value, document)
            fieldName=fieldName.replace('\n', '')
            fieldValue=fieldValue.replace('\n', '')
            newdict[fieldName]=fieldValue
    with open('filename.txt', 'w') as file:
        file.write(str(newdict))

def get_text(doc_element: dict, document: dict):
    """
    Document AI identifies form fields by their offsets
    in document text. This function converts offsets
    to text snippets.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in doc_element.text_anchor.text_segments:
        start_index = (
            int(segment.start_index)
            if segment in doc_element.text_anchor.text_segments
            else 0
        )
        end_index = int(segment.end_index)
        response += document.text[start_index:end_index]
    return response


extract_document(project_id, location, processor_id, file_path)
