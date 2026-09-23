# weights/

推理所需权重放这里。

```
weights/
├── GPT_weights/
│   └── tianyi2-e15.ckpt           155 MB   MD5 7c4f7051d85b50aace3bd928797c0d44
└── SoVITS_weights/
    └── tianyi2_e8_s128.pth        135 MB   MD5 ff5cd8eef78e6b47748ea64eab6c245c
```

校验：

```bash
certutil -hashfile weights\GPT_weights\tianyi2-e15.ckpt MD5
certutil -hashfile weights\SoVITS_weights\tianyi2_e8_s128.pth MD5
```

权重使用前请先读仓库根目录的 `NOTICE.md`。
