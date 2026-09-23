# -*- coding: utf-8 -*-
"""LuoTianyi-TTS - 洛天依（GPT-SoVITS v2Pro 微调）推理封装

用法:
    python synth.py --text "你好呀，我是洛天依。" --lang zh --out output/out.wav

支持语言: zh / ja / en

依赖 GPT-SoVITS 引擎，路径通过环境变量 GSV_ENGINE 指定，或修改下方 DEFAULT_ENGINE。
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# GPT-SoVITS 引擎根目录：优先读环境变量 GSV_ENGINE
DEFAULT_ENGINE = os.path.join(HERE, "engine")
ENGINE = os.environ.get("GSV_ENGINE", DEFAULT_ENGINE)
REPO = os.path.join(ENGINE, "GPT-SoVITS")
GSV = os.path.join(REPO, "GPT_SoVITS")

WEIGHTS = os.path.join(HERE, "weights")
GPT = os.path.join(WEIGHTS, "GPT_weights", "tianyi2-e15.ckpt")
SOVITS = os.path.join(WEIGHTS, "SoVITS_weights", "tianyi2_e8_s128.pth")
REF = os.path.join(HERE, "ref", "ref.wav")
PROMPT_FILE = os.path.join(HERE, "ref", "prompt.txt")

os.environ.setdefault("GSV_NODDP", "1")
os.environ["language"] = "zh"

_links = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Links")
if os.path.isdir(_links):
    os.environ["PATH"] = _links + os.pathsep + os.environ["PATH"]

os.chdir(REPO)
for _p in (REPO, GSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _load_prompt(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def main():
    ap = argparse.ArgumentParser(description="LuoTianyi-TTS inference")
    ap.add_argument("--text", required=True, help="要合成的文本")
    ap.add_argument("--lang", default="zh", choices=["zh", "ja", "en"], help="文本语言")
    ap.add_argument("--out", default=os.path.join(HERE, "output", "out.wav"))
    ap.add_argument("--temp", type=float, default=0.8, help="温度，调低更稳，调高更活")
    ap.add_argument("--top_k", type=int, default=10)
    ap.add_argument("--rep", type=float, default=1.2, help="重复惩罚，念错字或拖长音可上调")
    ap.add_argument("--ref", default=REF, help="参考音频（3-10 秒干净人声）")
    ap.add_argument("--prompt", default=None, help="参考音频对应的文字")
    ap.add_argument("--gpt", default=GPT)
    ap.add_argument("--sovits", default=SOVITS)
    a = ap.parse_args()

    prompt_text = a.prompt if a.prompt is not None else _load_prompt(PROMPT_FILE)

    if not os.path.exists(a.gpt):
        sys.exit("找不到 GPT 权重: %s" % a.gpt)
    if not os.path.exists(a.sovits):
        sys.exit("找不到 SoVITS 权重: %s" % a.sovits)
    if not os.path.exists(a.ref):
        sys.exit("找不到参考音频: %s" % a.ref)

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)

    import soundfile as sf
    from TTS_infer_pack.TTS import TTS, TTS_Config

    cfg = {
        "custom": {
            "bert_base_path": "GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large",
            "cnhuhbert_base_path": "GPT_SoVITS/pretrained_models/chinese-hubert-base",
            "device": "cuda",
            "is_half": True,
            "t2s_weights_path": a.gpt,
            "version": "v2Pro",
            "vits_weights_path": a.sovits,
        }
    }
    tts = TTS(TTS_Config(cfg))
    gen = tts.run({
        "text": a.text,
        "text_lang": a.lang,
        "ref_audio_path": a.ref,
        "prompt_text": prompt_text,
        "prompt_lang": "zh",
        "top_k": a.top_k,
        "top_p": 1,
        "temperature": a.temp,
        "text_split_method": "cut5",
        "batch_size": 1,
        "speed_factor": 1.0,
        "split_bucket": False,
        "return_fragment": False,
        "seed": 1234,
        "parallel_infer": True,
        "repetition_penalty": a.rep,
    })
    for sr, audio in gen:
        sf.write(a.out, audio, sr)
        print("WROTE %s  %.2fs  %dHz" % (a.out, len(audio) / sr, sr))


if __name__ == "__main__":
    main()
