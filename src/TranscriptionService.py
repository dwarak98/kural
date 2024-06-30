import whisper

from pyannote.audio import Pipeline
from pyannote_whisper.utils import diarize_text


def audio_to_text():
    # choco install ffmpeg

    model = whisper.load_model("large", device="cuda")  # large
    result = model.transcribe("C:\\Users\\dwara\\OneDrive\\Documents\\projects\\kural\\output_20240629_235615.wav",
                              language="English")  # language="Tamil"
    print(result["text"])
    file_path = "output.txt"
    #
    # # # Open the file in write mode ('w')
    # # with open(file_path, 'w') as file:
    # #     # Write the string to the file
    # #     file.write(result["text"])
    #
    # print(f"String has been successfully written to '{file_path}'.")

    # pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token="")

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token="")

    # send pipeline to GPU (when available)
    import torch
    pipeline.to(torch.device("cuda"))

    diarization_result = pipeline("C:\\Users\\dwara\\OneDrive\\Documents\\projects\\kural\\output_20240629_235615.wav")
    print(diarization_result)

    # print the result
    for turn, _, speaker in diarization_result.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")

    final_result = diarize_text(result, diarization_result)

    for seg, spk, sent in final_result:
        line = f'{seg.start:.2f} {seg.end:.2f} {spk} {sent}'
        print(line)


audio_to_text()
