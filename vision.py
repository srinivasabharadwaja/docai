from google.cloud import vision,storage
import io 
import re
bucket_name = "bharadwaja-gcp-training"
storage_client = storage.Client()
def detect_text(uri):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri
    response = client.text_detection(image=image)
    texts = response.text_annotations

    bucket = storage_client.bucket(bucket_name)
    
    # blob.upload_from_string(str(texts))
    print('Texts:')

    full_text = ""
    for text in texts:
        #print('\n"{}"'.format(text.description))
        full_text = full_text+text.description
    print(full_text)
    invoice_number = re.search('INVOICE\n*\s*#\s*(.*)\s*\n*From', full_text)
    if invoice_number:
        invoice_number = invoice_number.group(1)
        print('invoice number:',invoice_number)
    else:
        invoice_number = ""
    blob = bucket.blob('output1.txt')
    blob.upload_from_string(str(full_text))
    blob = bucket.blob('output1_invoice.txt')
    blob.upload_from_string(str(invoice_number))
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

path = "gs://bharadwaja-gcp-training/12340987-1.jpg"
detect_text(path)