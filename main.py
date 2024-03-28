import os
import json
from dotenv import load_dotenv
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from openai import OpenAI

load_dotenv()

client = OpenAI(
	api_key=os.environ.get("OPENAI_API_KEY"),
)

pdf_path = './residential-tenancy-agreement-5.pdf'

images = convert_from_path(pdf_path, dpi=200)

texts = []
for i, image in enumerate(images):
	text = pytesseract.image_to_string(image)
	texts.append(text)

for i, text in enumerate(texts):
  completion = client.chat.completions.create(
    model="gpt-4-turbo-preview",
		messages=[
			{"role": "system", "content": "You are specialised in interpreting forms from text content that has been extracted from a PDF file using OCR."},
			{"role": "user", "content": "I have extracted text from a form inside a PDF, which includes questions, helptext, guidelines, headings etc. I'd like you to tell me what you think the form questions and answer field types are likely to be. I'd like you to present those form questions and answer field types in a JSON format - something similar to { landlord: { name(s): string, address: string... } }."},
			{"role": "user", "content": text}
		]
	)

  content = completion.choices[0].message.content
  # remove code syntax block wrapping
  json_string = content.strip('```json\n').rstrip('\n```')

  data = json.loads(json_string)

  # Write the formatted JSON to the file
  with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)

  print(f"JSON saved to {filename}")
