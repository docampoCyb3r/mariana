import nemo.collections.asr as nemo_asr

asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(model_name="nvidia/parakeet-rnnt-1.1b")

trans = asr_model.transcribe([r'C:\Users\Aero\Desktop\Reconocimiento_1.0 (izzi- val)\CAVQPCJ9K93P51VHBUCS0GCVKK07AV2K_sin_silencios.wav'])

print(trans)
