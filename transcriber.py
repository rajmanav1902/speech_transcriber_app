import speech_recognition as sr
from pydub import AudioSegment
import os
import io
from concurrent.futures import ThreadPoolExecutor, as_completed

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:05.2f}"

def transcribe_chunk(chunk, start_ms, recognizer):
    try:
        wav_io = io.BytesIO()
        chunk.export(wav_io, format="wav")
        wav_io.seek(0)

        with sr.AudioFile(wav_io) as source:
            audio_listened = recognizer.record(source)
            text = recognizer.recognize_google(audio_listened, language='en-IN')
            start_time = start_ms / 1000.0
            return {
                "start_time": start_time,
                "text": text
            }
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Chunk starting at {start_ms}ms: API request error: {e}")
        return None
    except Exception as e:
        print(f"Chunk starting at {start_ms}ms: Unexpected error: {e}")
        return None

def transcribe_audio(audio_file_path, chunk_length_ms=10000):
    recognizer = sr.Recognizer()
    transcription_results = []

    if not audio_file_path or not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found or path is invalid: {audio_file_path}")

    try:
        audio = AudioSegment.from_file(audio_file_path)
        total_duration_ms = len(audio)
        num_chunks = total_duration_ms // chunk_length_ms + 1

        tasks = []
        with ThreadPoolExecutor() as executor:
            for i in range(num_chunks):
                start_ms = i * chunk_length_ms
                end_ms = min((i + 1) * chunk_length_ms, total_duration_ms)
                chunk = audio[start_ms:end_ms]
                tasks.append(executor.submit(transcribe_chunk, chunk, start_ms, recognizer))

            for future in as_completed(tasks):
                result = future.result()
                if result:
                    transcription_results.append(result)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

    # Sort results by start time (since parallel execution may return out of order)
    transcription_results.sort(key=lambda x: x['start_time'])

    # Format the results into a structured transcript
    formatted_transcript = ""
    for item in transcription_results:
        formatted_time = format_time(item['start_time'])
        formatted_transcript += f"[{formatted_time}]\n{item['text']}\n\n"

    return formatted_transcript

# Optional: still allow running directly
if __name__ == "__main__":
    audio_file = "Java Session 95 Audio.mp3"
    output_text_file = "transcription_output.txt"

    if not os.path.exists(audio_file):
        print(f"\nERROR: The specified audio file '{audio_file}' was not found.")
    else:
        print(f"\nStarting transcription for: {audio_file}")
        transcript = transcribe_audio(audio_file)

        if transcript:
            with open(output_text_file, "w", encoding="utf-8") as f:
                f.write(transcript)
            print(f"Transcription complete. Results saved to {output_text_file}")
        else:
            print("\nNo transcription data generated or an error occurred during transcription.")
