# LuoTianyi-TTS

洛天依（ルォ・ティエンイー）音色的中文 / 日文 / 英文语音合成模型，基于 **GPT-SoVITS v2Pro** 微调。

仓库只包含**推理代码**。权重见 [Releases](https://github.com/Kevin14827/LuoTianyi-TTS/releases)，训练素材不在此仓库内。

---

## 模型信息

| 项 | 值 |
|---|---|
| 基座 | GPT-SoVITS v2Pro |
| 输出采样率 | 32000 Hz |
| 训练素材 | 演出录音重切 30 段（3–10 秒，合计 221.6 秒） |
| 训练量 | SoVITS 8 epoch / GPT 15 epoch |
| 语言 | 中文、日文、英文 |
| 日语写法 | ルォ・ティエンイー |

### 权重文件

到 [Releases](https://github.com/Kevin14827/LuoTianyi-TTS/releases) 下载最新版本的两个附件：

| 附件 | 大小 | 放到 | MD5 |
|---|---|---|---|
| `tianyi2-e15.ckpt` | ≈148 MB | `weights/GPT_weights/` | `7c4f7051d85b50aace3bd928797c0d44` |
| `tianyi2_e8_s128.pth` | ≈129 MB | `weights/SoVITS_weights/` | `ff5cd8eef78e6b47748ea64eab6c245c` |

MD5：

```bash
certutil -hashfile weights\GPT_weights\tianyi2-e15.ckpt MD5
certutil -hashfile weights\SoVITS_weights\tianyi2_e8_s128.pth MD5
```

权重和 `weights/` 目录都已加入 `.gitignore`，不会被误提交。

---

## 快速开始

### 1. 准备引擎

本仓库**不含** GPT-SoVITS 引擎本体，请自行拉取并放置为 `engine/GPT-SoVITS`：

```bash
git clone https://github.com/RVC-Boss/GPT-SoVITS.git engine/GPT-SoVITS
```

然后按其文档下载预训练模型（`chinese-roberta-wwm-ext-large`、`chinese-hubert-base` 等）。

引擎也可以放在别处，用环境变量指定：

```bash
set GSV_ENGINE=D:\somewhere\engine
```

### 2. 放好权重

仓库里没有 `weights/` 目录，先自己建两个：

```bash
mkdir -p weights/GPT_weights weights/SoVITS_weights
```

从 Releases 下载两个附件，按上表放进去。

### 3. 准备参考音频

推理需要一段 3–10 秒的干净人声作为音色参考。放进 `ref/`：

```
ref/ref.wav       # 3–10 秒，无背景音乐、无混响
ref/prompt.txt    # 与 ref.wav 逐字对应的文字
```


### 4. 合成

```bash
python synth.py --text "你好呀，我是洛天依。好久没跟你说话了。" --lang zh --out output/test.wav
```

日文：

```bash
python synth.py --text "こんにちは、ルォ・ティエンイーです。" --lang ja
```

英文：

```bash
python synth.py --text "Hello, this is Luo Tianyi." --lang en
```

---

## 参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `--text` | 必填 | 要合成的文本 |
| `--lang` | `zh` | `zh` / `ja` / `en` |
| `--out` | `output/out.wav` | 输出路径 |
| `--temp` | `0.8` | 温度。调低更稳，调高语气更活 |
| `--top_k` | `10` | 采样范围 |
| `--rep` | `1.2` | 重复惩罚。念错字、拖长音时上调 |
| `--ref` | `ref/ref.wav` | 参考音频路径 |
| `--prompt` | 读 `ref/prompt.txt` | 参考音频对应文字 |
| `--gpt` / `--sovits` | `weights/...` | 权重路径覆盖 |

**调参经验**

- 语气平：`--temp 0.9`
- 念错字 / 漏字：`--rep 1.3`
- 拖长音收不住：`--rep 1.35 --temp 0.75`

---

## 已知限制

- 长句建议用标点自然断句，`cut5` 会自动切分。
- 音高跨度大的句子（大幅度滑音、喊叫）稳定性会下降。

---

## 声明

- 本仓库的**代码**以 MIT 协议开源，见 `LICENSE`。
- 权重为社区研究用途产出，详见 `NOTICE.md`。使用前请自行确认所在地法律与相关权利方的授权条款。
- 请勿用于冒充真人、伪造音频证据、诈骗等用途。

## 致谢

- [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)
