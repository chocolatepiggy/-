# 🚢 Maritime Trade Tycoon - 海上丝绸之路贸易大亨



> **Note:** The following documentation is available in both English and Chinese. You may read the English section first, then refer to the Chinese translation below for easier understanding if needed.

> **说明：** 以下文档提供中英文双版本。您可以先阅读英文部分，若有需要可参考下方的中文翻译以便更顺畅地理解游戏。



---



<div align="center">

  <h1>🌊 Maritime Trade Tycoon 🚢</h1>

  <p><strong>Historical Business Simulation / 历史商业模拟游戏</strong></p>

  <p>A strategic trading game inspired by the Maritime Silk Road.</p>

  <p>一款以海上丝绸之路为灵感的策略贸易游戏。</p>

</div>



---



## 📖 1. Overview / 简介



### 🔵 English Version

Welcome to **Maritime Trade Tycoon**! Set sail during the Golden Age of exploration along the historic Silk Road. Manage resources, hire artisans to craft valuable goods, complete trade orders at various ports, and navigate economic challenges like taxes and maintenance costs. Your goal is to accumulate wealth and reputation over 8 voyages to become the ultimate trading mogul.



### 🔴 中文版

欢迎来到 **海上丝绸之路贸易大亨**！扬帆起航于大航海时代，穿梭于历史悠久的丝绸之路上。管理资源，雇佣工匠制作高价值商品，在各大港口完成贸易订单，并应对税收与维护成本等经济挑战。你的目标是在 8 次航程中积累财富与声望，成为终极商业巨头。



---



## 🛠️ 2. How to Install & Run / 安装与运行



### Prerequisites / 前置要求

- **Python 3.x** installed on your machine.

- **No additional external libraries required.** (Uses standard `tkinter`, `json`, `random` modules).

- **Operating System:** Windows, macOS, or Linux.



### Installation Steps / 安装步骤

1. Download or clone this project folder.

2. Open your terminal or command prompt.

3. Navigate to the project directory.

4. Run the main script:

   ```bash

   python maritime_trade_game.py

   ```

5. Enjoy sailing! 🌊



---



## 🎮 3. Gameplay Mechanics / 游戏机制



The game consists of **8 Voyages**, each divided into **4 Phases**.



| Phase | Description (EN) | 描述 (CN) |

| :--- | :--- | :--- |

| **Phase 1** | **Port Purchase**: Visit ports to buy raw materials or finished goods. | **港口采购**：访问港口购买原材料或成品。 |

| **Phase 2** | **Trade Transaction**: Complete orders given by port customers for rewards. | **贸易交易**：完成港口顾客给定的订单以获取报酬。 |

| **Phase 3** | **Maintenance & Wages**: Pay fixed ship maintenance fees and worker salaries. | **维护与工资**：支付船只固定维护费及工人薪资。 |

| **Phase 4** | **Ship Upgrade**: Upgrade your ship level to reduce future transport costs. | **船只升级**：提升船只等级以降低未来运输成本。 |



### Resource Types / 资源类型

- **Raw Materials (原材料):**

  - **Hemp (麻布)**: Base material for basic clothing.

  - **Silk (丝绸)**: Premium fabric for high-end goods.

  - **Tea (茶叶)**: Luxury beverage used in sachets.

- **Finished Goods (成品):**

  - **Linen Clothes (麻衣)**: Simple clothing (Weaver made).

  - **Cotton Clothes (布衣)**: Mid-tier clothing (Weaver made).

  - **Brocade (绫罗绸缎)**: High-value fabric (Master made).

  - **Sachet (香囊)**: Luxury fragrant pouch (Maker made).



### Worker System / 工匠系统

- **Weavers (织女):** Craft Linen & Cotton clothes. Wage: 8 Gold/Round.

- **Master Weavers (纺织大师):** Craft Linen, Cotton & Brocade. Wage: 12 Gold/Round.

- **Sachet Makers (香囊师):** Craft Sachets. Wage: 20 Gold/Round.

- **Skilling Up:** Workers gain efficiency after producing enough items, doubling output while increasing wage temporarily.



### Taxes & Finance / 税收与财务

- **VAT (增值税):** Charged on Finished Goods profits (~5%).

- **Income Tax (所得税):** Charged on voyage net profit (~10%).

