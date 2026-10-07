from resemblyzer import VoiceEncoder, preprocess_wav
import librosa
import io
import numpy as np 
import streamlit as st


st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr = 16000)
        wav = preprocess_wav(audio)

        embeding = encoder.embed_utterance(wav)
        return embeding.tolist()
    except Exception as e:
        st.error("Voice recog error")
        return None
def identify_speaker(new_embeding, candidates_dict, threshold = 0.65):
    if new_embeding is None or not candidates_dict:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    for sid, stored_embeding in candidates_dict.items():
        if stored_embeding:
            similarity = np.dot(new_embeding, stored_embeding)
            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


def process_bulk_audio(audio_bytes, candidates_dict, threshold = 0.65):
    try:
        embedding = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr = 16000)
        segments =  librosa.effects.split(audio, top_db=30)

        identify_speaker = {}

        for  start, end in segments:
            if (end - start) < sr * 0.5:
                continue
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)

            sid, score = identify_speaker(embedding, candidates_dict, threshold)

            if sid:
                if sid not in identify_speaker or  score > identify_speaker[sid]:
                    identify_speaker[sid] = score

        return identify_speaker
    except Exception as e:
        st.error("Bulk  process error")
        return {}