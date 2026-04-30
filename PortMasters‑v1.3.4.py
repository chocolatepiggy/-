import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
import math


class MaritimeTradeGameGUI:
    def __init__(self):
        """The function initializes the game window, settings, and inventory data."""
        self.window = tk.Tk()
        self.window.title("海上丝绸之路贸易大亨 / Maritime Trade Tycoon")
        self.window.geometry("1600x950")
        self.window.minsize(1400, 850)

        self.colors = {
            "bg_light": "#E6F2FF",
            "bg_dark": "#1A3C8C",
            "accent_blue": "#2E5AA7",
            "accent_gold": "#FFD700",
            "accent_red": "#FF6B6B",
            "accent_green": "#4CAF50",
            "text_dark": "#1A237E",
            "text_light": "#FFFFFF",
            "button_primary": "#2E5AA7",
            "button_success": "#4CAF50",
            "button_warning": "#FF9800",
            "button_danger": "#FF5252",
            "hemp": "#8B7355",
            "silk": "#DC143C",
            "tea": "#228B22",
            "linen_clothes": "#D2691E",
            "cotton_clothes": "#4169E1",
            "silk_brocade": "#8B008B",
            "sachet": "#FF1493",
            "worker_bg": "#FFF8DC"
        }

        self.window.configure(bg=self.colors["bg_light"])

        self.inventory = {
            "麻布": 8, "丝绸": 5, "茶叶": 3,
            "麻衣": 0, "布衣": 0, "绫罗绸缎": 0, "香囊": 0
        }
        self.money = 100
        self.score = 0
        self.current_round = 1
        self.max_rounds = 8

        self.total_revenue = 0
        self.total_costs = 0
        self.material_costs = 0
        self.worker_wages = 0
        self.maintenance_costs = 0
        self.vat_paid = 0
        self.income_tax_paid = 0
        self.round_revenue = 0
        self.round_costs = 0

        self.weavers = []
        self.master_weavers = []
        self.sachet_makers = []

        self.WEAVER_WAGE = 8
        self.MASTER_WEAVER_WAGE = 12
        self.SACHET_MAKER_WAGE = 20

        self.RECIPES = {
            "麻衣": {"materials": {"麻布": 2}, "value": 15, "worker_type": "weaver"},
            "布衣": {"materials": {"麻布": 2, "丝绸": 1}, "value": 35, "worker_type": "weaver"},
            "绫罗绸缎": {"materials": {"丝绸": 3}, "value": 60, "worker_type": "master"},
            "香囊": {"materials": {"丝绸": 1, "茶叶": 2}, "value": 80, "worker_type": "sachet_maker"}
        }

        self.fixed_cost = 15

        self.resource_types = ["麻布", "丝绸", "茶叶"]
        self.product_types = ["麻衣", "布衣", "绫罗绸缎", "香囊"]

        self.resource_colors = {
            "麻布": self.colors["hemp"],
            "丝绸": self.colors["silk"],
            "茶叶": self.colors["tea"],
            "麻衣": self.colors["linen_clothes"],
            "布衣": self.colors["cotton_clothes"],
            "绫罗绸缎": self.colors["silk_brocade"],
            "香囊": self.colors["sachet"]
        }

        self.resource_icons = {
            "麻布": "🧶", "丝绸": "👘", "茶叶": "🍵",
            "麻衣": "👔", "布衣": "👕", "绫罗绸缎": "👗", "香囊": "🌸"
        }

        self.ports = ["泉州港 / Quanzhou", "广州港 / Guangzhou", "宁波港 / Ningbo", "扬州港 / Yangzhou", "杭州港 / Hangzhou"]
        self.commodities = {
            "麻布": {"港口": ["泉州港 / Quanzhou", "宁波港 / Ningbo"], "基础价格": (3, 5)},
            "丝绸": {"港口": ["杭州港 / Hangzhou", "扬州港 / Yangzhou"], "基础价格": (6, 9)},
            "茶叶": {"港口": ["广州港 / Guangzhou", "泉州港 / Quanzhou"], "基础价格": (10, 14)}
        }

        self.product_prices = {
            "麻衣": (30, 42),
            "布衣": (50, 65),
            "绫罗绸缎": (70, 90),
            "香囊": (95, 120)
        }

        self.resource_probabilities = {"麻布": 0.4, "丝绸": 0.35, "茶叶": 0.25}

        self.ship_level = 0
        self.ship_upgrade_cost = [15, 25, 40]

        self.phase = 0
        self.resource_cards = []
        self.customer_cards = []
        self.purchased_cards = set()
        self.completed_orders = set()
        self.purchase_count = 0
        self.order_count = 0
        self.game_over = False

        self.purchase_buttons = []
        self.order_buttons = []

        self.save_file = "maritime_trade_save.json"

        self.setup_styles()
        self.create_widgets()
        self.setup_keyboard_shortcuts()

        if os.path.exists(self.save_file):
            if messagebox.askyesno("读取存档 / Load Save", "检测到上次的存档，是否继续游戏？ / Detected previous save, continue playing?"):
                self.load_game()
                return

        self.show_welcome()

    def setup_keyboard_shortcuts(self):
        """The function binds keyboard events to game control actions."""
        self.window.bind('<Control-s>', lambda e: self.save_game())
        self.window.bind('<Control-n>', lambda e: self.next_phase())
        self.window.bind('<Control-r>', lambda e: self.restart_game())
        self.window.bind('<Control-h>', lambda e: self.show_worker_management())
        self.window.bind('<F1>', lambda e: self.show_instructions())

    def save_game(self):
        """The function saves the current game state to a JSON file."""
        game_data = {
            "inventory": self.inventory,
            "money": self.money,
            "score": self.score,
            "current_round": self.current_round,
            "ship_level": self.ship_level,
            "phase": self.phase,
            "purchase_count": self.purchase_count,
            "order_count": self.order_count,
            "purchased_cards": list(self.purchased_cards),
            "completed_orders": list(self.completed_orders),
            "resource_cards": self.resource_cards,
            "customer_cards": self.customer_cards,
            "weavers": self.weavers,
            "master_weavers": self.master_weavers,
            "sachet_makers": self.sachet_makers,
            "total_revenue": self.total_revenue,
            "total_costs": self.total_costs,
            "material_costs": self.material_costs,
            "worker_wages": self.worker_wages,
            "maintenance_costs": self.maintenance_costs,
            "vat_paid": self.vat_paid,
            "income_tax_paid": self.income_tax_paid
        }
        try:
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(game_data, f, ensure_ascii=False, indent=2)
            self.log_message("💾 游戏已保存！ / Game Saved!")
            messagebox.showinfo("保存成功 / Save Success", "游戏进度已保存！ / Progress Saved!")
        except Exception as e:
            self.log_message(f"❌ 保存失败：{str(e)}")
            messagebox.showerror("保存失败 / Save Failed", f"无法保存游戏：{str(e)}")

    def load_game(self):
        """The function loads the game state from a previously saved JSON file."""
        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
                game_data = json.load(f)

            self.inventory = game_data["inventory"]
            self.money = game_data["money"]
            self.score = game_data["score"]
            self.current_round = game_data["current_round"]
            self.ship_level = game_data["ship_level"]
            self.phase = game_data["phase"]
            self.purchase_count = game_data["purchase_count"]
            self.order_count = game_data["order_count"]
            self.purchased_cards = set(game_data["purchased_cards"])
            self.completed_orders = set(game_data["completed_orders"])
            self.resource_cards = game_data["resource_cards"]
            self.customer_cards = game_data["customer_cards"]

            self.weavers = game_data.get("weavers", [])
            self.master_weavers = game_data.get("master_weavers", [])
            self.sachet_makers = game_data.get("sachet_makers", [])
            self.total_revenue = game_data.get("total_revenue", 0)
            self.total_costs = game_data.get("total_costs", 0)
            self.material_costs = game_data.get("material_costs", 0)
            self.worker_wages = game_data.get("worker_wages", 0)
            self.maintenance_costs = game_data.get("maintenance_costs", 0)
            self.vat_paid = game_data.get("vat_paid", 0)
            self.income_tax_paid = game_data.get("income_tax_paid", 0)

            self.log_message("📂 存档已加载！ / Save Loaded!")
            self.update_display()

            if self.phase == 0:
                self.show_welcome()
            elif self.phase == 1:
                self.start_phase1()
            elif self.phase == 2:
                self.start_phase2()
            elif self.phase == 3:
                self.start_phase3()
            elif self.phase == 4:
                self.start_phase4()
            else:
                self.show_worker_management()

        except Exception as e:
            self.log_message(f"❌ 加载存档失败：{str(e)}")
            messagebox.showerror("加载失败 / Load Failed", "无法读取存档，开始新游戏。 / Cannot read save, start new game.")
            self.show_welcome()

    def delete_save(self):
        """The function deletes the local save file if it exists."""
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
            self.log_message("🗑️ 存档已删除 / Save Deleted")

    def calculate_transport_cost(self, total_items):
        """The function calculates shipping cost based on items and ship level."""
        base_cost = total_items * 2
        discount = self.ship_level * 5
        return max(5, base_cost - discount)

    def show_transport_cost_detail(self, total_items):
        """The function returns detailed breakdown information for transport costs."""
        base_cost = total_items * 2
        discount = self.ship_level * 5
        final_cost = self.calculate_transport_cost(total_items)
        return {
            "total_items": total_items,
            "base_cost": base_cost,
            "discount": discount,
            "final_cost": final_cost,
            "formula": f"max(5, ({total_items} × 2) - {discount}) = {final_cost}"
        }

    def calculate_vat(self, product, selling_price):
        """The function calculates Value Added Tax based on profit margins."""
        recipe = self.RECIPES[product]
        material_cost = 0

        for material, amount in recipe["materials"].items():
            avg_price = sum(self.commodities[material]["基础价格"]) / 2
            material_cost += avg_price * amount

        worker_cost = 0
        if recipe["worker_type"] == "weaver":
            worker_cost = self.WEAVER_WAGE
        elif recipe["worker_type"] == "master":
            worker_cost = self.MASTER_WEAVER_WAGE
        elif recipe["worker_type"] == "sachet_maker":
            worker_cost = self.SACHET_MAKER_WAGE

        taxable_amount = selling_price - material_cost - worker_cost

        if taxable_amount > 0:
            vat = math.floor(taxable_amount * 0.05)
            self.log_message(f"🧮 VAT Calculation: 5% x ({selling_price} - {material_cost:.1f}(Mat) - {worker_cost}(Wage)) = {vat}")
            return vat
        return 0

    def calculate_income_tax(self, pre_tax_profit):
        """The function calculates income tax based on pre-tax profit."""
        if pre_tax_profit > 0:
            return math.floor(pre_tax_profit * 0.1)
        return 0

    def hire_worker(self, worker_type):
        """The function adds a new worker to the employment roster."""
        if worker_type == "weaver":
            wage = self.WEAVER_WAGE
            if self.money >= wage:
                self.money -= wage
                self.weavers.append({'task': None, 'progress': 0, 'produced_count': 0, 'is_skilled': False})
                self.worker_wages += wage
                self.log_message(f"👩‍🔧 Hired a Weaver! Wage: {wage} Gold / Round")
                self.update_display()
                return True
        elif worker_type == "master":
            wage = self.MASTER_WEAVER_WAGE
            if self.money >= wage:
                self.money -= wage
                self.master_weavers.append({'task': None, 'progress': 0, 'produced_count': 0, 'is_skilled': False})
                self.worker_wages += wage
                self.log_message(f"👩‍🎨 Hired a Master Weaver! Wage: {wage} Gold / Round")
                self.update_display()
                return True
        elif worker_type == "sachet_maker":
            wage = self.SACHET_MAKER_WAGE
            if self.money >= wage:
                self.money -= wage
                self.sachet_makers.append({'task': None, 'progress': 0, 'produced_count': 0, 'is_skilled': False})
                self.worker_wages += wage
                self.log_message(f"🌸 Hired a Sachet Maker! Wage: {wage} Gold / Round")
                self.update_display()
                return True

        self.log_message(f"❌ Insufficient funds to hire workers!")
        return False

    def fire_worker(self, worker_type, index):
        """The function removes a worker from employment with severance pay."""
        if worker_type == "weaver":
            worker_list = self.weavers
            wage = self.WEAVER_WAGE
            worker_name = "织女 / Weaver"
        elif worker_type == "master":
            worker_list = self.master_weavers
            wage = self.MASTER_WEAVER_WAGE
            worker_name = "纺织大师 / Master"
        elif worker_type == "sachet_maker":
            worker_list = self.sachet_makers
            wage = self.SACHET_MAKER_WAGE
            worker_name = "香囊师 / Sachet Maker"
        else:
            return False

        if index < 0 or index >= len(worker_list):
            self.log_message(f"❌ Invalid worker ID!")
            return False

        if self.money >= wage:
            self.money -= wage
            worker = worker_list.pop(index)
            self.log_message(f"💔 Dismissed a {worker_name}. Severance Paid: {wage} Gold")
            if worker['task']:
                self.log_message(f"  This worker was making: {worker['task']}")
            self.update_display()
            return True
        else:
            self.log_message(f"❌ Insufficient funds for {worker_name}'s severance fee: {wage} Gold")
            return False

    def assign_worker_task(self, worker_list, worker_type, task):
        """The function assigns a production task to available workers."""
        for worker in worker_list:
            if worker['task'] is None:
                recipe = self.RECIPES[task]
                can_produce = True
                for material, amount in recipe["materials"].items():
                    if self.inventory.get(material, 0) < amount:
                        can_produce = False
                        break

                if can_produce:
                    for material, amount in recipe["materials"].items():
                        self.inventory[material] -= amount
                        self.material_costs += amount * (sum(self.commodities[material]["基础价格"]) / 2)

                    worker['task'] = task
                    worker['progress'] = 0

                    material_list = [f"{self.resource_icons[m]}{m}×{a}" for m, a in recipe["materials"].items()]
                    self.log_message(
                        f"📋 Assigned task: Produce {self.resource_icons[task]}{task} (Req: {' + '.join(material_list)})")
                    self.update_display()
                    return True
                else:
                    self.log_message(f"❌ Material shortage to produce {task}!")
                    return False

        self.log_message(f"❌ All workers are already assigned tasks!")
        return False

    def process_production(self):
        """The function resolves completed production tasks for all workers."""
        for weaver in self.weavers:
            if weaver['task']:
                if weaver.get('is_skilled', False):
                    product = weaver['task']
                    self.inventory[product] = self.inventory.get(product, 0) + 2
                    weaver['produced_count'] = weaver.get('produced_count', 0) + 2
                    weaver['double_production_this_round'] = True
                    self.log_message(f"✅ Skilled Weaver finished 2x {self.resource_icons[product]}{product}!")
                else:
                    product = weaver['task']
                    self.inventory[product] = self.inventory.get(product, 0) + 1
                    weaver['produced_count'] = weaver.get('produced_count', 0) + 1
                    self.log_message(f"✅ Weaver finished {self.resource_icons[product]}{product}!")

                    if weaver.get('produced_count', 0) >= 2:
                        weaver['is_skilled'] = True
                        self.log_message(f"⭐ Weaver Promotion! Can now produce 2 items per round!")

                weaver['task'] = None
                weaver['progress'] = 0

        for master in self.master_weavers:
            if master['task']:
                if master.get('is_skilled', False):
                    product = master['task']
                    self.inventory[product] = self.inventory.get(product, 0) + 2
                    master['produced_count'] = master.get('produced_count', 0) + 2
                    master['double_production_this_round'] = True
                    self.log_message(f"✅ Skilled Master finished 2x {self.resource_icons[product]}{product}!")
                else:
                    product = master['task']
                    self.inventory[product] = self.inventory.get(product, 0) + 1
                    master['produced_count'] = master.get('produced_count', 0) + 1
                    self.log_message(f"✅ Master finished {self.resource_icons[product]}{product}!")

                    if master.get('produced_count', 0) >= 2:
                        master['is_skilled'] = True
                        self.log_message(f"⭐ Master Promotion! Can now produce 2 items per round!")

                master['task'] = None
                master['progress'] = 0

        for maker in self.sachet_makers:
            if maker['task']:
                if maker.get('is_skilled', False):
                    product = maker['task']
                    self.inventory[product] = self.inventory.get(product, 0) + 2
                    maker['produced_count'] = maker.get('produced_count', 0) + 2
                    maker['double_production_this_round'] = True
                    self.log_message(f"✅ Skilled Maker finished 2x {self.resource_icons[product]}{product}!")
                else:
                    product = maker['task']
                    self.inventory[product] = self.inventory.get(product, 0) + 1
                    maker['produced_count'] = maker.get('produced_count', 0) + 1
                    self.log_message(f"✅ Maker finished {self.resource_icons[product]}{product}!")

                    if maker.get('produced_count', 0) >= 2:
                        maker['is_skilled'] = True
                        self.log_message(f"⭐ Maker Promotion! Can now produce 2 items per round!")

                maker['task'] = None
                maker['progress'] = 0

    def pay_worker_wages(self):
        """The function pays wages to all employed workers based on performance."""
        total_paid = 0

        weaver_wages = 0
        for weaver in self.weavers:
            base_wage = self.WEAVER_WAGE
            if weaver.get('double_production_this_round', False):
                base_wage = int(base_wage * 1.5)
                self.log_message(f"💪 Weaver High Yield (2 items), Wage increased to {base_wage} Gold")
            weaver_wages += base_wage

        master_wages = 0
        for master in self.master_weavers:
            base_wage = self.MASTER_WEAVER_WAGE
            if master.get('double_production_this_round', False):
                base_wage = int(base_wage * 1.5)
                self.log_message(f"💪 Master High Yield (2 items), Wage increased to {base_wage} Gold")
            master_wages += base_wage

        maker_wages = 0
        for maker in self.sachet_makers:
            base_wage = self.SACHET_MAKER_WAGE
            if maker.get('double_production_this_round', False):
                base_wage = int(base_wage * 1.5)
                self.log_message(f"💪 Maker High Yield (2 items), Wage increased to {base_wage} Gold")
            maker_wages += base_wage

        total_wages = weaver_wages + master_wages + maker_wages

        if total_wages == 0:
            return True

        if self.money >= total_wages:
            self.money -= total_wages
            total_paid = total_wages
            self.worker_wages += total_wages
            self.round_costs += total_wages

            if weaver_wages > 0:
                self.log_message(f"💰 Paid wages for {len(self.weavers)} Weavers: {weaver_wages} Gold")
            if master_wages > 0:
                self.log_message(f"💰 Paid wages for {len(self.master_weavers)} Masters: {master_wages} Gold")
            if maker_wages > 0:
                self.log_message(f"💰 Paid wages for {len(self.sachet_makers)} Makers: {maker_wages} Gold")

            self._clear_wage_markers()
            self.update_display()
            return True
        else:
            self.log_message(f"⚠️ Insufficient funds! Needed Wages: {total_wages} Gold, Have: {self.money} Gold")
            self.log_message(f"💥 Could not pay wages, workers strike...")
            self.log_message(f"💥 Reputation collapsed, forced bankruptcy!")
            return "bankruptcy"

    def _clear_wage_markers(self):
        """The function removes temporary wage multiplier flags from workers."""
        for worker in self.weavers + self.master_weavers + self.sachet_makers:
            if 'double_production_this_round' in worker:
                del worker['double_production_this_round']

    def generate_raw_material_order(self):
        """The function generates a demand order for raw materials."""
        num_resources = random.randint(1, 3)
        resources = []
        available_resources = self.resource_types.copy()

        demand_port = random.choice(self.ports)
        total_items = 0

        for _ in range(num_resources):
            if not available_resources:
                break

            resource = random.choice(available_resources)
            available_resources.remove(resource)

            required = random.randint(2, 5)
            total_items += required
            resources.append({
                "type": resource,
                "required": required
            })

        base_reward = sum(r["required"] * 5 for r in resources)
        reward = base_reward + random.randint(10, 25)

        return {
            "demand_port": demand_port,
            "resources": resources,
            "reward": reward,
            "total_items": total_items,
            "is_product_order": False
        }

    def generate_product_order(self):
        """The function generates a demand order for finished products."""
        product = random.choice(self.product_types)
        required = random.randint(1, 3)

        demand_port = random.choice(self.ports)

        base_price = random.randint(*self.product_prices[product])
        reward = base_price * required

        return {
            "demand_port": demand_port,
            "resources": [{"type": product, "required": required}],
            "reward": reward,
            "total_items": required,
            "is_product_order": True
        }

    def generate_mixed_order(self):
        """The function generates a mixed trade order randomly."""
        if random.random() < 0.5 or not self.product_types:
            return self.generate_raw_material_order()
        else:
            return self.generate_product_order()

    def generate_mixed_resource_card(self):
        """The function generates a port resource card including materials and products."""
        if random.random() < 0.3:
            return self.generate_product_purchase_card()

        num_resources = random.randint(1, 3)
        resources = []
        available_resources = list(self.resource_probabilities.keys())
        probabilities = list(self.resource_probabilities.values())

        port = random.choice(self.ports)

        for _ in range(num_resources):
            if not available_resources:
                break

            resource = random.choices(available_resources, weights=probabilities)[0]
            idx = available_resources.index(resource)
            available_resources.pop(idx)
            probabilities.pop(idx)

            quantity = random.randint(1, 3)
            price_range = self.commodities[resource]["基础价格"]
            base_price = random.randint(price_range[0], price_range[1])

            if port in self.commodities[resource]["港口"]:
                price = base_price - 1
            else:
                price = base_price + 1

            resources.append({
                "type": resource,
                "quantity": quantity,
                "price": price
            })

        total_cost = sum(r["quantity"] * r["price"] for r in resources)

        return {
            "port": port,
            "resources": resources,
            "total_cost": total_cost,
            "is_product_card": False
        }

    def generate_product_purchase_card(self):
        """The function generates a card to purchase finished products at ports."""
        product = random.choice(self.product_types)
        quantity = random.randint(1, 2)

        port = random.choice(self.ports)

        recipe = self.RECIPES[product]
        material_cost = 0
        material_details = []
        for material, amount in recipe["materials"].items():
            avg_price = sum(self.commodities[material]["基础价格"]) / 2
            material_cost += avg_price * amount
            material_details.append(f"{material}×{amount}")

        markup = random.uniform(1.4, 1.8)
        unit_price = math.floor(material_cost * markup)

        min_price, max_price = self.product_prices[product]
        unit_price = max(min_price, min(unit_price, max_price))

        total_cost = unit_price * quantity

        resources = [{
            "type": product,
            "quantity": quantity,
            "price": unit_price,
            "material_cost": material_cost,
            "material_details": " + ".join(material_details)
        }]

        return {
            "port": port,
            "resources": resources,
            "total_cost": total_cost,
            "is_product_card": True
        }

    def purchase_card_specific(self, card):
        """The function processes the purchase of a specific resource card."""
        if card["id"] in self.purchased_cards:
            return

        if self.money >= card["total_cost"]:
            self.money -= card["total_cost"]
            self.round_costs += card["total_cost"]
            self.total_costs += card["total_cost"]

            for resource_info in card["resources"]:
                self.inventory[resource_info["type"]] += resource_info["quantity"]

            self.purchased_cards.add(card["id"])
            self.purchase_count += 1

            if card.get("is_product_card"):
                for r in card["resources"]:
                    self.log_message(
                        f"🛒 Bought Product at {card['port']}: {self.resource_icons.get(r['type'])}{r['type']}×{r['quantity']}"
                        f"(@{r['price']} Gold/item, Mat Cost {r.get('material_cost', '?')} Gold), Total {card['total_cost']} Gold")
                    self.log_message(f"   💡 Tip: VAT applies when selling finished products")
            else:
                resources_text = " + ".join(
                    f"{self.resource_icons.get(r['type'])}{r['type']}×{r['quantity']}({r['price']} Gold/item)"
                    for r in card["resources"]
                )
                self.log_message(f"🛒 Bought at {card['port']}: {resources_text}, Total {card['total_cost']} Gold")

            self.update_display()
            self.update_purchase_buttons()
            self.log_message(f"📊 Purchased {self.purchase_count} cargo batches")
        else:
            self.log_message(f"❌ Insufficient funds! Need {card['total_cost']} Gold, Have {self.money} Gold")

    def complete_order(self, order):
        """The function executes a trade order delivering goods to a port."""
        if order["id"] in self.completed_orders:
            return

        for resource_info in order["resources"]:
            if self.inventory.get(resource_info["type"], 0) < resource_info["required"]:
                self.log_message(f"❌ Inventory short! Need {resource_info['type']}×{resource_info['required']}")
                return

        transport_cost = self.calculate_transport_cost(order["total_items"])
        transport_detail = self.show_transport_cost_detail(order["total_items"])

        for resource_info in order["resources"]:
            self.inventory[resource_info["type"]] -= resource_info["required"]

        self.money -= transport_cost
        self.round_costs += transport_cost
        self.total_costs += transport_cost

        reward = order["reward"]
        is_product = order.get("is_product_order", False)

        if is_product:
            product = order["resources"][0]["type"]
            vat = self.calculate_vat(product, reward / order["resources"][0]["required"])
            total_vat = vat * order["resources"][0]["required"]
            actual_reward = reward - total_vat
            self.vat_paid += total_vat
            self.log_message(f"🧾 Product Sales VAT: {total_vat} Gold")
        else:
            actual_reward = reward

        self.money += actual_reward
        self.round_revenue += actual_reward
        self.total_revenue += actual_reward
        self.score += int(actual_reward - transport_cost)

        self.completed_orders.add(order["id"])
        self.order_count += 1

        resources_text = " + ".join(
            f"{self.resource_icons.get(r['type'])}{r['type']}×{r['required']}"
            for r in order["resources"]
        )
        net_profit = actual_reward - transport_cost

        self.log_message(f"📦 Completed Order at {order['demand_port']}: {resources_text}")
        self.log_message(f"   📦 Total Items: {transport_detail['total_items']} × 2 = {transport_detail['base_cost']} Gold")
        self.log_message(f"   🚢 Discount: -{transport_detail['discount']} Gold")
        self.log_message(f"   ⚓ Final Freight: {transport_detail['final_cost']} Gold")
        self.log_message(f"   💰 Reward: {actual_reward} Gold - ⚓ Freight: {transport_cost} Gold = 📊 Net Profit: {net_profit} Gold")

        self.update_display()
        self.update_order_buttons()
        self.log_message(f"📊 Completed {self.order_count} transactions")

    def pay_fixed_cost(self):
        """The function pays the fixed maintenance cost for the voyage."""
        if self.money >= self.fixed_cost:
            self.money -= self.fixed_cost
            self.maintenance_costs += self.fixed_cost
            self.round_costs += self.fixed_cost
            self.total_costs += self.fixed_cost
            self.log_message(f"💸 Paid Ship Maintenance Fee: {self.fixed_cost} Gold")
            self.update_display()
            self.start_phase4()
        else:
            self.force_pay_cost()

    def force_pay_cost(self):
        """The function forces payment with remaining funds if insufficient."""
        if self.money > 0:
            paid = min(self.money, self.fixed_cost)
            self.money -= paid
            self.maintenance_costs += paid
            self.round_costs += paid
            self.total_costs += paid
            self.log_message(f"⚠️ Forced payment of {paid} Gold (Needed {self.fixed_cost} Gold)")
            self.update_display()

            if self.money <= 0:
                self.log_message("⚠️ Funds depleted! Cannot continue sailing...")
                self.show_bankruptcy_screen()
            else:
                self.start_phase4()
        else:
            self.log_message("💸 No funds to pay")
            self.show_bankruptcy_screen()

    def end_round(self):
        """The function concludes the current voyage round and resets stats."""
        self.log_message(f"\n📊=== Round {self.current_round} Settlement ===")

        self.log_message(f"💰 Revenue this round: {self.round_revenue} Gold")

        total_round_costs = self.round_costs + self.maintenance_costs + self.worker_wages
        self.log_message(f"💸 Total Cost this round: {total_round_costs} Gold")
        self.log_message(f"   🔧 Maintenance: {self.maintenance_costs} Gold")
        self.log_message(f"   📦 Materials: {self.material_costs} Gold")
        self.log_message(f"   👥 Wages: {self.worker_wages} Gold")

        pre_tax_profit = self.round_revenue - total_round_costs
        self.log_message(f"📈 Pre-tax Profit: {pre_tax_profit} Gold")

        income_tax = self.calculate_income_tax(pre_tax_profit)
        if income_tax > 0:
            self.money -= income_tax
            self.income_tax_paid += income_tax
            self.log_message(f"🏛️ Income Tax Paid (10%): {income_tax} Gold")
        else:
            self.log_message(f"🏛️ No profit, no income tax due")

        if self.vat_paid > 0:
            self.log_message(f"🧾 VAT Paid this round: {self.vat_paid} Gold")

        self.round_revenue = 0
        self.round_costs = 0
        self.maintenance_costs = 0
        self.material_costs = 0
        self.worker_wages = 0

        self.current_round += 1

        if self.current_round > self.max_rounds:
            self.end_game()
        else:
            self.log_message(f"\n🔄=== Preparing for Round {self.current_round} ===")
            self.phase = 0
            self.purchase_count = 0
            self.order_count = 0
            self.resource_cards = []
            self.customer_cards = []
            self.purchased_cards.clear()
            self.completed_orders.clear()

            self.update_display()
            self.show_welcome()
            self.update_button_states()

    def create_inventory_row(self, parent, item):
        """The function creates a row display for inventory items."""
        color = self.resource_colors.get(item, "black")
        icon = self.resource_icons.get(item, "")

        frame = tk.Frame(parent, bg="#F0F8FF")
        frame.pack(fill=tk.X, padx=20, pady=2)

        tk.Label(frame, text=icon,
                 font=("Microsoft YaHei", 12),
                 bg="#F0F8FF").pack(side=tk.LEFT, padx=(0, 5))

        tk.Label(frame, text=item,
                 font=("Microsoft YaHei", 11),
                 bg="#F0F8FF",
                 fg=color,
                 width=10,
                 anchor="w").pack(side=tk.LEFT)

        tk.Label(frame, text=str(self.inventory.get(item, 0)),
                 font=("Microsoft YaHei", 11, "bold"),
                 bg="#F0F8FF",
                 fg=color,
                 width=5).pack(side=tk.RIGHT)

    def show_worker_management(self, in_phase=False):
        """The function displays the worker management interface screen."""
        self.clear_phase_content()

        main_container = ttk.Frame(self.phase_content, style="DarkFrame.TLabelframe")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        canvas = tk.Canvas(main_container, highlightthickness=0, bg=self.colors["bg_light"])
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_light"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        title_frame = tk.Frame(scrollable_frame, bg=self.colors["bg_light"])
        title_frame.pack(fill=tk.X, pady=20)

        tk.Label(title_frame, text="👥 工匠管理 / Worker Management",
                 font=("Microsoft YaHei", 28, "bold"),
                 bg=self.colors["bg_light"],
                 fg=self.colors["bg_dark"]).pack(pady=(0, 10))

        if in_phase:
            tk.Label(title_frame, text=f"💰 Current Funds: {self.money} Gold",
                     font=("Microsoft YaHei", 14),
                     bg=self.colors["bg_light"],
                     fg=self.colors["accent_blue"]).pack()
        else:
            tk.Label(title_frame, text=f"💰 Current Funds: {self.money} Gold | 📦 See Inventory Below",
                     font=("Microsoft YaHei", 14),
                     bg=self.colors["bg_light"],
                     fg=self.colors["accent_blue"]).pack()

        inventory_frame = tk.Frame(scrollable_frame, bg="#F0F8FF", relief=tk.RAISED, borderwidth=2)
        inventory_frame.pack(fill=tk.X, padx=50, pady=10)

        tk.Label(inventory_frame, text="📦 当前库存 / Current Inventory",
                 font=("Microsoft YaHei", 16, "bold"),
                 bg="#F0F8FF",
                 fg=self.colors["bg_dark"]).pack(pady=10)

        materials_frame = tk.Frame(inventory_frame, bg="#F0F8FF")
        materials_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(materials_frame, text="原材料 / Raw Materials:",
                 font=("Microsoft YaHei", 12, "bold"),
                 bg="#F0F8FF",
                 fg=self.colors["accent_blue"]).pack(anchor=tk.W)

        for resource in self.resource_types:
            self.create_inventory_row(materials_frame, resource)

        products_frame = tk.Frame(inventory_frame, bg="#F0F8FF")
        products_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(products_frame, text="成品 / Finished Goods:",
                 font=("Microsoft YaHei", 12, "bold"),
                 bg="#F0F8FF",
                 fg=self.colors["accent_blue"]).pack(anchor=tk.W)

        for product in self.product_types:
            self.create_inventory_row(products_frame, product)

        separator = tk.Frame(scrollable_frame, height=2, bg=self.colors["accent_blue"])
        separator.pack(fill=tk.X, padx=50, pady=15)

        hire_frame = tk.Frame(scrollable_frame, bg=self.colors["worker_bg"], relief=tk.RAISED, borderwidth=2)
        hire_frame.pack(fill=tk.X, padx=50, pady=10)

        tk.Label(hire_frame, text="🔨 雇佣工匠 / Hire Workers",
                 font=("Microsoft YaHei", 18, "bold"),
                 bg=self.colors["worker_bg"],
                 fg=self.colors["bg_dark"]).pack(pady=10)

        workers_info = [
            ("👩‍🔧 织女 / Weaver", f"Making: Linen Clothes(2 Hemp) or Cotton Clothes(2 Hemp+1 Silk)\nWage: {self.WEAVER_WAGE} Gold/Round"),
            ("👩‍🎨 纺织大师 / Master", f"Making: Linen Clothes, Cotton Clothes or Brocade(3 Silk)\nWage: {self.MASTER_WEAVER_WAGE} Gold/Round"),
            ("🌸 香囊师 / Sachet Maker", f"Making: Sachet(1 Silk+2 Tea)\nWage: {self.SACHET_MAKER_WAGE} Gold/Round")
        ]

        for title, desc in workers_info:
            info_frame = tk.Frame(hire_frame, bg=self.colors["worker_bg"])
            info_frame.pack(fill=tk.X, padx=20, pady=5)

            tk.Label(info_frame, text=title,
                     font=("Microsoft YaHei", 12, "bold"),
                     bg=self.colors["worker_bg"],
                     fg=self.colors["text_dark"]).pack(anchor=tk.W)

            tk.Label(info_frame, text=desc,
                     font=("Microsoft YaHei", 10),
                     bg=self.colors["worker_bg"],
                     fg="#666666",
                     justify=tk.LEFT).pack(anchor=tk.W, padx=20)

        hire_buttons_frame = tk.Frame(hire_frame, bg=self.colors["worker_bg"])
        hire_buttons_frame.pack(pady=15)

        if in_phase:
            refresh_func = self.show_worker_management_in_phase
        else:
            refresh_func = self.show_worker_management

        tk.Button(hire_buttons_frame, text=f"👩‍🔧 雇佣织女 ({self.WEAVER_WAGE}💰)",
                  font=("Microsoft YaHei", 12, "bold"),
                  bg=self.colors["button_success"],
                  fg="white",
                  relief=tk.RAISED,
                  borderwidth=2,
                  width=20,
                  height=2,
                  command=lambda: [self.hire_worker("weaver"), refresh_func()]).pack(side=tk.LEFT, padx=10)

        tk.Button(hire_buttons_frame, text=f"👩‍🎨 雇佣纺织大师 ({self.MASTER_WEAVER_WAGE}💰)",
                  font=("Microsoft YaHei", 12, "bold"),
                  bg=self.colors["button_primary"],
                  fg="white",
                  relief=tk.RAISED,
                  borderwidth=2,
                  width=20,
                  height=2,
                  command=lambda: [self.hire_worker("master"), refresh_func()]).pack(side=tk.LEFT, padx=10)

        tk.Button(hire_buttons_frame, text=f"🌸 雇佣香囊师 ({self.SACHET_MAKER_WAGE}💰)",
                  font=("Microsoft YaHei", 12, "bold"),
                  bg=self.colors["button_warning"],
                  fg="white",
                  relief=tk.RAISED,
                  borderwidth=2,
                  width=20,
                  height=2,
                  command=lambda: [self.hire_worker("sachet_maker"), refresh_func()]).pack(side=tk.LEFT, padx=10)

        if self.weavers or self.master_weavers or self.sachet_makers:
            status_frame = tk.Frame(scrollable_frame, bg="#F0F8FF", relief=tk.RAISED, borderwidth=2)
            status_frame.pack(fill=tk.X, padx=50, pady=10)

            tk.Label(status_frame, text="👥 工匠状态与任务分配 / Worker Status & Tasks",
                     font=("Microsoft YaHei", 18, "bold"),
                     bg="#F0F8FF",
                     fg=self.colors["bg_dark"]).pack(pady=10)

            if self.weavers:
                tk.Label(status_frame, text=f"👩‍🔧 织女 / Weavers: {len(self.weavers)}",
                         font=("Microsoft YaHei", 14, "bold"),
                         bg="#F0F8FF",
                         fg=self.colors["accent_blue"]).pack(anchor=tk.W, padx=20, pady=5)

                for i, weaver in enumerate(self.weavers):
                    worker_frame = tk.Frame(status_frame, bg="#F0F8FF")
                    worker_frame.pack(fill=tk.X, padx=20, pady=5)

                    if weaver['task']:
                        skill_text = "(熟练 / Skilled)" if weaver.get('is_skilled', False) else ""
                        task_text = f"Working on: {weaver['task']}{skill_text}"
                    else:
                        skill_text = " ⭐ Skilled" if weaver.get('is_skilled', False) else ""
                        task_text = f"Idle{skill_text}"
                    tk.Label(worker_frame, text=f"  Weaver {i + 1}: {task_text}",
                             font=("Microsoft YaHei", 12),
                             bg="#F0F8FF",
                             fg=self.colors["text_dark"]).pack(side=tk.LEFT, padx=(0, 10))

                    if in_phase and weaver['task'] is None:
                        tk.Button(worker_frame, text=f"Dismiss ({self.WEAVER_WAGE}💰)",
                                  font=("Microsoft YaHei", 9),
                                  bg=self.colors["button_danger"],
                                  fg="white",
                                  command=lambda idx=i: [self.fire_worker("weaver", idx),
                                                         self.show_worker_management_in_phase()]).pack(side=tk.RIGHT,
                                                                                                       padx=5)

                task_frame = tk.Frame(status_frame, bg="#F0F8FF")
                task_frame.pack(pady=10)

                tk.Button(task_frame, text="Make Linen Clothes (Needs 2 Hemp)",
                          font=("Microsoft YaHei", 10),
                          bg=self.colors["button_success"],
                          fg="white",
                          command=lambda: [self.assign_worker_task(self.weavers, "weaver", "麻衣"),
                                           refresh_func()]).pack(side=tk.LEFT, padx=5)

                tk.Button(task_frame, text="Make Cotton Clothes (Needs 2 Hemp+1 Silk)",
                          font=("Microsoft YaHei", 10),
                          bg=self.colors["button_success"],
                          fg="white",
                          command=lambda: [self.assign_worker_task(self.weavers, "weaver", "布衣"),
                                           refresh_func()]).pack(side=tk.LEFT, padx=5)

            if self.master_weavers:
                tk.Label(status_frame, text=f"👩‍🎨 纺织大师 / Masters: {len(self.master_weavers)}",
                         font=("Microsoft YaHei", 14, "bold"),
                         bg="#F0F8FF",
                         fg=self.colors["accent_blue"]).pack(anchor=tk.W, padx=20, pady=10)

                for i, master in enumerate(self.master_weavers):
                    worker_frame = tk.Frame(status_frame, bg="#F0F8FF")
                    worker_frame.pack(fill=tk.X, padx=20, pady=5)

                    if master['task']:
                        skill_text = "(熟练 / Skilled)" if master.get('is_skilled', False) else ""
                        task_text = f"Working on: {master['task']}{skill_text}"
                    else:
                        skill_text = " ⭐ Skilled" if master.get('is_skilled', False) else ""
                        task_text = f"Idle{skill_text}"
                    tk.Label(worker_frame, text=f"  Master {i + 1}: {task_text}",
                             font=("Microsoft YaHei", 12),
                             bg="#F0F8FF",
                             fg=self.colors["text_dark"]).pack(side=tk.LEFT, padx=(0, 10))

                    if in_phase and master['task'] is None:
                        tk.Button(worker_frame, text=f"Dismiss ({self.MASTER_WEAVER_WAGE}💰)",
                                  font=("Microsoft YaHei", 9),
                                  bg=self.colors["button_danger"],
                                  fg="white",
                                  command=lambda idx=i: [self.fire_worker("master", idx),
                                                         self.show_worker_management_in_phase()]).pack(side=tk.RIGHT,
                                                                                                       padx=5)

                task_frame = tk.Frame(status_frame, bg="#F0F8FF")
                task_frame.pack(pady=10)

                for task in ["麻衣 / Linen Clothes", "布衣 / Cotton Clothes", "绫罗绸缎 / Brocade"]:
                    clean_task = task.split()[0]
                    recipe = self.RECIPES[clean_task]
                    materials = [f"{a}{m}" for m, a in recipe["materials"].items()]
                    tk.Button(task_frame, text=f"Make {clean_task} (Need {'+'.join(materials)})",
                              font=("Microsoft YaHei", 10),
                              bg=self.colors["button_primary"],
                              fg="white",
                              command=lambda t=clean_task: [self.assign_worker_task(self.master_weavers, "master", t),
                                                      refresh_func()]).pack(side=tk.LEFT, padx=5)

            if self.sachet_makers:
                tk.Label(status_frame, text=f"🌸 香囊师 / Sachet Makers: {len(self.sachet_makers)}",
                         font=("Microsoft YaHei", 14, "bold"),
                         bg="#F0F8FF",
                         fg=self.colors["accent_blue"]).pack(anchor=tk.W, padx=20, pady=10)

                for i, maker in enumerate(self.sachet_makers):
                    worker_frame = tk.Frame(status_frame, bg="#F0F8FF")
                    worker_frame.pack(fill=tk.X, padx=20, pady=5)

                    task_text = f"Working on: {maker['task']}" if maker['task'] else "Idle"
                    tk.Label(worker_frame, text=f"  Maker {i + 1}: {task_text}",
                             font=("Microsoft YaHei", 12),
                             bg="#F0F8FF",
                             fg=self.colors["text_dark"]).pack(side=tk.LEFT, padx=(0, 10))

                    if in_phase and maker['task'] is None:
                        tk.Button(worker_frame, text=f"Dismiss ({self.SACHET_MAKER_WAGE}💰)",
                                  font=("Microsoft YaHei", 9),
                                  bg=self.colors["button_danger"],
                                  fg="white",
                                  command=lambda idx=i: [self.fire_worker("sachet_maker", idx),
                                                         self.show_worker_management_in_phase()]).pack(side=tk.RIGHT,
                                                                                                       padx=5)

                task_frame = tk.Frame(status_frame, bg="#F0F8FF")
                task_frame.pack(pady=10)

                tk.Button(task_frame, text="Make Sachet (Need 1 Silk+2 Tea)",
                          font=("Microsoft YaHei", 10),
                          bg=self.colors["button_warning"],
                          fg="white",
                          command=lambda: [self.assign_worker_task(self.sachet_makers, "sachet_maker", "香囊"),
                                           refresh_func()]).pack(side=tk.LEFT, padx=5)

        separator2 = tk.Frame(scrollable_frame, height=2, bg=self.colors["accent_blue"])
        separator2.pack(fill=tk.X, padx=50, pady=15)

        if in_phase:
            tk.Button(scrollable_frame,
                      text="✅ 完成工匠管理，继续航行 / Complete Workers, Sailing",
                      font=("Microsoft YaHei", 16, "bold"),
                      bg=self.colors["button_primary"],
                      fg="white",
                      relief=tk.RAISED,
                      borderwidth=3,
                      width=20,
                      height=2,
                      command=self.start_phase2).pack(pady=10)
        else:
            tk.Button(scrollable_frame,
                      text="🔙 返回主界面 / Return Home",
                      font=("Microsoft YaHei", 16, "bold"),
                      bg=self.colors["button_primary"],
                      fg="white",
                      relief=tk.RAISED,
                      borderwidth=3,
                      width=20,
                      height=2,
                      command=self.show_welcome).pack(pady=10)

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(0)

    def show_worker_management_in_phase(self):
        """The function shows worker management specifically within a gameplay phase."""
        self.show_worker_management(in_phase=True)

    def setup_styles(self):
        """The function configures visual styles for the application components."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Title.TLabel", font=("Microsoft YaHei", 18, "bold"),
                        foreground=self.colors["text_dark"], background=self.colors["bg_light"])
        style.configure("Subtitle.TLabel", font=("Microsoft YaHei", 12, "bold"),
                        foreground=self.colors["accent_blue"], background=self.colors["bg_light"])
        style.configure("DarkFrame.TLabelframe", background=self.colors["bg_light"],
                        foreground=self.colors["text_dark"], font=("Microsoft YaHei", 10, "bold"))
        style.configure("DarkFrame.TLabelframe.Label", background=self.colors["bg_light"],
                        foreground=self.colors["accent_blue"])

    def create_widgets(self):
        """The function constructs all widget elements for the main interface."""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.configure(style="DarkFrame.TLabelframe")

        title_frame = ttk.Frame(main_frame, style="DarkFrame.TLabelframe")
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))

        title_container = ttk.Frame(title_frame, style="DarkFrame.TLabelframe")
        title_container.pack(fill=tk.X, pady=5)

        tk.Label(title_container, text="⚓ 海上丝绸之路贸易大亨 / Maritime Trade Tycoon 🚢",
                 font=("Microsoft YaHei", 22, "bold"),
                 bg=self.colors["bg_light"], fg=self.colors["bg_dark"]).pack()

        tk.Label(title_container, text="⚓ 航海贸易 / Navigation | 🚢 船只升级 / Upgrades | 👥 工匠制作 / Work | 🧾 税收系统 / Taxes",
                 font=("Microsoft YaHei", 12), bg=self.colors["bg_light"],
                 fg=self.colors["accent_blue"]).pack(pady=5)

        tk.Label(title_container,
                 text="Shortcuts: Ctrl+S Save | Ctrl+N Next Phase | Ctrl+H Workers | Ctrl+R Restart | F1 Help",
                 font=("Microsoft YaHei", 9), bg=self.colors["bg_light"], fg="#666666").pack(pady=2)

        content_frame = ttk.Frame(main_frame, style="DarkFrame.TLabelframe")
        content_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        self.create_status_panel(content_frame)
        self.create_phase_panel(content_frame)
        self.create_control_panel(main_frame)
        self.create_log_panel(main_frame)

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=0)
        content_frame.columnconfigure(0, weight=0)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)

    def create_status_panel(self, parent):
        """The function builds the status display panel layout."""
        status_panel = ttk.LabelFrame(parent, text="📊 航海日志 / Navigation Log", padding="10", style="DarkFrame.TLabelframe")
        status_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        status_panel.configure(width=280)

        self.round_label = tk.Label(status_panel, text=f"🌊 Round 1/{self.max_rounds}",
                                    font=("Microsoft YaHei", 12, "bold"),
                                    bg=self.colors["bg_light"],
                                    fg=self.colors["bg_dark"])
        self.round_label.grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky=tk.W)

        self.money_label = tk.Label(status_panel, text=f"💰 Funds: 100 Gold",
                                    font=("Microsoft YaHei", 11, "bold"),
                                    bg=self.colors["bg_light"],
                                    fg=self.colors["accent_green"])
        self.money_label.grid(row=1, column=0, columnspan=2, pady=(0, 6), sticky=tk.W)

        self.score_label = tk.Label(status_panel, text=f"🏆 Reputation: 0",
                                    font=("Microsoft YaHei", 11),
                                    bg=self.colors["bg_light"],
                                    fg=self.colors["text_dark"])
        self.score_label.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)

        self.create_ship_panel(status_panel)
        self.create_inventory_panel(status_panel)

        status_panel.rowconfigure(4, weight=1)

    def create_ship_panel(self, parent):
        """The function constructs the ship status component."""
        ship_frame = ttk.LabelFrame(parent, text="🚢 船只状态 / Ship Status", padding="8", style="DarkFrame.TLabelframe")
        ship_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))

        self.ship_label = tk.Label(ship_frame, text="🚢 Merchant Ship: Level 0",
                                   font=("Microsoft YaHei", 10),
                                   bg=self.colors["bg_light"], fg=self.colors["text_dark"])
        self.ship_label.pack(anchor=tk.W, pady=2)

        self.transport_label = tk.Label(ship_frame, text="⚓ Freight: max(5, Items×2 - 0) Gold",
                                        font=("Microsoft YaHei", 10),
                                        bg=self.colors["bg_light"], fg=self.colors["accent_red"])
        self.transport_label.pack(anchor=tk.W, pady=2)

    def create_inventory_panel(self, parent):
        """The function creates the inventory panel with scroll capabilities."""
        inv_frame = ttk.LabelFrame(parent, text="📦 船舱货物 / Cargo Hold", padding="3", style="DarkFrame.TLabelframe")
        inv_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        canvas = tk.Canvas(inv_frame, height=200, highlightthickness=0, bg=self.colors["bg_light"])
        scrollbar = ttk.Scrollbar(inv_frame, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_light"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.inventory_labels = {}

        tk.Label(scrollable_frame, text="━━ 原材料 / Raw Materials ━━",
                 font=("Microsoft YaHei", 9, "bold"),
                 bg=self.colors["bg_light"],
                 fg=self.colors["accent_blue"]).pack(anchor=tk.W, pady=(5, 2), padx=5)

        for resource in self.resource_types:
            self.create_inventory_item(scrollable_frame, resource)

        tk.Frame(scrollable_frame, height=1, bg=self.colors["accent_blue"]).pack(fill=tk.X, pady=5, padx=5)

        tk.Label(scrollable_frame, text="━━ 成品 / Finished Goods ━━",
                 font=("Microsoft YaHei", 9, "bold"),
                 bg=self.colors["bg_light"],
                 fg=self.colors["accent_gold"]).pack(anchor=tk.W, pady=(5, 2), padx=5)

        for product in self.product_types:
            self.create_inventory_item(scrollable_frame, product)

        if self.weavers or self.master_weavers or self.sachet_makers:
            tk.Frame(scrollable_frame, height=1, bg=self.colors["accent_blue"]).pack(fill=tk.X, pady=5, padx=5)

            tk.Label(scrollable_frame, text="━━ 工匠 / Workers ━━",
                     font=("Microsoft YaHei", 9, "bold"),
                     bg=self.colors["bg_light"],
                     fg=self.colors["accent_blue"]).pack(anchor=tk.W, pady=(5, 2), padx=5)

            workers_info = [
                (f"👩‍🔧 织女 / Weavers", len(self.weavers)),
                (f"👩‍🎨 大师 / Masters", len(self.master_weavers)),
                (f"🌸 香囊师 / Makers", len(self.sachet_makers))
            ]

            for name, count in workers_info:
                frame = tk.Frame(scrollable_frame, bg=self.colors["bg_light"])
                frame.pack(fill=tk.X, padx=10, pady=1)

                tk.Label(frame, text=name,
                         font=("Microsoft YaHei", 9),
                         bg=self.colors["bg_light"],
                         fg=self.colors["text_dark"],
                         width=10,
                         anchor="w").pack(side=tk.LEFT)

                tk.Label(frame, text=str(count),
                         font=("Microsoft YaHei", 9, "bold"),
                         bg=self.colors["bg_light"],
                         fg=self.colors["accent_blue"],
                         width=4,
                         anchor="e").pack(side=tk.RIGHT)

    def create_inventory_item(self, parent, item):
        """The function renders a single inventory item entry."""
        color = self.resource_colors.get(item, "black")
        icon = self.resource_icons.get(item, "")

        frame = tk.Frame(parent, bg=self.colors["bg_light"])
        frame.pack(fill=tk.X, padx=10, pady=1)

        tk.Label(frame, text=icon,
                 font=("Microsoft YaHei", 10),
                 bg=self.colors["bg_light"]).pack(side=tk.LEFT, padx=(0, 3))

        tk.Label(frame, text=item,
                 font=("Microsoft YaHei", 9),
                 bg=self.colors["bg_light"],
                 fg=color,
                 width=8,
                 anchor="w").pack(side=tk.LEFT)

        label_value = tk.Label(frame, text=str(self.inventory.get(item, 0)),
                               font=("Microsoft YaHei", 9, "bold"),
                               bg=self.colors["bg_light"],
                               fg=color,
                               width=5,
                               anchor="e")
        label_value.pack(side=tk.RIGHT, padx=(0, 5))
        self.inventory_labels[item] = label_value

    def create_phase_panel(self, parent):
        """The function creates the trading phase display area."""
        self.phase_frame = ttk.LabelFrame(parent, text="🌊 贸易阶段 / Trade Phases", padding="15", style="DarkFrame.TLabelframe")
        self.phase_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.phase_content = ttk.Frame(self.phase_frame, style="DarkFrame.TLabelframe")
        self.phase_content.pack(fill=tk.BOTH, expand=True)

    def create_control_panel(self, parent):
        """The function creates the control panel with navigation buttons."""
        control_panel = ttk.Frame(parent, style="DarkFrame.TLabelframe")
        control_panel.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

        control_container = ttk.Frame(control_panel, style="DarkFrame.TLabelframe")
        control_container.pack(fill=tk.X, pady=5)

        row1_frame = ttk.Frame(control_container, style="DarkFrame.TLabelframe")
        row1_frame.pack(fill=tk.X, pady=3)

        self.start_btn = tk.Button(row1_frame, text="🚢 开始航行 / Start Voyage",
                                   font=("Microsoft YaHei", 10, "bold"),
                                   bg=self.colors["button_primary"], fg=self.colors["text_light"],
                                   relief=tk.RAISED, borderwidth=2, width=15, height=1,
                                   cursor="hand2", command=self.show_worker_management)
        self.start_btn.pack(side=tk.LEFT, padx=2)

        self.next_btn = tk.Button(row1_frame, text="⏭️ 继续航行 / Continue Voyage",
                                  font=("Microsoft YaHei", 10, "bold"),
                                  bg=self.colors["button_primary"], fg=self.colors["text_light"],
                                  relief=tk.RAISED, borderwidth=2, width=15, height=1,
                                  cursor="hand2", state=tk.DISABLED, command=self.next_phase)
        self.next_btn.pack(side=tk.LEFT, padx=2)

        row2_frame = ttk.Frame(control_container, style="DarkFrame.TLabelframe")
        row2_frame.pack(fill=tk.X, pady=3)

        buttons = [
            ("📖 航海指南 / Guide", self.show_instructions, self.colors["button_primary"]),
            ("💾 保存进度 / Save", self.save_game, self.colors["button_success"]),
            ("🔄 重新起航 / Restart", self.restart_game, self.colors["button_primary"])
        ]

        for text, command, color in buttons:
            tk.Button(row2_frame, text=text, font=("Microsoft YaHei", 10, "bold"),
                      bg=color, fg="white", relief=tk.RAISED, borderwidth=2,
                      width=15, height=1, cursor="hand2", command=command).pack(side=tk.LEFT, padx=2)


    def create_log_panel(self, parent):
        """The function builds the scrolling log panel for messages."""
        log_frame = ttk.LabelFrame(parent, text="📜 航行日志 / Voyage Log", padding="5", style="DarkFrame.TLabelframe")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(8, 0))

        log_container = ttk.Frame(log_frame, style="DarkFrame.TLabelframe")
        log_container.pack(fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(log_container, height=5, font=("Microsoft YaHei", 9),
                                bg="#F8F9FA", fg=self.colors["text_dark"],
                                wrap=tk.WORD, borderwidth=1, relief=tk.SOLID)

        scrollbar = ttk.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def log_message(self, message):
        """The function appends a message to the log display."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def clear_phase_content(self):
        """The function clears all widgets currently shown in the phase panel."""
        for widget in self.phase_content.winfo_children():
            widget.destroy()
        self.purchase_buttons.clear()
        self.order_buttons.clear()

    def update_display(self):
        """The function updates all dynamic display elements in real-time."""
        self.round_label.config(text=f"🌊 Round {self.current_round}/{self.max_rounds}")
        self.money_label.config(text=f"💰 Funds: {self.money} Gold")
        self.score_label.config(text=f"🏆 Reputation: {self.score}")
        discount = self.ship_level * 5
        self.ship_label.config(text=f"🚢 Merchant Ship: Level {self.ship_level}")
        self.transport_label.config(text=f"⚓ Freight: max(5, Items×2 - {discount}) Gold")

        for item, label in self.inventory_labels.items():
            label.config(text=str(self.inventory.get(item, 0)))

    def show_welcome(self):
        """The function displays the welcome screen upon initialization or reset."""
        self.phase = 0
        self.clear_phase_content()

        self.log_message("=" * 50)
        self.log_message("⚓ Welcome to Maritime Trade Tycoon!")
        self.log_message("🚢 Sail across ports, build your business empire!")
        self.log_message("👥 Hire artisans to craft valuable goods for higher profits!")
        self.log_message("=" * 50)

        welcome_frame = ttk.Frame(self.phase_content, style="DarkFrame.TLabelframe")
        welcome_frame.pack(fill=tk.BOTH, expand=True, pady=30)

        tk.Label(welcome_frame, text="⚓ 海上丝绸之路贸易大亨 / Maritime Trade Tycoon 🚢",
                 font=("Microsoft YaHei", 28, "bold"),
                 bg=self.colors["bg_light"], fg=self.colors["bg_dark"]).pack(pady=(20, 10))

        tk.Label(welcome_frame, text="🌊 Eight Voyages await, become the Sea Master!",
                 font=("Microsoft YaHei", 16), bg=self.colors["bg_light"],
                 fg=self.colors["accent_blue"]).pack(pady=(0, 30))

        if os.path.exists(self.save_file):
            tk.Button(welcome_frame, text="📂 继续航行 / Continue Voyage", font=("Microsoft YaHei", 12, "bold"),
                      bg=self.colors["button_success"], fg=self.colors["text_light"],
                      relief=tk.RAISED, borderwidth=3, width=20, height=2,
                      cursor="hand2", command=self.load_game).pack(pady=10)

        tk.Button(welcome_frame, text="🚢 扬帆起航 / Set Sail", font=("Microsoft YaHei", 16, "bold"),
                  bg=self.colors["button_primary"], fg=self.colors["text_light"],
                  relief=tk.RAISED, borderwidth=3, width=20, height=2,
                  cursor="hand2", command=self.start_phase1).pack(pady=20)

        tips_frame = ttk.Frame(welcome_frame, style="DarkFrame.TLabelframe")
        tips_frame.pack(pady=20)

        tips = [
            "📦 Initial Goods: Hemp×8, Silk×5, Tea×3",
            "💰 Starting Funds: 100 Gold",
            "👥 Hire artisans to craft high-value products",
            "🧾 Product sales incur VAT, end-round tax on profit",
            "🚢 8 Voyages, each has 4 Phases: Buy → Trade → Maintain → Upgrade",
            "⚓ Freight Cost: max(5, ItemCount×2 - ShipLevel×5)",
            "💾 Press Ctrl+S to save progress",
            "🎯 Goal: Accumulate Wealth and Reputation!"
        ]

        for tip in tips:
            tk.Label(tips_frame, text=tip, font=("Microsoft YaHei", 11),
                     bg=self.colors["bg_light"], fg=self.colors["text_dark"]).pack(anchor=tk.W, pady=3)

        self.update_button_states()

    def show_instructions(self):
        """The function displays the comprehensive game rules and instructions."""
        instructions = """
        ⚓ Maritime Trade Tycoon - Rules

        🚢 Objective:
        Travel 8 voyages, accumulate wealth and reputation!

       📦 Goods System:
         Raw Materials: Hemp(3-6💰), Silk(6-10💰), Tea(10-14💰)
         Finished Goods: Linen Clothes(30-42💰), Cotton Clothes(50-65💰), Brocade(70-90💰), Sachet(95-120💰)

        👥 Worker System:
        • Weaver (8 Gold/Round): Makes Linen or Cotton Clothes
        • Master (12 Gold/Round): Makes Linen, Cotton or Brocade
        • Sachet Maker (20 Gold/Round): Makes Sachets

        🧾 Tax System:
        • VAT: 5% on finished product profit margin
        • Income Tax: 10% on voyage net profit

        🌊 Voyage Phases:
        1. Port Purchase - Buy resources at ports
        2. Trade Transaction - Complete orders
        3. Maintenance - Pay upkeep fees
        4. Upgrade - Improve ships to lower costs

        ⌨️ Shortcuts:
        • Ctrl+S: Save Game
        • Ctrl+N: Next Phase
        • Ctrl+H: Manage Workers
        • Ctrl+R: Restart
        • F1: Instructions

        ⚓ Bon Voyage and Good Luck!
        """
        messagebox.showinfo("⚓ Navigation Guide", instructions)

    def start_phase1(self):
        """The function initializes Phase 1 of the voyage: Port Purchasing."""
        self.phase = 1
        self.purchase_count = 0
        self.purchased_cards.clear()
        self.clear_phase_content()

        self.log_message(f"\n⚓=== Round {self.current_round} - Phase 1: Port Purchase ===")
        self.log_message(f"💰 Current Funds: {self.money} Gold")

        self.resource_cards = []
        for i in range(5):
            card = self.generate_mixed_resource_card()
            card["id"] = i
            self.resource_cards.append(card)

        self.show_purchase_interface()
        self.update_button_states()

    def show_purchase_interface(self):
        """The function renders the card selection interface for purchasing."""
        main_container = ttk.Frame(self.phase_content, style="DarkFrame.TLabelframe")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(tk.Frame(main_container, bg=self.colors["bg_light"]), text="⚓ 港口商品采购 / Port Goods Purchase",
                 font=("Microsoft YaHei", 20, "bold"),
                 bg=self.colors["bg_light"], fg=self.colors["bg_dark"]).pack(anchor=tk.W, pady=(0, 15))

        cards_container = tk.Frame(main_container, bg=self.colors["bg_light"])
        cards_container.pack(fill=tk.BOTH, expand=True)

        self.create_scrollable_cards(cards_container, self.resource_cards, self.create_purchase_card)
        self.create_phase_bottom_buttons(main_container, "✅ 完成采购，继续航行 / Complete Purchase, Continue", self.complete_phase1)

    def start_phase2(self):
        """The function initiates Phase 2: Trade Transactions."""
        self.phase = 2
        self.order_count = 0
        self.completed_orders.clear()
        self.clear_phase_content()

        self.log_message(f"\n🤝=== Round {self.current_round} - Phase 2: Trade Transaction ===")

        self.customer_cards = []
        for i in range(5):
            order = self.generate_mixed_order()
            order["id"] = i
            self.customer_cards.append(order)

        self.show_orders_interface()
        self.update_button_states()

    def show_orders_interface(self):
        """The function displays available trade orders for completion."""
        main_container = ttk.Frame(self.phase_content, style="DarkFrame.TLabelframe")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(tk.Frame(main_container, bg=self.colors["bg_light"]), text="🤝 贸易订单 / Trade Orders",
                 font=("Microsoft YaHei", 20, "bold"),
                 bg=self.colors["bg_light"], fg=self.colors["bg_dark"]).pack(anchor=tk.W, pady=(0, 15))

        cards_container = tk.Frame(main_container, bg=self.colors["bg_light"])
        cards_container.pack(fill=tk.BOTH, expand=True)

        self.create_scrollable_cards(cards_container, self.customer_cards, self.create_order_card)
        self.create_phase_bottom_buttons(main_container, "✅ 完成交易，继续航行 / Complete Trades, Continue", self.complete_phase2)

    def create_scrollable_cards(self, parent, cards, card_creator):
        """The function manages the layout of scrollable interactive cards."""
        canvas = tk.Canvas(parent, highlightthickness=0, bg=self.colors["bg_light"])
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_light"])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        scrollbar.pack(side="right", fill="y")

        grid_frame = tk.Frame(scrollable_frame, bg=self.colors["bg_light"])
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for i in range(3):
            grid_frame.columnconfigure(i, weight=1, uniform="col", minsize=350)

        for i, card in enumerate(cards):
            row, col = self.get_card_grid_position(i, len(cards))
            card_creator(grid_frame, card, row, col)

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(0)

    def get_card_grid_position(self, index, total):
        """The function calculates the grid coordinates for a card."""
        if index < 3:
            return 0, index
        else:
            return 1, index - 3

    def create_purchase_card(self, parent, card, row, col):
        """The function creates an individual purchasable resource card widget."""
        card_frame = tk.Frame(parent, bg="#F0F8FF", relief=tk.RAISED, borderwidth=2)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        port_frame = tk.Frame(card_frame, bg="#E6F2FF")
        port_frame.pack(fill=tk.X, padx=10, pady=8)

        card_type = "Product / 成品" if card.get("is_product_card") else "Raw Material / 原材料"
        tk.Label(port_frame, text=f"📍 {card['port']} [{card_type}]",
                 font=("Microsoft YaHei", 14, "bold"),
                 bg="#E6F2FF", fg=self.colors["bg_dark"]).pack(pady=5)

        items_frame = tk.Frame(card_frame, bg="#F0F8FF")
        items_frame.pack(fill=tk.X, padx=15, pady=10)

        for resource_info in card["resources"]:
            self.create_resource_info_row(items_frame, resource_info, font_size=11)

            if card.get("is_product_card") and "material_cost" in resource_info:
                cost_frame = tk.Frame(items_frame, bg="#F0F8FF")
                cost_frame.pack(fill=tk.X, pady=2)
                tk.Label(cost_frame,
                         text=f"   📦 Material Cost: {resource_info['material_cost']} Gold ({resource_info['material_details']})",
                         font=("Microsoft YaHei", 9),
                         bg="#F0F8FF",
                         fg="#888888").pack(anchor=tk.W)

                profit_margin = resource_info['price'] - resource_info['material_cost']
                tk.Label(cost_frame,
                         text=f"   💰 Markup: +{profit_margin} Gold ({profit_margin / resource_info['material_cost'] * 100:.0f}%)",
                         font=("Microsoft YaHei", 9),
                         bg="#F0F8FF",
                         fg=self.colors["accent_red"]).pack(anchor=tk.W)

        total_frame = tk.Frame(card_frame, bg="#F0F8FF")
        total_frame.pack(fill=tk.X, padx=15, pady=8)
        tk.Label(total_frame, text=f"💰 Total: {card['total_cost']} Gold",
                 font=("Microsoft YaHei", 13, "bold"),
                 bg="#F0F8FF",
                 fg=self.colors["accent_red"]).pack(anchor=tk.W)

        is_purchased = card["id"] in self.purchased_cards
        can_afford = self.money >= card["total_cost"] and not is_purchased

        btn_text = "✅ Purchased / 已采购" if is_purchased else f"🛒 Buy ({card['total_cost']}💰)"
        btn_state = tk.DISABLED if is_purchased or not can_afford else tk.NORMAL
        
        # Changed grey background to blue as requested
        btn_bg = self.colors["button_primary"] if is_purchased or not can_afford else self.colors["button_success"] 

        btn_frame = tk.Frame(card_frame, bg="#F0F8FF")
        btn_frame.pack(fill=tk.X, padx=15, pady=(5, 12))

        btn = tk.Button(btn_frame, text=btn_text, font=("Microsoft YaHei", 12, "bold"),
                        bg=btn_bg, fg="white", relief=tk.RAISED, borderwidth=1, height=2,
                        state=btn_state, command=lambda c=card: self.purchase_card_specific(c))
        btn.pack(fill=tk.X, expand=True)
        self.purchase_buttons.append({"button": btn, "card_id": card["id"], "total_cost": card["total_cost"]})

    def create_order_card(self, parent, order, row, col):
        """The function generates the interface for trade order acceptance."""
        order_frame = tk.Frame(parent, bg="#F0F8FF", relief=tk.RAISED, borderwidth=2)
        order_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        port_frame = tk.Frame(order_frame, bg="#E6F2FF")
        port_frame.pack(fill=tk.X, padx=10, pady=8)
        order_type = "Finished Product Demand / 成品需求" if order.get("is_product_order") else "Raw Material Demand / 原材料需求"
        tk.Label(port_frame, text=f"📍 {order['demand_port']} {order_type}",
                 font=("Microsoft YaHei", 14, "bold"),
                 bg="#E6F2FF", fg=self.colors["bg_dark"]).pack(pady=5)

        items_frame = tk.Frame(order_frame, bg="#F0F8FF")
        items_frame.pack(fill=tk.X, padx=15, pady=10)

        for resource_info in order["resources"]:
            has_enough = self.inventory.get(resource_info["type"], 0) >= resource_info["required"]
            status_icon = "✅" if has_enough else "❌"
            item_frame = tk.Frame(items_frame, bg="#F0F8FF")
            item_frame.pack(fill=tk.X, pady=4)
            tk.Label(item_frame, text=status_icon, font=("Microsoft YaHei", 14),
                     bg="#F0F8FF").pack(side=tk.LEFT, padx=(0, 8))
            self.create_resource_info_row(item_frame, resource_info, show_inventory=True, font_size=11)

        transport_detail = self.show_transport_cost_detail(order["total_items"])
        transport_frame = tk.Frame(order_frame, bg="#F0F8FF")
        transport_frame.pack(fill=tk.X, padx=15, pady=5)
        tk.Label(transport_frame,
                 text=f"⚓ Freight: {transport_detail['base_cost']} - {transport_detail['discount']} = {transport_detail['final_cost']} Gold",
                 font=("Microsoft YaHei", 11), bg="#F0F8FF", fg=self.colors["accent_red"]).pack(anchor=tk.W)

        net_profit = order['reward'] - transport_detail['final_cost']

        if order.get("is_product_order"):
            product = order["resources"][0]["type"]
            estimated_vat = self.calculate_vat(product, order['reward'] / order["resources"][0]["required"])
            total_vat = estimated_vat * order["resources"][0]["required"]
            net_profit -= total_vat

        finance_frame = tk.Frame(order_frame, bg="#F0F8FF")
        finance_frame.pack(fill=tk.X, padx=15, pady=8)

        finance_text = f"💰 Reward: {order['reward']} Gold 📊 Net Profit: {net_profit} Gold"
        if order.get("is_product_order"):
            finance_text += f"\n🧾 Est. VAT: {total_vat} Gold"

        tk.Label(finance_frame, text=finance_text, font=("Microsoft YaHei", 12, "bold"),
                 bg="#F0F8FF", fg=self.colors["accent_green"] if net_profit > 0 else self.colors["accent_red"],
                 justify=tk.LEFT).pack(anchor=tk.W)

        can_complete = all(self.inventory.get(r["type"], 0) >= r["required"] for r in order["resources"])
        is_completed = order["id"] in self.completed_orders

        btn_text = "✅ Completed / 已完成" if is_completed else f"🤝 Trade (Net {net_profit}💰)"
        btn_state = tk.DISABLED if is_completed or not can_complete else tk.NORMAL
        # Changed grey background to blue as requested
        btn_bg = self.colors["button_primary"] if is_completed or not can_complete else self.colors["button_success"]

        btn_frame = tk.Frame(order_frame, bg="#F0F8FF")
        btn_frame.pack(fill=tk.X, padx=15, pady=(5, 12))

        btn = tk.Button(btn_frame, text=btn_text, font=("Microsoft YaHei", 12, "bold"),
                        bg=btn_bg, fg="white", relief=tk.RAISED, borderwidth=1, height=2,
                        state=btn_state, command=lambda o=order: self.complete_order(o))
        btn.pack(fill=tk.X, expand=True)
        self.order_buttons.append({"button": btn, "order_id": order["id"], "net_profit": net_profit})

    def create_resource_info_row(self, parent, resource_info, show_inventory=False, font_size=10):
        """The function displays detailed line item information within a card."""
        resource = resource_info["type"]
        color = self.resource_colors.get(resource, "black")
        icon = self.resource_icons.get(resource, "")

        item_frame = tk.Frame(parent, bg="#F0F8FF")
        item_frame.pack(fill=tk.X, pady=2)

        tk.Label(item_frame, text=icon, font=("Microsoft YaHei", font_size + 2),
                 bg="#F0F8FF").pack(side=tk.LEFT, padx=(0, 5))

        tk.Label(item_frame, text=resource, font=("Microsoft YaHei", font_size, "bold"),
                 bg="#F0F8FF", fg=color, width=8).pack(side=tk.LEFT)

        if "quantity" in resource_info:
            tk.Label(item_frame, text=f"×{resource_info['quantity']}",
                     font=("Microsoft YaHei", font_size), bg="#F0F8FF").pack(side=tk.LEFT, padx=5)
            if "price" in resource_info:
                tk.Label(item_frame, text=f"Unit Price: {resource_info['price']}💰",
                         font=("Microsoft YaHei", font_size), bg="#F0F8FF", fg="#666").pack(side=tk.LEFT, padx=5)
        elif "required" in resource_info:
            tk.Label(item_frame, text=f"×{resource_info['required']}",
                     font=("Microsoft YaHei", font_size), bg="#F0F8FF").pack(side=tk.LEFT, padx=5)

        if show_inventory:
            inv_color = "green" if self.inventory.get(resource, 0) >= resource_info.get("required", 0) else "red"
            tk.Label(item_frame, text=f"Inv: {self.inventory.get(resource, 0)}",
                     font=("Microsoft YaHei", font_size - 1), bg="#F0F8FF",
                     fg=inv_color).pack(side=tk.LEFT, padx=(5, 0))

    def create_phase_bottom_buttons(self, parent, text, command):
        """The function creates the large action button at the bottom of phases."""
        bottom_frame = tk.Frame(parent, bg=self.colors["bg_light"])
        bottom_frame.pack(fill=tk.X, pady=(15, 5))
        tk.Button(bottom_frame, text=text, font=("Microsoft YaHei", 13, "bold"),
                  bg=self.colors["button_primary"], fg="white", relief=tk.RAISED,
                  borderwidth=2, width=25, height=2, command=command).pack(pady=5)

    def update_purchase_buttons(self):
        """The function refreshes the state of all purchase buttons dynamically."""
        for btn_info in self.purchase_buttons:
            card_id = btn_info["card_id"]
            total_cost = btn_info["total_cost"]
            button = btn_info["button"]
            is_purchased = card_id in self.purchased_cards
            can_afford = self.money >= total_cost and not is_purchased
            
            btn_text = "✅ Purchased / 已采购" if is_purchased else f"🛒 Buy ({total_cost}💰)"
            btn_state = tk.DISABLED if is_purchased or not can_afford else tk.NORMAL
            # Changed grey background to blue as requested
            btn_bg = self.colors["button_primary"] if is_purchased or not can_afford else self.colors["button_success"] 
            button.config(text=btn_text, state=btn_state, bg=btn_bg)

    def complete_phase1(self):
        """The function transitions from purchasing to worker management."""
        if self.purchase_count == 0:
            self.log_message("⏭️ Purchasing skipped")
        else:
            self.log_message(f"✅ Purchasing ended, bought {self.purchase_count} batches")
        self.show_worker_management_in_phase()

    def update_order_buttons(self):
        """The function refreshes the state of all trade order buttons dynamically."""
        for btn_info in self.order_buttons:
            order_id = btn_info["order_id"]
            net_profit = btn_info["net_profit"]
            button = btn_info["button"]
            is_completed = order_id in self.completed_orders
            can_complete = True
            for order in self.customer_cards:
                if order["id"] == order_id:
                    can_complete = all(self.inventory.get(r["type"], 0) >= r["required"] for r in order["resources"])
                    break
            btn_text = "✅ Completed / 已完成" if is_completed else f"🤝 Trade (Net {net_profit}💰)"
            btn_state = tk.DISABLED if is_completed or not can_complete else tk.NORMAL
            # Changed grey background to blue as requested
            btn_bg = self.colors["button_primary"] if is_completed or not can_complete else self.colors["button_success"]
            button.config(text=btn_text, state=btn_state, bg=btn_bg)

    def complete_phase2(self):
        """The function concludes Phase 2 and advances to maintenance."""
        if self.order_count == 0:
            self.log_message("⏭️ Trading skipped")
        else:
            self.log_message(f"✅ Trading ended, completed {self.order_count} trades")
        self.start_phase3()

    def start_phase3(self):
        """The function handles Phase 3: Production, Wages, and Maintenance."""
        self.phase = 3
        self.clear_phase_content()

        self.log_message(f"\n👥=== Processing Worker Production ===")
        self.process_production()

        self.log_message(f"\n💰=== Paying Worker Wages ===")
        wage_result = self.pay_worker_wages()

        if wage_result == "bankruptcy":
            self.log_message("⚠️ Bankruptcy due to inability to pay wages!")
            self.show_bankruptcy_screen()
            return
        elif not wage_result:
            self.log_message("⚠️ Wage payment error occurred!")
            self.show_bankruptcy_screen()
            return

        self.log_message(f"\n🔧=== Round {self.current_round} - Phase 3: Ship Maintenance ===")

        if self.money <= 0:
            self.log_message("⚠️ Funds at 0, cannot pay maintenance!")
            self.show_bankruptcy_screen()
            return

        maintenance_frame = ttk.Frame(self.phase_content, style="DarkFrame.TLabelframe")
        maintenance_frame.pack(fill=tk.BOTH, expand=True, pady=40)

        tk.Label(maintenance_frame, text="🔧 船只维护 / Ship Maintenance", font=("Microsoft YaHei", 24, "bold"),
                 bg=self.colors["bg_light"], fg=self.colors["bg_dark"]).pack(pady=20)

        tk.Label(maintenance_frame, text=f"Monthly Fixed Maintenance Fee: {self.fixed_cost} Gold",
                 font=("Microsoft YaHei", 18), bg=self.colors["bg_light"],
                 fg=self.colors["text_dark"]).pack(pady=10)

        tk.Label(maintenance_frame, text=f"Current Funds: {self.money} Gold",
                 font=("Microsoft YaHei", 16), bg=self.colors["bg_light"],
                 fg=self.colors["accent_green"]).pack(pady=15)

        separator = tk.Frame(maintenance_frame, height=2, bg=self.colors["accent_blue"])
        separator.pack(fill=tk.X, padx=80, pady=25)

        if self.money >= self.fixed_cost:
            btn_text = f"💸 Pay {self.fixed_cost} Gold"
            btn_bg = self.colors["button_primary"]
            btn_command = self.pay_fixed_cost
        else:
            btn_text = f"⚠️ Force Pay ({self.money}/{self.fixed_cost} Gold)"
            btn_bg = self.colors["button_warning"]
            btn_command = self.force_pay_cost

        tk.Button(maintenance_frame, text=btn_text, font=("Microsoft YaHei", 16, "bold"),
                  bg=btn_bg, fg="white", relief=tk.RAISED, borderwidth=3,
                  width=25, height=2, command=btn_command).pack(pady=20)
        self.update_button_states()

    def show_bankruptcy_screen(self):
        """The function displays the failure screen and statistics for bankruptcy."""
        self.game_over = True
        self.clear_phase_content()

        self.log_message("\n" + "=" * 50)
        self.log_message("💥 Bankruptcy!")
        self.log_message("💰 Funds exhausted, cannot continue business")
        self.log_message(f"🏆 Final Reputation: {self.score}")
        self.log_message(f"🌊 Rounds Completed: {self.current_round - 1}/{self.max_rounds}")
        self.log_message("=" * 50)

        bankruptcy_frame = ttk.Frame(self.phase_content, style="DarkFrame.TLabelframe")
        bankruptcy_frame.pack(fill=tk.BOTH, expand=True, pady=30)

        tk.Label(bankruptcy_frame, text="💥",
                 font=("Microsoft YaHei", 80),
                 bg=self.colors["bg_light"],
                 fg=self.colors["accent_red"]).pack(pady=15)

        tk.Label(bankruptcy_frame, text="Ship Fleet Bankrupt!",
                 font=("Microsoft YaHei", 32, "bold"),
                 bg=self.colors["bg_light"],
                 fg=self.colors["accent_red"]).pack(pady=8)

        reason = ""
        if self.money <= 0:
            reason = "Funds depleted, unable to pay essential operational costs"
        else:
            reason = "Insufficient funds to cover maintenance and wages"

        tk.Label(bankruptcy_frame, text=reason,
                 font=("Microsoft YaHei", 16),
                 bg=self.colors["bg_light"],
                 fg=self.colors["text_dark"]).pack(pady=8)

        separator = tk.Frame(bankruptcy_frame, height=3, bg=self.colors["accent_red"])
        separator.pack(fill=tk.X, padx=100, pady=20)

        stats_frame = tk.Frame(bankruptcy_frame, bg=self.colors["bg_light"])
        stats_frame.pack(pady=15)

        stats = [
            (f"🌊 Rounds Completed:", f"{self.current_round - 1}/{self.max_rounds}"),
            (f"💰 Final Funds:", f"{self.money} Gold"),
            (f"🏆 Final Reputation:", f"{self.score}"),
            (f"🚢 Ship Level:", f"{self.ship_level}"),
            (f"👥 Worker Team:",
             f"Weavers:{len(self.weavers)} Masters:{len(self.master_weavers)} Makers:{len(self.sachet_makers)}"),
            (f"🧾 Taxes Paid:", f"{self.vat_paid + self.income_tax_paid} Gold")
        ]

        for label_text, value_text in stats:
            stat_frame = tk.Frame(stats_frame, bg=self.colors["bg_light"])
            stat_frame.pack(fill=tk.X, pady=6)
            tk.Label(stat_frame, text=label_text,
                     font=("Microsoft YaHei", 14),
                     bg=self.colors["bg_light"],
                     fg=self.colors["text_dark"]).pack(side=tk.LEFT)
            tk.Label(stat_frame, text=value_text,
                     font=("Microsoft YaHei", 14, "bold"),
                     bg=self.colors["bg_light"],
                     fg=self.colors["accent_blue"]).pack(side=tk.RIGHT)

        separator2 = tk.Frame(bankruptcy_frame, height=2, bg=self.colors["accent_blue"])
        separator2.pack(fill=tk.X, padx=100, pady=20)

        buttons_frame = tk.Frame(bankruptcy_frame, bg=self.colors["bg_light"])
        buttons_frame.pack(pady=10)

        tk.Button(buttons_frame, text="🔄 重新起航 / Restart",
                  font=("Microsoft YaHei", 16, "bold"),
                  bg=self.colors["button_primary"],
                  fg="white",
                  relief=tk.RAISED,
                  borderwidth=3,
                  width=18,
                  height=2,
                  cursor="hand2",
                  command=self.restart_game).pack(side=tk.LEFT, padx=10)

        tk.Button(buttons_frame, text="💡 Strategy Tips / 贸易策略",
                  font=("Microsoft YaHei", 14),
                  bg=self.colors["button_warning"],
                  fg="white",
                  relief=tk.RAISED,
                  borderwidth=2,
                  width=18,
                  height=2,
                  cursor="hand2",
                  command=self.show_bankruptcy_tips).pack(side=tk.LEFT, padx=10)

        self.update_button_states()

    def show_bankruptcy_tips(self):
        """The function provides strategic advice to avoid bankruptcy."""
        tips = """
        ⚓ Avoiding Bankruptcy Strategies:

        💰 Financial Management:
        1. Always maintain reserve funds for expenses
        2. Maintenance ({}) + Wages are fixed rounds costs
        3. Calculate total expenditure before buying

        👥 Worker Management:
        1. Weaver Wage: {} Gold / Round
        2. Master Wage: {} Gold / Round
        3. Maker Wage: {} Gold / Round
        4. Hire only as needed

        🛒 Buying Strategy:
        1. Reserve funds for maintenance+wages first
        2. Select high value-for-money goods
        3. Prioritize port specialties

        🤝 Trading Strategy:
        1. Prioritize highest profit orders
        2. Consider freight impact on margins
        3. Finished orders yield high profit but incur VAT

        ⚠️ Risk Control:
        1. Calculate fixed round costs: Maintenance{} + Wages
        2. Keep funds consistently > fixed costs
        3. Avoid over-expansion cash flow issues

        💾 Save game progress frequently with Ctrl+S!
        """.format(
            self.fixed_cost,
            self.WEAVER_WAGE,
            self.MASTER_WEAVER_WAGE,
            self.SACHET_MAKER_WAGE,
            self.fixed_cost
        )
        messagebox.showinfo("💡 Trade Strategy Advice", tips)

    def start_phase4(self):
        """The function handles Phase 4: Ship Upgrading and Options."""
        self.phase = 4
        self.clear_phase_content()

        self.log_message(f"\n🚢=== Round {self.current_round} - Phase 4: Ship Upgrade ===")

        main_container = ttk.Frame(self.phase_content, style="DarkFrame.TLabelframe")
        main_container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_container, highlightthickness=0, bg=self.colors["bg_light"])
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_light"])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(5, 0))
        scrollbar.pack(side="right", fill="y")

        tk.Label(scrollable_frame, text="🚢 船只升级系统 / Ship Upgrade System", font=("Microsoft YaHei", 28, "bold"),
                 bg=self.colors["bg_light"], fg=self.colors["bg_dark"]).pack(pady=25)

        separator = tk.Frame(scrollable_frame, height=3, bg=self.colors["accent_blue"])
        separator.pack(fill=tk.X, padx=80, pady=(0, 25))

        columns_container = tk.Frame(scrollable_frame, bg=self.colors["bg_light"])
        columns_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        columns_container.columnconfigure(0, weight=1)
        columns_container.columnconfigure(1, weight=1)

        current_card = tk.Frame(columns_container, bg="#E6F2FF", relief=tk.RAISED, borderwidth=3, padx=30, pady=30)
        current_card.grid(row=0, column=0, padx=(0, 20), pady=10, sticky="nsew")

        tk.Label(current_card, text="📊 当前状态 / Current Status", font=("Microsoft YaHei", 22, "bold"),
                 bg="#E6F2FF", fg=self.colors["bg_dark"]).pack(pady=(0, 25))

        status_info = [
            ("🚢 Ship Level:", f"{self.ship_level}"),
            ("⚓ Freight Discount:", f"{self.ship_level * 5} Gold"),
            ("💰 Current Funds:", f"{self.money} Gold")
        ]

        for label_text, value_text in status_info:
            info_frame = tk.Frame(current_card, bg="#E6F2FF")
            info_frame.pack(fill=tk.X, pady=10)
            tk.Label(info_frame, text=label_text, font=("Microsoft YaHei", 16),
                     bg="#E6F2FF", fg=self.colors["text_dark"]).pack(side=tk.LEFT)
            tk.Label(info_frame, text=value_text, font=("Microsoft YaHei", 16, "bold"),
                     bg="#E6F2FF", fg=self.colors["accent_blue"]).pack(side=tk.RIGHT)

        tk.Label(current_card, text="📝 Freight Formula:", font=("Microsoft YaHei", 15, "bold"),
                 bg="#E6F2FF", fg=self.colors["text_dark"]).pack(pady=(25, 8))

        formula_text = f"max(5, (Total Items × 2) - {self.ship_level * 5})"
        tk.Label(current_card, text=formula_text, font=("Microsoft YaHei", 15, "italic"),
                 bg="#E6F2FF", fg=self.colors["accent_red"]).pack(pady=8)

        upgrade_card = tk.Frame(columns_container, bg="#F0F8FF", relief=tk.RAISED, borderwidth=3, padx=30, pady=30)
        upgrade_card.grid(row=0, column=1, padx=(20, 0), pady=10, sticky="nsew")

        tk.Label(upgrade_card, text="⚡ Upgrade Options / 升级选项", font=("Microsoft YaHei", 22, "bold"),
                 bg="#F0F8FF", fg=self.colors["bg_dark"]).pack(pady=(0, 25))

        if self.ship_level < 3:
            upgrade_cost = self.ship_upgrade_cost[self.ship_level]
            next_level = self.ship_level + 1
            next_discount = next_level * 5
            can_upgrade = self.money >= upgrade_cost

            tk.Label(upgrade_card, text=f"🔼 Upgrade to Level {next_level} / 升级到 {next_level} 级",
                     font=("Microsoft YaHei", 22), bg="#F0F8FF",
                     fg=self.colors["accent_blue"]).pack(pady=20)

            details = [
                (f"💰 Upgrade Cost:", f"{upgrade_cost} Gold"),
                (f"⚓ Discount After:", f"{next_discount} Gold"),
                (f"📈 Discount Increase:", f"+5 Gold")
            ]

            for label_text, value_text in details:
                detail_frame = tk.Frame(upgrade_card, bg="#F0F8FF")
                detail_frame.pack(fill=tk.X, pady=10)
                tk.Label(detail_frame, text=label_text, font=("Microsoft YaHei", 16),
                         bg="#F0F8FF", fg=self.colors["text_dark"]).pack(side=tk.LEFT)
                tk.Label(detail_frame, text=value_text, font=("Microsoft YaHei", 16, "bold"),
                         bg="#F0F8FF",
                         fg=self.colors["accent_red"] if "Cost" in label_text or "费用" in label_text else self.colors["accent_green"]).pack(
                    side=tk.RIGHT)

            separator = tk.Frame(upgrade_card, height=2, bg=self.colors["accent_blue"])
            separator.pack(fill=tk.X, pady=25)

            button_frame = tk.Frame(upgrade_card, bg="#F0F8FF")
            button_frame.pack(pady=15)

            if can_upgrade:
                btn_text = f"🚢 Upgrade Now to Level {next_level}\n💰 {upgrade_cost} Gold"
                btn_bg = self.colors["button_primary"]
                btn_state = tk.NORMAL
                btn_command = self.upgrade_ship
            else:
                btn_text = f"❌ Insufficient Funds\nNeed {upgrade_cost}, Have {self.money}"
                btn_bg = self.colors["button_primary"] # Changed to blue
                btn_state = tk.DISABLED
                btn_command = None

            tk.Button(button_frame, text=btn_text, font=("Microsoft YaHei", 16, "bold"),
                      bg=btn_bg, fg="white", relief=tk.RAISED, borderwidth=3,
                      width=30, height=4, state=btn_state,
                      cursor="hand2" if can_upgrade else "arrow",
                      command=btn_command if can_upgrade else None).pack()
        else:
            max_level_frame = tk.Frame(upgrade_card, bg="#F0F8FF")
            max_level_frame.pack(fill=tk.BOTH, expand=True, pady=50)
            tk.Label(max_level_frame, text="🎉 Fully Upgraded / 已满级！", font=("Microsoft YaHei", 24, "bold"),
                     bg="#F0F8FF", fg=self.colors["accent_gold"]).pack(pady=25)
            tk.Label(max_level_frame, text="🚢 Your ship reached max level",
                     font=("Microsoft YaHei", 18), bg="#F0F8FF",
                     fg=self.colors["text_dark"]).pack(pady=15)
            tk.Label(max_level_frame, text=f"⚓ Max Freight Discount: {self.ship_level * 5} Gold",
                     font=("Microsoft YaHei", 18), bg="#F0F8FF",
                     fg=self.colors["accent_green"]).pack(pady=15)

        bottom_container = tk.Frame(scrollable_frame, bg=self.colors["bg_light"])
        bottom_container.pack(fill=tk.X, pady=(30, 20))
        buttons_frame = tk.Frame(bottom_container, bg=self.colors["bg_light"])
        buttons_frame.pack()

        buttons = [
            ("📖 Upgrade Rules / 升级规则", self.show_upgrade_rules, self.colors["button_primary"]),
            ("⏭️ Skip Upgrade / 跳过升级", self.skip_upgrade, self.colors["button_warning"]),
            ("🔙 Return to Maintenance / 返回维护", lambda: self.start_phase3(), self.colors["button_primary"])
        ]

        for text, command, color in buttons:
            tk.Button(buttons_frame, text=text, font=("Microsoft YaHei", 13, "bold"),
                      bg=color, fg="white", relief=tk.RAISED, borderwidth=2,
                      width=15, height=2, cursor="hand2", command=command).pack(side=tk.LEFT, padx=10)

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(0)
        self.update_button_states()

    def upgrade_ship(self):
        """The function executes the ship upgrading process."""
        if self.ship_level >= 3:
            return

        upgrade_cost = self.ship_upgrade_cost[self.ship_level]
        next_level = self.ship_level + 1

        if self.money >= upgrade_cost:
            self.money -= upgrade_cost
            self.ship_level = next_level
            new_discount = self.ship_level * 5
            self.log_message(f"🎉 Ship Successfully Upgraded to Level {self.ship_level}!")
            self.log_message(f"   💰 Cost: {upgrade_cost} Gold")
            self.log_message(f"   ⚓ New Freight Discount: {new_discount} Gold")
            messagebox.showinfo("Upgrade Success",
                                f"🎉 Ship upgraded to Level {self.ship_level}!\n\n"
                                f"💰 Cost: {upgrade_cost} Gold\n"
                                f"⚓ Freight Discount: {new_discount} Gold")
            self.update_display()
            self.start_phase4()
        else:
            messagebox.showerror("Insufficient Funds",
                                 f"❌ Not enough money!\n\n"
                                 f"Needed: {upgrade_cost} Gold\n"
                                 f"Have: {self.money} Gold")
            self.log_message(f"❌ Upgrade failed! Need {upgrade_cost} Gold")

    def show_upgrade_rules(self):
        """The function explains how ship upgrades and freight discounts work."""
        rules = """
        🚢 Ship Upgrade Rules:

        📊 Freight Cost Formula:
        Freight = max(5, (Total Items × 2) - (Ship Level × 5))

        ⚓ Explanation:
        • Base Freight: 2 Gold per item
        • Ship Upgrade: -5 Gold total freight per level
        • Minimum Freight: 5 Gold (fixed floor)

        🚢 Costs and Effects:
        • Level 0 → 1: 15 Gold, Discount 5 Gold
        • Level 1 → 2: 25 Gold, Discount 10 Gold
        • Level 2 → 3: 40 Gold, Discount 15 Gold (Max)

        💡 Strategy:
        • Upgrade ship early to reduce costs
        • Freight is fixed expense, upgrade saves long term
        """
        messagebox.showinfo("🚢 Upgrade Rules Details", rules)

    def skip_upgrade(self):
        """The function skips the upgrade phase to proceed."""
        self.log_message("⏭️ Skipped Ship Upgrade")
        self.end_round()

    def end_game(self):
        """The function calculates final scores and displays the end-game screen."""
        self.log_message("\n" + "=" * 50)
        self.log_message("🎮 Maritime Trade Tycoon - Game Over!")
        self.log_message(f"💰 Final Funds: {self.money} Gold")
        self.log_message(f"🏆 Final Reputation: {self.score}")
        self.log_message(f"🧾 Total Taxes Paid: {self.vat_paid + self.income_tax_paid} Gold")
        self.log_message(
            f"👥 Worker Team: Weavers{len(self.weavers)} Masters{len(self.master_weavers)} Makers{len(self.sachet_makers)}")

        if self.score >= 300:
            rating = "👑 King of Silk Road"
        elif self.score >= 200:
            rating = "🏆 Maritime Tycoon"
        elif self.score >= 100:
            rating = "⭐ Successful Merchant"
        elif self.score >= 50:
            rating = "👍 Qualified Trader"
        else:
            rating = "🌊 Novice Merchant"

        self.log_message(f"📈 Rank: {rating}")
        self.log_message("=" * 50)

        self.clear_phase_content()

        result_frame = ttk.Frame(self.phase_content, style="DarkFrame.TLabelframe")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=40)

        tk.Label(result_frame, text="🎮 Game Over / 游戏结束!", font=("Microsoft YaHei", 32, "bold"),
                 bg=self.colors["bg_light"], fg=self.colors["bg_dark"]).pack(pady=20)

        tk.Label(result_frame, text=f"🏆 Final Reputation: {self.score}",
                 font=("Microsoft YaHei", 22, "bold"),
                 bg=self.colors["bg_light"], fg=self.colors["accent_blue"]).pack(pady=10)

        tk.Label(result_frame, text=f"💰 Final Funds: {self.money} Gold",
                 font=("Microsoft YaHei", 20),
                 bg=self.colors["bg_light"], fg=self.colors["accent_green"]).pack(pady=10)

        tk.Label(result_frame, text=f"📈 Merchant Rank: {rating}",
                 font=("Microsoft YaHei", 20),
                 bg=self.colors["bg_light"], fg=self.colors["accent_gold"]).pack(pady=20)

        tk.Button(result_frame, text="🔄 重新起航 / Restart", font=("Microsoft YaHei", 18, "bold"),
                  bg=self.colors["button_primary"], fg="white", relief=tk.RAISED,
                  borderwidth=3, width=20, height=2,
                  command=self.restart_game).pack(pady=25)

        self.delete_save()
        self.update_button_states()

    def restart_game(self):
        """The function resets all game variables and starts fresh."""
        if messagebox.askyesno("Restart Voyage / 重新起航", "Confirm restarting the maritime journey?"):
            self.inventory = {"麻布": 8, "丝绸": 5, "茶叶": 3, "麻衣": 0, "布衣": 0, "绫罗绸缎": 0, "香囊": 0}
            self.money = 100
            self.score = 0
            self.current_round = 1
            self.ship_level = 0
            self.phase = 0
            self.game_over = False
            self.purchase_count = 0
            self.order_count = 0
            self.resource_cards = []
            self.customer_cards = []
            self.purchased_cards.clear()
            self.completed_orders.clear()
            self.weavers = []
            self.master_weavers = []
            self.sachet_makers = []
            self.total_revenue = 0
            self.total_costs = 0
            self.material_costs = 0
            self.worker_wages = 0
            self.maintenance_costs = 0
            self.vat_paid = 0
            self.income_tax_paid = 0
            self.round_revenue = 0
            self.round_costs = 0

            self.log_text.delete(1.0, tk.END)
            self.update_display()
            self.show_welcome()
            self.delete_save()

    def update_button_states(self):
        """The function enables or disables control buttons based on game context."""
        if self.game_over:
            self.start_btn.config(state=tk.DISABLED, text="⚠️ Game Over / 游戏结束")
            self.next_btn.config(state=tk.DISABLED, text="⏭️ Continue Voyage / 继续航行")
            return

        if self.phase == 0:
            self.start_btn.config(state=tk.NORMAL, text=f"🚢 Start Round {self.current_round} / 开始第{self.current_round}航程")
            self.next_btn.config(state=tk.DISABLED, text="⏭️ Continue Voyage / 继续航行")
        elif self.phase in [1, 2]:
            self.start_btn.config(state=tk.DISABLED, text="🚢 On Voyage... / 航行中...")
            self.next_btn.config(state=tk.NORMAL, text="⏭️ Continue Voyage / 继续航行")
        elif self.phase in [3, 4]:
            self.start_btn.config(state=tk.DISABLED, text="🚢 On Voyage... / 航行中...")
            self.next_btn.config(state=tk.NORMAL, text="⏭️ Continue Voyage / 继续航行")

    def next_phase(self):
        """The function navigates to the appropriate next phase logic."""
        phase_actions = {
            1: self.complete_phase1,
            2: self.complete_phase2,
            3: (self.pay_fixed_cost if self.money >= self.fixed_cost else self.force_pay_cost),
            4: self.skip_upgrade
        }

        action = phase_actions.get(self.phase)
        if action:
            action()

    def run(self):
        """The function starts the main event loop for the GUI application."""
        self.window.mainloop()


if __name__ == "__main__":
    app = MaritimeTradeGameGUI().run()