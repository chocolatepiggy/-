# 🚢 PortMasters

> 🌍 **Bilingual Documentation** | This README is provided in both **English** and **Simplified Chinese**. Each section contains parallel translations for easy reference.
> 🌏 **双语说明** | 本文档提供**英文**与**简体中文**对照版本。每个章节均采用双语排版，方便不同语言的玩家快速查阅。

---

## 📖 1. Overview / 游戏简介

**EN:** Welcome to **PortMasters**! Set sail during the Golden Age of exploration along the historic Maritime Silk Road. Manage resources, hire artisans to craft valuable goods, fulfill trade orders at bustling ports, and navigate economic challenges like taxes and maintenance costs. Your goal is to accumulate wealth and reputation across 8 voyages to become the ultimate trading mogul.

**CN:** 欢迎来到 **PortMasters（港口大师）**！扬帆起航于大航海时代，穿梭于历史悠久的海上丝绸之路上。管理资源，雇佣工匠制作高价值商品，在繁华港口完成贸易订单，并应对税收与维护成本等经济挑战。你的目标是在 8 次航程中积累财富与声望，成为终极商业巨头。

---

## 🛠️ 2. Installation & Running / 安装与运行

### ✅ Prerequisites / 前置要求
- **Python 3.8+** installed on your machine. / 已安装 Python 3.8 或以上版本。
- **No external libraries required.** Uses standard `tkinter`, `json`, `random` modules. / **无需额外依赖库**，仅使用 Python 标准库。
- **OS:** Windows, macOS, or Linux. / 支持 Windows、macOS 或 Linux 系统。

### 🚀 Steps to Run / 运行步骤
1. Download or clone the project folder. / 下载或克隆项目文件夹。
2. Open your terminal or command prompt. / 打开终端或命令提示符。
3. Navigate to the project directory. / 进入项目目录。
4. Run the main script: / 运行主程序：
   ```bash
   python PortMasters.py
   ```
   *(Note: Replace `PortMasters.py` with your actual versioned filename if applicable. / 注：若文件带版本号，请替换为实际文件名)*
5. Enjoy your voyage! 🌊 / 祝您航海愉快！🌊

---

## 🎮 3. Gameplay Mechanics / 游戏机制

The game spans **8 Voyages**, each divided into **4 Phases**. / 游戏共包含 **8 次航程**，每次航程分为 **4 个阶段**。

| Phase / 阶段 | Description (EN) / 英文描述 | 描述 (CN) / 中文描述 |
|:---|:---|:---|
| **Phase 1** | **Port Purchase**: Buy raw materials or finished goods at ports. | **港口采购**：在港口购买原材料或成品。 |
| **Phase 2** | **Trade Transaction**: Fulfill customer orders for gold & reputation. | **贸易交易**：完成客户订单以获取金币与声望。 |
| **Phase 3** | **Maintenance & Wages**: Pay ship upkeep and worker salaries. | **维护与工资**：支付船只维护费与工匠薪资。 |
| **Phase 4** | **Ship Upgrade**: Level up your ship to reduce future freight costs. | **船只升级**：提升船只等级以降低后续运输成本。 |

### 📦 Resources / 资源类型
- **Raw Materials / 原材料**
  - `Hemp / 麻布` – Base material for basic clothing. / 基础服装原料。
  - `Silk / 丝绸` – Premium fabric for high-end goods. / 高端商品面料。
  - `Tea / 茶叶` – Luxury beverage used in sachets. / 制作香囊的奢侈饮品。
- **Finished Goods / 成品**
  - `Linen Clothes / 麻衣` – Simple clothing (crafted by Weaver). / 基础服装（织女制作）。
  - `Cotton Clothes / 布衣` – Mid-tier clothing (crafted by Weaver). / 中级服装（织女制作）。
  - `Brocade / 绫罗绸缎` – High-value fabric (crafted by Master Weaver). / 高价值织物（纺织大师制作）。
  - `Sachet / 香囊` – Luxury fragrant pouch (crafted by Maker). / 奢侈香囊（香囊师制作）。

### 👷 Worker System / 工匠系统
- **Weavers / 织女**: Craft Linen & Cotton clothes. Wage: 8 Gold/Round. / 制作麻衣与布衣。薪资：8金币/回合。
- **Master Weavers / 纺织大师**: Craft Linen, Cotton & Brocade. Wage: 12 Gold/Round. / 可制作麻衣、布衣与绫罗绸缎。薪资：12金币/回合。
- **Sachet Makers / 香囊师**: Craft Sachets only. Wage: 20 Gold/Round. / 仅制作香囊。薪资：20金币/回合。
- **Skilling Up / 熟练度提升**: Workers gain efficiency after producing enough items, temporarily doubling output at a higher wage. / 工人累计生产足够物品后将升级，产出翻倍，但薪资临时增加。

### 💰 Taxes & Finance / 税收与财务
- **VAT / 增值税**: ~5% on Finished Goods profits. / 约5%，针对成品利润征收。
- **Income Tax / 所得税**: ~10% on voyage net profit. / 约10%，针对航程净利润征收。
- **Freight Costs / 运输费**: Based on item quantity minus Ship Level discount. Formula: `max(5, Items×2 - ShipLevel×5)` / 根据货物数量计算，扣除船只等级折扣。公式：`max(5, 货物数量×2 - 船只等级×5)`

