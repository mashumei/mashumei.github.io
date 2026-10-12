# 马树梅个人 AI 名片网站 · 上线部署指南（GitHub Pages，免费）

> 目标：把现在的静态网站发布到公网，拿到一个 `https://` 链接，别人在微信里点开就能看。
> 本指南零代码改动、零费用。网站文件已全部就绪（index.html / css / js / articles / assets）。

---

## 一、两种 GitHub Pages 形态（任选其一）

| 类型 | 仓库名（必须） | 最终链接 |
|---|---|---|
| **用户页（推荐，链接最短）** | `你的用户名.github.io` | `https://你的用户名.github.io/` |
| **项目页** | 任意，如 `mashumei-card` | `https://你的用户名.github.io/mashumei-card/` |

个人名片推荐用**用户页**：链接干净、好记、显专业。下面以用户页为例，项目页只差仓库名。

---

## 二、方案 A：GitHub Desktop（图形界面，最省心，推荐）

适合不熟悉命令行的同学。

> ✅ **已为你准备好**：网站文件夹已是 git 仓库（已 `git init` + 首次提交，分支 `main`，14 个文件全部纳入）。所以你**不用**再复制文件、不用再 `git init`，直接从第 3 步"Publish"开始。

1. 注册 GitHub 账号：https://github.com/ （记住用户名，链接里会用到）
2. 下载安装 GitHub Desktop：https://desktop.github.com/
3. 发布本地仓库：
   - 打开 GitHub Desktop → **File → Add Local Repository** → 选本文件夹 `E:\鸿雁归巢-运营系统\马树梅个人AI名片网站`
   - 点 **Publish repository**（发布仓库）
   - **Repository name 必须填** `你的用户名.github.io`（如 `mashumei.github.io`）
   - 勾选 **Public**（私有仓库 Pages 要付费）
   - 不要勾 "Keep this code private"
   - 点 Publish
4. 打开 GitHub 网页 → 进该仓库 → **Settings → Pages** → Source 选 `main` 分支 / `/root` → Save
5. 等 1–2 分钟，访问 `https://你的用户名.github.io/` 即可。

> 第一次部署可能要等几分钟才生效，刷新即可。

---

## 三、方案 B：命令行（本机已装 git）

如果你愿意用命令行，我已在本机准备好 git。你可以让我帮你把文件 `git add / commit`，你只负责 `push`（GitHub 现在用 **Personal Access Token** 代替密码，不是登录密码）。

最简流程（在仓库目录内）：
```bash
git init
git add .
git commit -m "个人名片网站上线"
git branch -M main
git remote add origin https://github.com/你的用户名/你的用户名.github.io.git
git push -u origin main
```
然后同样去 Settings → Pages 开启。

> 生成 Token：GitHub 网页 → 右上头像 → Settings → Developer settings → Personal access tokens → 勾 `repo` 权限 → 复制，push 时当密码粘贴（只显示一次，存好）。

---

## 四、拿到链接后，做两件事

1. **替换海报里的占位**：打开 `share-poster.html`，把底部"个人主页即将上线"改成你的真实链接（如 `https://mashumei.github.io/`），可顺手把网站二维码也放上去（生成二维码可用任意在线工具，输入你的链接即可）。
2. **自测**：用手机微信把链接发给自己 → 点开确认中文、排版、按钮、二维码都正常。

---

## 五、微信打开的注意事项（重要）

- GitHub Pages 自带 **https**，微信里通常能直接开。
- 个别情况下微信会对 `github.io` 境外域名提示"请在浏览器打开"——这是微信对境外域名的常规动作，**不影响对方在浏览器打开**，也不影响你正常分享。
- 如果希望微信里**绝对畅通、最显专业**，再走"国内域名 + 备案"方案（见 README 第六部分）：买个域名（几十元/年）+ 国内静态托管（如腾讯云 COS 静态网站 / coding.net）+ ICP 备案（个人免费，约 1–2 周）。

---

## 六、更新内容后如何重新发布

网站是纯静态文件，**改完 index.html / articles / assets 后，重新 Push（或 GitHub Desktop 重新 Commit+Push）即可**，GitHub Pages 会自动更新，无需其他操作。

---

## 七、隐私与安全

- 当前代码不含任何密钥、密码、付费 API。
- 微信二维码、头像、电话均为你主动提供的真实资料，已合规展示。
- 不要在此仓库提交任何私密文件（如未公开合同、客户名单）。
