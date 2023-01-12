import os
import sys
import torch

from InferenceInterfaces.FastSpeech2Interface import InferenceFastSpeech2


def read_texts(model_id, sentence, filename, device="cpu", language="en", speaker_reference=None):
    tts = InferenceFastSpeech2(device=device, model_name=model_id)
    tts.set_language(language)
    if speaker_reference is not None:
        tts.set_utterance_embedding(speaker_reference)
    if type(sentence) == str:
        sentence = [sentence]
    tts.read_to_file(text_list=sentence, file_location=filename)
    del tts


def read_texts_as_ensemble(model_id, sentence, filename, device="cpu", language="en", amount=10):
    """
    for this function, the filename should NOT contain the .wav ending, it's added automatically
    """
    tts = InferenceFastSpeech2(device=device, model_name=model_id)
    tts.set_language(language)
    if type(sentence) == str:
        sentence = [sentence]
    for index in range(amount):
        tts.default_utterance_embedding = torch.zeros(704).float().random_(-40, 40).to(device)
        tts.read_to_file(text_list=sentence, file_location=filename + f"_{index}" + ".wav")


def read_harvard_sentences(model_id, device):
    tts = InferenceFastSpeech2(device=device, model_name=model_id)

    with open("Utility/test_sentences_combined_3.txt", "r", encoding="utf8") as f:
        sents = f.read().split("\n")
    output_dir = "audios/harvard_03_{}".format(model_id)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    for index, sent in enumerate(sents):
        tts.read_to_file(text_list=[sent], file_location=output_dir + "/{}.wav".format(index))

    with open("Utility/test_sentences_combined_6.txt", "r", encoding="utf8") as f:
        sents = f.read().split("\n")
    output_dir = "audios/harvard_06_{}".format(model_id)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    for index, sent in enumerate(sents):
        tts.read_to_file(text_list=[sent], file_location=output_dir + "/{}.wav".format(index))


def read_contrastive_focus_sentences(model_id, device):
    tts = InferenceFastSpeech2(device=device, model_name=model_id)

    with open("Utility/contrastive_focus_test_sentences.txt", "r", encoding="utf8") as f:
        sents = f.read().split("\n")
    output_dir = "audios/focus_{}".format(model_id)
    os.makedirs(output_dir, exist_ok=True)
    for index, sent in enumerate(sents):
        tts.read_to_file(text_list=[sent], file_location=output_dir + "/{}.wav".format(index))


if __name__ == '__main__':
    exec_device = "cuda" if torch.cuda.is_available() else "cpu"
    os.makedirs("audios", exist_ok=True)
    name = input("\nName of the .wav file? (or 'exit')\n")
    if name == "exit":
        sys.exit()
    read_texts(model_id="Quechua",
               sentence="Qantapuni qhawashayki warmiypaq.",
               filename=f"audios/{name}_quechua_test_cloned.wav",
               device=exec_device,
               speaker_reference=f"{name}.wav",
               language="qu")

    read_texts(model_id="Quechua",
               sentence="This is a sentence meant for testing, whether the new vocoder works the way I hope it does.",
               filename=f"audios/{name}_english_test_cloned.wav",
               device=exec_device,
               speaker_reference=f"{name}.wav",
               language="en")

    read_texts(model_id="Quechua",
               sentence="Esta es una oración compleja. Incluso tiene una pausa.",
               filename=f"audios/{name}_spanish_test_cloned.wav",
               device=exec_device,
               speaker_reference=f"{name}.wav",
               language="es")
