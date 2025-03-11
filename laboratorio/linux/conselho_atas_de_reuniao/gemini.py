import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env (add this line!)
load_dotenv(verbose=True) 

# Debugging prints (important!)
print("Current Working Directory:", os.getcwd())
print("GEMINI_API_KEY Found:", "GEMINI_API_KEY" in os.environ)
if "GEMINI_API_KEY" in os.environ:
    print("GEMINI_API_KEY (Hidden):", "*" * len(os.environ["GEMINI_API_KEY"]))
else:
    print("GEMINI_API_KEY NOT FOUND in os.environ") 

# Use .get() for safer access
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))  

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-pro-exp-02-05",
  generation_config=generation_config,
)

# Atualize os caminhos para os arquivos na mesma pasta
files = [
  upload_to_gemini("20240215 - ata de reunião 2da4508bedf644e2be4f509c6ae01124.md", mime_type="text/markdown"),
  upload_to_gemini("20240321 - ata de reunião 2bb7360c4e47411aa2f61dcdd61aea16.md", mime_type="text/markdown"),
  upload_to_gemini("20240416 - ata de reunião a9150a9436544ba8a190391d2649d3bb.md", mime_type="text/markdown"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
        "Leia todos os arquivos compartilhados. Elabore um sumário de todos.",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)