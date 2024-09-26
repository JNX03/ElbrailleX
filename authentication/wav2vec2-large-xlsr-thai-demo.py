import torch
import torchaudio
from datasets import load_dataset
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from pythainlp.tokenize import word_tokenize

test_dataset = load_dataset("mozilla-foundation/common_voice_17_0", "th", split="test[:2%]")

processor = Wav2Vec2Processor.from_pretrained("sakares/wav2vec2-large-xlsr-thai-demo")
model = Wav2Vec2ForCTC.from_pretrained("sakares/wav2vec2-large-xlsr-thai-demo")

resampler = torchaudio.transforms.Resample(48_000, 16_000)

## For Thai NLP Library, please feel free to check https://pythainlp.github.io/docs/2.2/api/tokenize.html
def th_tokenize(batch):
    batch["sentence"] = " ".join(word_tokenize(batch["sentence"], engine="newmm"))
    return batch

# Preprocessing the datasets.
# We need to read the aduio files as arrays
def speech_file_to_array_fn(batch):
    speech_array, sampling_rate = torchaudio.load(batch["path"])
    batch["speech"] = resampler(speech_array).squeeze().numpy()
    return batch

test_dataset = test_dataset.map(speech_file_to_array_fn).map(th_tokenize)
inputs = processor(test_dataset["speech"][:2], sampling_rate=16_000, return_tensors="pt", padding=True)

with torch.no_grad():
    logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits

predicted_ids = torch.argmax(logits, dim=-1)

print("Prediction:", processor.batch_decode(predicted_ids))
print("Reference:", test_dataset["sentence"][:2])
