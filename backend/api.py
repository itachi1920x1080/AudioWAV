import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from converter import convert_to_wav  # ⚠️ ប្រើឈ្មោះមុខងារថ្មីដែលយើងទើបកែ

app = FastAPI()

# អនុញ្ញាតឲ្យវេបសាយ Vue (Frontend) របស់អ្នកអាចទាក់ទងមកកាន់ API នេះបាន
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convert")
async def convert_audio(audio: UploadFile = File(...)):
    # ១. កំណត់ឈ្មោះឯកសារ
    original_name = audio.filename
    input_path = f"temp_{original_name}"
    
    # កាត់យកតែឈ្មោះ មិនយកកន្ទុយចាស់ (.mp3) រួចតកន្ទុយ .wav ចូលជំនួសវិញ
    base_name = os.path.splitext(original_name)[0]
    output_name = f"{base_name}.wav"
    output_path = f"converted_{output_name}"

    # ២. រក្សាទុកឯកសារដែល Upload ពីវេបសាយ
    with open(input_path, "wb") as buffer:
        buffer.write(await audio.read())

    # ៣. ដំណើរការបម្លែង
    print(f"កំពុងបម្លែង {input_path}...")
    success = convert_to_wav(input_path, output_path)

    if success:
        # ៤. បញ្ជូនឯកសារ .wav ត្រឡប់ទៅកាន់ Browser វិញដើម្បីឲ្យវា Download
        return FileResponse(
            path=output_path, 
            media_type="audio/wav", 
            filename=output_name
        )
    else:
        return {"error": "មានបញ្ហាក្នុងការបម្លែងឯកសារ"}