- **Freight Costs (运输费):** Calculated based on item quantity minus Ship Level discount. Formula: `max(5, Items×2 - ShipLevel×5)`.



---



## ⌨️ 4. Controls & Shortcuts / 操作与快捷键



### Keyboard Shortcuts / 键盘快捷键



| Key | Action (EN) | 功能 (CN) |

| :--- | :--- | :--- |

| **Ctrl + S** | Save Game / 保存进度 |

| **Ctrl + N** | Next Phase / 进入下一阶段 |

| **Ctrl + H** | Worker Management / 工匠管理界面 |

| **Ctrl + R** | Restart Game / 重新开始游戏 |

| **F1** | Help Instructions / 帮助指南 |



### Mouse Usage / 鼠标使用

- Click buttons to confirm actions (Buy, Trade, Upgrade).

- Scroll to view inventory lists within panels.



---



## 💡 5. Strategy Tips / 策略建议



1. **Balance Expenses:** Never spend all money on purchasing. Always reserve funds for wages and maintenance fees to avoid bankruptcy.

2. **Upgrade Early:** Ship upgrades significantly lower long-term shipping costs. Do this as soon as you have surplus gold.

3. **Worker Efficiency:** Train workers to skilled status before firing them; they produce more, increasing overall ROI per round.

4. **Product Selection:** Selling finished goods yields higher profit margins than raw materials, but remember to pay VAT.

5. **Tax Planning:** Calculate potential income tax before completing high-reward transactions.



### 策略建议 / Strategy Tips (CN)

1. **平衡开支：** 不要花光所有钱用于采购。始终预留资金支付工资和维护费，避免破产。

2. **尽早升级：** 船只升级能显著降低长期运输成本。一旦有盈余金币，立即进行升级。

3. **工人效率：** 在解雇工人前让其达到熟练状态；熟练工产出翻倍，提高单回合投资回报率。

4. **商品选择：** 销售成品比原材料利润高，但要注意缴纳增值税。

5. **税务规划：** 在高收益交易前计算潜在的所得税影响。



---



## 🏁 6. Ending the Game / 游戏结局



After **8 Voyages**, the game concludes with a final score evaluation based on **Reputation (声望)**.



| Reputation Score | Rank Title (EN) | 称号 (CN) |

| :--- | :--- | :--- |

| **≥ 300** | 👑 King of Silk Road | 丝绸之路霸主 |

| **≥ 200** | 🏆 Maritime Tycoon | 海上贸易大亨 |

| **≥ 100** | ⭐ Successful Merchant | 成功商人 |

| **≥ 50** | 👍 Qualified Trader | 合格商人 |

| **< 50** | 🌊 Novice Merchant | 新手商人 |



---



## 🛡️ 7. Troubleshooting / 故障排除



- **"Cannot Save Game":** Ensure the current folder has write permissions. Check antivirus software if blocking the JSON file creation.

- **"Game Crashes on Launch":** Ensure Python version is 3.8+. Some older OS versions might lack bundled `tkinter` components.

- **"Black Screen":** Try updating your graphics driver or run with admin privileges if DPI scaling issues occur.



---



## 🤝 8. Credits & License / 版权信息



- **Developer:** [Your Name]

- **Version:** v1.0.0

- **Language Support:** English & Simplified Chinese (Bilingual UI).

- **License:** MIT License (Free to use and modify for personal projects).



---



## 🇨🇳 🏮 Quick Reference Card (Chinese Only Section) / 快速参考卡（仅中文）



如果你主要看中文，以下是核心摘要：



*   **启动游戏：** 双击运行程序或使用 `python 文件名.py`。

*   **核心循环：** 采购物资 ➔ 做任务/卖货 ➔ 付工资/维修费 ➔ 升级船。

*   **赚钱关键：** 制造“香囊”和“绫罗绸缎”单价最高，但要计算增值税。

*   **如何存盘：** 游戏会自动询问存档，也可以随时按 `Ctrl+S`。

*   **破产警告：** 如果余额不足以支付工资（💸），游戏结束！请控制工人数量。

*   **胜利条件：** 跑完 8 趟航线，最后声望 > 300 即为完美通关。



---



Enjoy your journey on the Maritime Silk Road! 🐟

祝你在海上丝绸之路的旅途愉快！🚩