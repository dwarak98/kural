import whisper


def audio_to_text():
    # choco install ffmpeg

    model = whisper.load_model("base") #{"ta_in": "Tamil"}
    options = dict(language="Tamil", beam_size=5, best_of=5)
    transcribe_options = dict(task="transcribe", **options)
    result = model.transcribe("C:\\Users\\dwara\\OneDrive\\Documents\\projects\\kural\\tests\\out.wav", **transcribe_options)
    print(result["text"])
    file_path = "output.txt"

    # Open the file in write mode ('w')
    with open(file_path, 'w') as file:
        # Write the string to the file
        file.write(result["text"])

    print(f"String has been successfully written to '{file_path}'.")


audio_to_text()
