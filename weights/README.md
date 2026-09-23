# weights/

推理所需权重放这里。**权重不随仓库提交**，从 Releases 下载后按目录放好。

```
weights/
├── GPT_weights/
│   └── tianyi2-e15.ckpt           ≈148 MB   MD5 7c4f7051d85b50aace3bd928797c0d44
└── SoVITS_weights/
    └── tianyi2_e8_s128.pth        ≈129 MB   MD5 ff5cd8eef78e6b47748ea64eab6c245c
```

## 下载

到 [Releases](https://github.com/Kevin14827/LuoTianyi-TTS/releases) 下最新版的两个附件。

用命令行：

```bash
gh release download --repo Kevin14827/LuoTianyi-TTS --pattern "*.ckpt" --dir weights/GPT_weights
gh release download --repo Kevin14827/LuoTianyi-TTS --pattern "*.pth"  --dir weights/SoVITS_weights
```

## 校验

```bash
certutil -hashfile weights\GPT_weights\tianyi2-e15.ckpt MD5
certutil -hashfile weights\SoVITS_weights\tianyi2_e8_s128.pth MD5
```

对不上就是没下完，重下。

## 为什么不用 Git LFS

可以，但会消耗 LFS 免费额度（1 GB 存储 / 1 GB 月流量），两个权重约 290 MB，每次有人 clone 都要走流量。Release 附件不占额度，对这类"下载一次就不动"的静态文件更合适。

权重使用前请先读仓库根目录的 `NOTICE.md`。
