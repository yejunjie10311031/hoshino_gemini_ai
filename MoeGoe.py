from scipy.io.wavfile import write
from mel_processing import spectrogram_torch
from text import text_to_sequence, _clean_text
from models import SynthesizerTrn
import utils
import commons
import sys
import re
from torch import no_grad, LongTensor
import logging
from pydub import AudioSegment
import pygame

logging.getLogger('numba').setLevel(logging.WARNING)


def ex_print(text, escape=False):
    if escape:
        print(text.encode('unicode_escape').decode())
    else:
        print(text)


def get_text(text, hps, cleaned=False):
    if cleaned:
        text_norm = text_to_sequence(text, hps.symbols, [])
    else:
        text_norm = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm


def print_speakers(speakers, escape=False):
    if len(speakers) > 100:
        return
    print('ID\tSpeaker')
    for id, name in enumerate(speakers):
        ex_print(str(id) + '\t' + name, escape)


def get_label_value(text, label, default, warning_name='value'):
    value = re.search(rf'\[{label}=(.+?)\]', text)
    if value:
        try:
            text = re.sub(rf'\[{label}=(.+?)\]', '', text, 1)
            value = float(value.group(1))
        except:
            print(f'Invalid {warning_name}!')
            sys.exit(1)
    else:
        value = default
    return value, text


def get_label(text, label):
    if f'[{label}]' in text:
        return True, text.replace(f'[{label}]', '')
    else:
        return False, text


'''if __name__ == '__main__':
    if '--escape' in sys.argv:
        escape = True
    else:
        escape = False'''

model = "G_latest.pth"
config = "finetune_speaker.json"

hps_ms = utils.get_hparams_from_file(config)
n_speakers = hps_ms.data.n_speakers if 'n_speakers' in hps_ms.data.keys() else 0
n_symbols = len(hps_ms.symbols) if 'symbols' in hps_ms.keys() else 0
speakers = hps_ms.speakers if 'speakers' in hps_ms.keys() else ['0']
use_f0 = hps_ms.data.use_f0 if 'use_f0' in hps_ms.data.keys() else False
emotion_embedding = hps_ms.data.emotion_embedding if 'emotion_embedding' in hps_ms.data.keys() else False

net_g_ms = SynthesizerTrn(
    n_symbols,
    hps_ms.data.filter_length // 2 + 1,
    hps_ms.train.segment_size // hps_ms.data.hop_length,
    n_speakers=n_speakers,
    emotion_embedding=emotion_embedding,
    **hps_ms.model)
_ = net_g_ms.eval()
utils.load_checkpoint(model, net_g_ms)

def speak(text,state,button_state):
    ex_print(_clean_text(
        text, hps_ms.data.text_cleaners), True)
    length_scale, text = get_label_value(
        text, 'LENGTH', 1, 'length scale')
    noise_scale, text = get_label_value(
        text, 'NOISE', 0.667, 'noise scale')
    noise_scale_w, text = get_label_value(
        text, 'NOISEW', 0.8, 'deviation of noise')
    cleaned, text = get_label(text, 'CLEANED')

    stn_tst = get_text(text, hps_ms, cleaned=cleaned)

    print_speakers(speakers, False)
    speaker_id = 0
    out_path = "reply.wav"

    with no_grad():
        x_tst = stn_tst.unsqueeze(0)
        x_tst_lengths = LongTensor([stn_tst.size(0)])
        sid = LongTensor([speaker_id])
        audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale,
                                noise_scale_w=noise_scale_w, length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()


    write(out_path, hps_ms.data.sampling_rate, audio)
    state.setText("正在播放语音")
    print("正在播放")
    pygame.mixer.init()
    pygame.mixer.music.load("reply.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    pygame.mixer.quit() 
    print("完成播放")
    state.setText("")
    button_state.setEnabled(True)