---

## ⌨️ 4. Controls / 操作指南

### ⚡ Keyboard Shortcuts / 键盘快捷键
| Key / 按键 | Action (EN) / 功能 (CN) |
|:---|:---|
| `Ctrl + S` | Save Game / 保存进度 |
| `Ctrl + N` | Next Phase / 进入下一阶段 |
| `Ctrl + H` | Worker Management / 工匠管理界面 |
| `Ctrl + R` | Restart Game / 重新开始游戏 |
| `F1` | Help Instructions / 帮助指南 |

### 🖱️ Mouse Usage / 鼠标操作
- Click buttons to confirm actions (Buy, Trade, Upgrade). / 点击按钮确认操作（购买、交易、升级）。
- Scroll within panels to view inventory lists. / 在面板内滚动查看库存列表。

---

## 💡 5. Strategy Tips / 策略建议

1. **Balance Expenses / 平衡开支**: Never spend all gold on purchases. Always reserve funds for wages and maintenance to avoid bankruptcy. / 切勿将所有金币用于采购，务必预留资金支付工资与维护费，避免破产。
2. **Upgrade Early / 尽早升级**: Ship upgrades significantly reduce long-term shipping costs. Invest surplus gold early. / 船只升级能大幅降低长期运输成本，有盈余时优先升级。
3. **Optimize Workers / 优化工匠**: Train workers to "Skilled" status before dismissing them. Their doubled output maximizes ROI per round. / 解雇前确保工匠达到“熟练”状态，产出翻倍可大幅提升单回合回报率。
4. **Product Selection / 商品选择**: Finished goods yield higher profit margins than raw materials, but factor in the VAT. / 成品利润高于原材料，但需计入增值税成本。
5. **Tax Planning / 税务规划**: Estimate potential Income Tax before accepting high-reward orders. / 接取高收益订单前，请提前估算所得税影响。

---

## 🏁 6. Game End & Rankings / 游戏结局与评级

After **8 Voyages**, the game ends with a final evaluation based on **Reputation / 声望**.

| Reputation / 声望 | Rank Title (EN) / 英文称号 | 中文称号 |
|:---|:---|:---|
| **≥ 300** | 👑 King of the Silk Road | 丝绸之路霸主 |
| **≥ 200** | 🏆 Maritime Tycoon | 海上贸易大亨 |
| **≥ 100** | ⭐ Successful Merchant | 成功商人 |
| **≥ 50** | 👍 Qualified Trader | 合格商人 |
| **< 50** | 🌊 Novice Merchant | 新手商人 |

---

## 🛡️ 7. Troubleshooting / 故障排除

- **"Cannot Save Game" / 无法存档**: Ensure the project folder has write permissions. Check if antivirus software is blocking JSON file creation. / 请确保项目文件夹具有写入权限，并检查杀毒软件是否拦截了 JSON 文件生成。
- **"Game Crashes on Launch" / 启动崩溃**: Verify Python version is 3.8+. Older OS versions may lack bundled `tkinter` components. / 确认 Python 版本 ≥3.8。部分旧版系统可能缺少 `tkinter` 组件。
- **"Black Screen / UI Issues" / 黑屏或界面异常**: Update your graphics driver or run with admin privileges if DPI scaling causes rendering issues. / 更新显卡驱动；若因 DPI 缩放导致显示异常，请尝试以管理员身份运行。

---

## 🤝 8. Credits & License / 版权与许可

- **Developer / 开发者**: `Joe Zhou, Aaron Zhu`
- **Version / 版本**: `v1.3.4`
- **Language Support / 语言支持**: English & Simplified Chinese (Bilingual UI) / 英文与简体中文双语界面
- **License / 许可协议**: MIT License. Free to use, modify, and distribute for personal or commercial projects. / MIT 开源协议。允许自由使用、修改及分发，适用于个人或商业项目。

---

## 📌 Quick Reference / 快速参考

| 🇬🇧 English | 🇨🇳 中文 |
|:---|:---|
| **Launch**: `python PortMasters.py` | **启动**: 运行 `python PortMasters.py` |
| **Core Loop**: Buy ➔ Trade ➔ Pay Wages ➔ Upgrade | **核心循环**: 采购 ➔ 交易 ➔ 付薪 ➔ 升级 |
| **Top Sellers**: Sachets & Brocade (watch VAT!) | **高利润商品**: 香囊与绫罗绸缎（注意增值税！） |
| **Save**: Auto-prompt or `Ctrl+S` | **存档**: 自动提示或按 `Ctrl+S` |
| **Bankruptcy Warning**: Salary > Gold = Game Over | **破产警告**: 金币 < 工资 = 游戏结束！ |
| **Win Condition**: Complete 8 voyages, Rep ≥ 300 | **通关目标**: 完成8次航程，声望 ≥ 300 |

---

🌊 *Fair winds and following seas!* 🚩  
🌊 *祝您在海上丝绸之路的旅途一帆风顺！* 🏮
