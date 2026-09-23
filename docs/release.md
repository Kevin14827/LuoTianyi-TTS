# 发布流程

**本仓库采用的方案：权重走 Release 附件，仓库只存代码和文档。**

## 0. 前置

先读根目录 `NOTICE.md`，确认你接受其中的使用与责任说明。

## 1. 为什么权重不进仓库

| 文件 | 大小 | GitHub 限制 |
|---|---|---|
| `tianyi2-e15.ckpt` | ≈148 MB | 单文件超 100 MB，`push` 直接被拒（`GH001`） |
| `tianyi2_e8_s128.pth` | ≈129 MB | 同上 |

而且一旦用普通提交写进 history，文件会永久留在 `.git` 里，`git rm` 也不会让仓库变小，除非用 `filter-repo` 重写全部历史（所有 commit hash 全变）。

所以走 Release 附件：不占 LFS 额度，不污染 git history。

## 2. 发 Release

```powershell
$env:HTTPS_PROXY="http://127.0.0.1:10809"    # 需要代理才连得上 GitHub
$gh = "C:\Program Files\GitHub CLI\gh.exe"

& $gh release create v1.0.0 `
  --title "LuoTianyi-TTS v1.0.0" `
  --notes "GPT-SoVITS v2Pro 微调权重（32kHz / zh-ja-en）。使用前请阅读 NOTICE.md。" `
  "C:\Users\c0810\Desktop\LuoTianyi_TTS\GPT_weights\tianyi2-e15.ckpt" `
  "C:\Users\c0810\Desktop\LuoTianyi_TTS\SoVITS_weights\tianyi2_e8_s128.pth"
```

`gh` 会打印 assets 的上传结果和 release 页面地址。

**注意**：`--notes` 里别写任何"官方""授权"之类的措辞，也别承诺商用可用。

## 3. 校验

```powershell
& $gh release view v1.0.0 --repo Kevin14827/LuoTianyi-TTS
& $gh release download v1.0.0 --repo Kevin14827/LuoTianyi-TTS --dir /tmp/check
```

下回来的两个文件对一遍 MD5，应该和 `weights/README.md` 里写的一致：

```
7c4f7051d85b50aace3bd928797c0d44  tianyi2-e15.ckpt
ff5cd8eef78e6b47748ea64eab6c245c  tianyi2_e8_s128.pth
```

## 4. 日常改文档

代码和文档照常走 git：

```bash
git add .
git commit -m "docs: ..."
git push
```

`.gitignore` 已排除 `engine/`、`ref/*.wav`、`output/`，不会误传。

## 5. 发布前自查

- [ ] `git status` 里没有 `ref/*.wav`
- [ ] 没有 `engine/` 目录被误加
- [ ] 没有训练素材、数据集 list 文件
- [ ] Release 两个附件 MD5 与 `weights/README.md` 一致
- [ ] `NOTICE.md` 在仓库根目录
- [ ] LICENSE（代码 MIT）与 NOTICE（权重声明）范围没冲突
- [ ] Release notes 里没有授权类措辞

## 6. 备选方案

**Git LFS**：`git lfs track "weights/**/*.ckpt" "weights/**/*.pth"` 后再 `git add weights/`。
好处是 clone 即得权重；坏处是消耗 LFS 免费额度（1 GB 存储 / 1 GB 月流量），每次 clone 都走流量。

**HuggingFace 镜像**：权重传 HF，README 给链接。国内可走 `hf-mirror.com`。

## 7. 收到 DMCA 怎么办

1. **不要**反复重推同一内容，会升级为账号处罚。
2. 先读通知，确认是哪一方、针对哪个文件。
3. 有异议走 GitHub 的 counter notice 流程；没异议就移除对应附件，保留代码部分。
4. 三次有效 strike 会封号，别赌。
