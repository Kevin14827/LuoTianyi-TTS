# 发布流程

本仓库按设计**需要分发权重**。以下是把仓库推到 GitHub 的步骤。

## 0. 前置

先读根目录 `NOTICE.md`，确认你接受其中的使用与责任说明。

## 1. 本地初始化

```bash
cd LuoTianyi-TTS
git init
git add .
git commit -m "init: LuoTianyi-TTS inference repo"
```

`.gitignore` 已排除 `engine/`、`ref/*.wav`、`output/`，不会误传。

## 2. 权重怎么放

权重单个 135–155 MB，**两个加起来 290 MB**，超过 GitHub 普通仓库单文件 100 MB 的硬限制，必须选一种方式：

### 方案 A：Git LFS（推荐，clone 即得）

```bash
git lfs install
git lfs track "weights/**/*.ckpt" "weights/**/*.pth"
git add .gitattributes
git add weights/GPT_weights/tianyi2-e15.ckpt
git add weights/SoVITS_weights/tianyi2_e8_s128.pth
git commit -m "add: model weights via LFS"
git push
```

注意 LFS 免费额度 1 GB 存储 / 1 GB 月流量，两个权重约 290 MB，够用但要注意流量。

### 方案 B：Release 附件

仓库里只留 `weights/README.md`，权重传到 Release 的 assets 里。好处是不占 LFS 额度，坏处是用户得手动下载放置。

### 方案 C：HuggingFace 镜像

权重传 HuggingFace，仓库 README 里给链接。HF 对模型文件友好，国内访问可以走 `hf-mirror.com`。

```bash
pip install -U huggingface_hub
huggingface-cli upload <你的HF用户名>/LuoTianyi-TTS ./weights --repo-type model
```

## 3. 推送到远端

```bash
git remote add origin git@github.com:<用户名>/LuoTianyi-TTS.git
git branch -M main
git push -u origin main
```

## 4. 发布前自查

- [ ] `git status` 里没有 `ref/*.wav`
- [ ] 没有 `engine/` 目录被误加
- [ ] 没有训练素材、数据集 list 文件
- [ ] 权重 MD5 与 `weights/README.md` 一致
- [ ] `NOTICE.md` 在仓库根目录
- [ ] LICENSE 与 NOTICE 的授权范围不冲突

## 5. 收到 DMCA 怎么办

如果收到下架通知：

1. **不要**反复重推同一内容，会升级为账号处罚。
2. 先读通知，确认是哪一方、针对哪个文件。
3. 有异议走 GitHub 的 counter notice 流程；没异议就移除对应文件并保留代码部分。
4. 三次有效 strike 会封号，别赌。
