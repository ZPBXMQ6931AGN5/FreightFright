import time
import random
import sys
import os

# --- 基础配置与工具 ---

def pause():
    print()
    input("按任意键退出游戏...")

class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"          # 危险/致命规则/警告
    GREEN = "\033[32m"        # 安全/正常系统
    YELLOW = "\033[33m"       # 警告/手写字迹
    BLUE = "\033[34m"         # 机械/冷漠的系统音
    MAGENTA = "\033[35m"      # 精神污染/幻觉
    CYAN = "\033[36m"         # 提示
    BOLD = "\033[1m"
    ITALIC = "\033[3m"

# --- 新增：互动检查单系统 ---

def interactive_checklist():
    clear_screen()
    type_print(f"{Colors.BOLD}>>> 进入交互式检查单程序 (Interactive Checklist) <<<{Colors.RESET}")
    type_print("提示：请输入括号内的指令（不区分大小写）。输入错误可能导致系统故障。", 0.03, Colors.CYAN)
    
    steps = [
        {"system": "HYDRAULIC AUX PUMPS", "cmd": "AUTO", "msg": "液压辅助泵已设为自动。"},
        {"system": "ANTI-ICE ENGINE 2", "cmd": "ON", "msg": "2号引擎防冰已开启。"},
        {"system": "LANDING GEAR", "cmd": "DOWN", "msg": "起落架放下。四盏绿灯。"}
    ]
    
    # 随机加入一个恐怖检查项
    if state.san < 60:
        steps.insert(1, {"system": "PASSENGER OXYGEN", "cmd": "CUT", "msg": "客舱氧气已切断...等等，这是货机。"})

    for step in steps:
        print(f"\n[{step['system']}] 设置为 -> ", end="")
        user_input = input().strip().upper()
        
        if user_input == step['cmd']:
            type_print(f"CHECK. {step['msg']}", 0.02, Colors.GREEN)
            time.sleep(0.5)
        else:
            type_print(f"ERR: 指令错误！系统发出刺耳的警报。", 0.05, Colors.RED)
            state.change_san(-10)
            state.trust_md11 -= 10
            type_print("驾驶舱的灯光闪烁了一下，仿佛飞机在表达不满。", 0.05, Colors.YELLOW)

# --- 新增：黑山基地货物互动 (Risk/Reward) ---

def cargo_hold_event():
    clear_screen()
    type_print("飞航工程师 Mike 突然盯着监控屏幕发抖。", 0.03)
    type_print("'机长，主货舱的温度传感器失效了。那是放[B-12]生物样本的地方。'", 0.03, Colors.YELLOW)
    print(f"\n{Colors.CYAN}【抉择】{Colors.RESET}")
    print("1. 坚守驾驶舱：'不要管它，只要不着火就行。' (安全，无特殊能力)")
    print("2. 亲自去查看：'我去看看。' (极度危险，解锁[真实视野])")
    
    choice = input("你的选择 (1/2): ")
    
    if choice == '1':
        type_print("你决定不冒这个险。Mike 似乎松了一口气，但监控屏幕上闪过一张人脸。", 0.03)
        return
        
    elif choice == '2':
        type_print("你离开驾驶舱，穿过幽暗的过道进入主货舱。", 0.03)
        type_print("这里冷得刺骨。你找到了标有 [BLACK MESA / B-12] 的集装箱。", 0.03)
        type_print("箱子漏了一条缝，里面透出不可名状的紫光。", 0.03, Colors.MAGENTA)
        type_print("你忍不住往里面看了一眼——", 0.1, Colors.RED)
        
        # 视觉冲击
        clear_screen()
        print(Colors.MAGENTA + "👁️  " * 10 + Colors.RESET)
        type_print("你看到了维度的缝隙。你看到了死在你之后的人。你理解了所有规则的含义。", 0.05, Colors.MAGENTA)
        print(Colors.MAGENTA + "👁️  " * 10 + Colors.RESET)
        
        type_print("你回到了驾驶舱。你感觉双眼灼痛，但世界变得'清晰'了。", 0.03)
        
        state.san -= 40  # 巨额扣除
        state.night_vision = True # 获得能力
        state.endings_unlocked.append("TRUE_SIGHT")

# --- 新增：ATC 空管交互 (基于真实视野) ---

def atc_interaction():
    clear_screen()
    type_print("无线电里传来杂音...", 0.05)
    
    # 普通玩家看到的信息
    msg_1 = "FedEx 888, Shannon Control. Radar contact lost. Turn right heading 180."
    msg_2 = "FedEx 888, Swissair 111 here... heavy smoke... we need priority..."
    
    print(f"\n{Colors.BLUE}[RADIO] {msg_1}{Colors.RESET}")
    
    if state.night_vision:
        # 有真实视野玩家看到的真相
        print(f"{Colors.RED}[真实视野] 信号来源：大西洋海底，深度3000米。发送者：未知有机体。{Colors.RESET}")
        print(f"{Colors.RED}[解析] Heading 180 指向风暴中心。它想让你坠毁。{Colors.RESET}")
    else:
        print(f"{Colors.CYAN}(你觉得这个指令有点奇怪，但听起来像是管制的口音){Colors.RESET}")

    time.sleep(2)
    print("-" * 30)
    print(f"\n{Colors.BLUE}[RADIO] {msg_2}{Colors.RESET}")
    
    if state.night_vision:
         print(f"{Colors.GREEN}[真实视野] 信号来源：1998年的时间回响。这是真实的历史记录。{Colors.RESET}")
    else:
         print(f"{Colors.YELLOW}(你的脊背发凉。Swissair 111 不是二十年前就坠毁了吗？){Colors.RESET}")

    print(f"\n{Colors.CYAN}【回复】{Colors.RESET}")
    print("A. 听从 'Shannon Control' (右转航向 180)")
    print("B. 联系 Swissair 111 (试图对话)")
    print("C. 保持当前航向，无视所有指令")

    choice = input("你的选择 (A/B/C): ").upper()
    
    if choice == 'A':
        if state.night_vision:
            type_print("你知道你在自杀。但你无法抗拒那紫色的召唤...", 0.05, Colors.RED)
        else:
            type_print("你执行了指令。飞机飞入了一团黑云中。", 0.05)
        state.change_san(-20)
        return "BAD_ATC"
    elif choice == 'B':
        type_print("你按下发话按钮：'SR111, 这里是 FX888...'", 0.05)
        type_print("无线电那头传来一声尖啸，所有仪表盘瞬间黑屏。", 0.05, Colors.RED)
        state.trust_md11 -= 10 # 吓到了飞机
        return "GHOST_ATC"
    elif choice == 'C':
        type_print("你关掉了无线电。'闭嘴，我们在飞自己的路。'", 0.05, Colors.GREEN)
        type_print("MD-11 的自动驾驶指示灯亮起，仿佛在为你点赞。", 0.05)
        state.trust_md11 += 15
        return "GOOD_ATC"
    
    return "GOOD_ATC"

# --- 扩展包整合入口 ---

def expansion_chapter(setpart,enable):
    """
    将新功能串联起来的章节
    """
    global res
        
    if setpart == 0:
        clear_screen()
        print(f"{Colors.BOLD}{Colors.YELLOW}=== 扩展内容：深渊凝视 ==={Colors.RESET}")
        print("本章节包含新增的游戏机制：互动指令、生物危害、亡灵通讯。")
        if input("是否跳过此扩展内容？(y/n): ").lower() == 'y':
            return False

    elif setpart == 1:
        # 1. 检查单环节
        if state.if_atc:
            atc_effect(res)
        input("\n[按回车开始进近前检查单程序]...")
        interactive_checklist()        
    
    elif setpart == 2: 
        # 2. 货舱环节
        if state.san > 0:
            cargo_hold_event()
    
    elif setpart == 3:
        # 3. ATC 环节
        if state.san > 0: 
            res = atc_interaction()
            state.if_atc = True
            # 这里可以根据 res 影响后续剧情
    
    else:
        print(f"{Colors.BOLD}{Colors.RED}ERROR{Colors.RESET}")

def atc_effect(res):
    """
    根据 ATC 交互的结果 (res) 决定命运走向
    res: 全局变量，取值为 "BAD_ATC", "GHOST_ATC", "GOOD_ATC"
    """
    clear_screen()
    type_print(f"{Colors.BOLD}>>> 正在执行航向指令... <<<{Colors.RESET}", 0.05)
    time.sleep(1)

    # ---------------------------------------------------------
    # 分支 1：听信了邪恶指令 (BAD_ATC) -> 结局 5：深海之下
    # ---------------------------------------------------------
    if res == "BAD_ATC":
        type_print("\n你转动航向旋钮至 180 度。", 0.05)
        type_print("飞机穿过了云层，但你没有看到陆地。", 0.05)
        
        # 视觉/文字恐怖效果
        if state.night_vision:
            # 拥有真实视野的玩家会看到真相
            type_print(f"{Colors.MAGENTA}[真实视野] 你看到海面不是水，而是无数只向上伸出的苍白手臂。{Colors.RESET}", 0.04)
            type_print(f"{Colors.MAGENTA}黑山基地的货物正在发光，它想回家。{Colors.RESET}", 0.04)
        else:
            type_print("高度表疯狂旋转。大海似乎倒悬在天空之上。", 0.05, Colors.RED)

        type_print("\nEICAS 屏幕显示：TERMINATE. (终止)", 0.1, Colors.RED)
        type_print("你感觉到失重，水瞬间灌满了驾驶舱。", 0.05)
        
        print(f"\n{Colors.RED}========================================{Colors.RESET}")
        print(f"{Colors.BOLD}   【结局 5：深海的重逢 (Deep Dive)】   {Colors.RESET}")
        print(f"{Colors.RED}========================================{Colors.RESET}")
        print("你听从了来自深渊的诱导。你们成为了那里的一部分。")
        pause()
        sys.exit()

    # ---------------------------------------------------------
    # 分支 2：试图与亡魂沟通 (GHOST_ATC) -> 结局 6：系统夺舍
    # ---------------------------------------------------------
    elif res == "GHOST_ATC":
        type_print("\n你试图再次呼叫瑞航 111...", 0.05)
        type_print("驾驶舱内所有的灯光突然熄灭。", 0.02)
        time.sleep(1)
        
        # 模拟系统重启/被入侵
        print(f"{Colors.YELLOW}[SYSTEM ERROR] FMC DATABASE CORRUPTED{Colors.RESET}")
        print(f"{Colors.YELLOW}[SYSTEM ERROR] AUTOPILOT DISCONNECT{Colors.RESET}")
        
        type_print("\n一个冰冷的声音直接在你的脑海中响起：", 0.05, Colors.MAGENTA)
        type_print(f"{Colors.ITALIC}“既然你这么想念我们，那就留下来陪我们吧。”{Colors.RESET}", 0.06, Colors.MAGENTA)
        
        type_print("\n操纵杆变得滚烫，仿佛握着燃烧的金属。", 0.04)
        type_print("MD-11 的机魂被过去的记忆吞噬了，它拒绝执行你的任何指令。", 0.04, Colors.RED)
        
        print(f"\n{Colors.RED}========================================{Colors.RESET}")
        print(f"{Colors.BOLD}   【结局 6：幽灵航班 (Ghost Flight)】   {Colors.RESET}")
        print(f"{Colors.RED}========================================{Colors.RESET}")
        print("这架飞机永远不会降落了。它将在大西洋上空盘旋，直到时间的尽头。")
        pause()
        sys.exit()

    # ---------------------------------------------------------
    # 分支 3：坚定意志 (GOOD_ATC) -> 继续游戏
    # ---------------------------------------------------------
    elif res == "GOOD_ATC":
        type_print("\n你切断了干扰源，握紧了操纵杆。", 0.05)
        type_print("“这里是联邦快递 888，我们要降落了。”", 0.05, Colors.GREEN)
        
        # 机魂的反馈
        if state.trust_md11 > 0:
            type_print("\nMD-11 的引擎轰鸣声变得平稳有力。", 0.03, Colors.BLUE)
            type_print("EICAS 屏幕闪过一行字：I TRUST YOU. (我相信你)", 0.05, Colors.GREEN)
            state.change_san(10) # 恢复 SAN 值
        else:
            type_print("\n飞机还在震动，但勉强服从了你的控制。", 0.03)

        type_print("\n前方的云层散开，日内瓦的跑道灯光隐约可见。", 0.05)
        # 进入原来的最终环节

def type_print(text, delay=0.03, color=Colors.RESET):
    """打字机效果输出"""
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(Colors.RESET + "\n")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- 游戏状态管理 ---

class GameState:
    def __init__(self):
        self.san = 100
        self.difficulty = "Normal"
        self.endings_unlocked = []
        self.is_passenger_mode = False # 是否触发瑞航111幻觉
        self.trust_md11 = 0 # 对机魂的亲密度
        self.try_times = 0
        self.if_atc = False
        self.night_vision = False
        self.known_atc_ghosts = False
        self.ext_enable = True

    def change_san(self, amount):
        self.san += amount
        if self.san > 100: self.san = 100
        if self.san <= 0:
            self.trigger_insanity_end()
    
    def trigger_insanity_end(self):
        clear_screen()
        type_print("SAN值归零...", 0.1, Colors.RED)
        type_print("驾驶舱的门打开了。你看见后面坐满了浑身湿透的乘客。", 0.05, Colors.RED)
        type_print("他们都在看着你微笑。", 0.05, Colors.RED)
        type_print("【结局 -1：深海的重逢】", 0.1, Colors.BOLD)
        pause()
        sys.exit()

state = GameState()

# --- 剧情文本块 ---

def show_manifest():
    clear_screen()
    print(f"{Colors.BOLD}=== FLIGHT MANIFEST: FX888 ==={Colors.RESET}")
    print(f"机型: McDonnell Douglas MD-11F")
    print(f"航线: JFK (纽约) -> GVA (日内瓦)")
    print(f"巡航高度: FL330 | 气象: 大西洋上空由于低压槽影响，有中度颠簸")
    print(f"机组: 机长(玩家), 副驾(John), 飞航工程师(Mike)")
    print("-" * 30)
    print(f"{Colors.YELLOW}特殊货物清单 (Black Mesa 委托):{Colors.RESET}")
    print("1. [A-77] 高能物理实验样本 (密封铅箱) - 绝对禁止打开")
    print("2. [B-12] 生物组织样本 (需保持 -70°C)")
    print("-" * 30)
    input("\n按回车键签署放行单并起飞...")

def eicas_system_check():
    """模拟 EICAS 屏幕"""
    print(f"\n{Colors.BLUE}[ EICAS DISPLAY ]{Colors.RESET}")
    status = [
        "ENG 1 N1 ... 88.4%",
        "ENG 2 N1 ... 88.4%",
        "ENG 3 N1 ... 88.4%",
        "CABIN ALT ... 6000FT",
    ]
    
    # 根据SAN值插入异常信息
    if state.san < 80:
        status.append(f"{Colors.RED}DO NOT LOOK BEHIND{Colors.RESET}")
    if state.san < 60:
        status[1] = f"{Colors.MAGENTA}ENG 2 SOUL ... TRAPPED{Colors.RESET}"
    
    for s in status:
        print(s)
    print("-" * 20)

# --- 规则生成系统 ---

def check_rules_phase_1():
    """第一阶段规则：起飞后平飞阶段"""
    clear_screen()
    eicas_system_check()
    type_print("\n你拿起《驾驶舱操作检查单》，发现上面多了一些奇怪的字迹...", 0.05)
    
    print("\n" + "="*10 + " 联邦快递 MD-11F 补充操作守则 " + "="*10)
    
    # 规则1：正常
    print(f"1. 本机为{Colors.BOLD}货机{Colors.RESET}。机上只有三名机组成员。")
    
    # 规则2：警告 (SAN影响)
    if state.san > 50:
        print(f"2. 如果你听到主货舱传来哭声，请检查《货舱灭火程序》，但{Colors.RED}不要{Colors.RESET}去查看。")
    else:
        print(f"2. {Colors.MAGENTA}主货舱的哭声是正常的。那是风声。去看看也没关系。{Colors.RESET}")

    # 规则3：手写规则 (字迹潦草)
    print(f"{Colors.YELLOW}3. (手写) 别相信TCAS。那是波音的人在看着我们。{Colors.RESET}")
    
    # 规则4：关于MD-11机魂
    print(f"4. 既然我们没有GE90引擎，就不要强迫她飞得太快。她会生气的。")

    print("="*40)

# --- 核心剧情节点 ---

def scene_1_cockpit():
    clear_screen()
    type_print("大西洋上空，夜，33000英尺。", 0.05)
    type_print("单调的引擎轰鸣声。副驾 John 正在低头喝咖啡，工程师 Mike 在检查燃油面板。", 0.05)
    type_print("突然，EICAS 屏幕闪烁了一下。", 0.02, Colors.YELLOW)
    
    check_rules_phase_1()
    
    print(f"\n{Colors.CYAN}【抉择时刻】{Colors.RESET}")
    print("A. 询问副驾有没有看到规则。")
    print("B. 默默记下规则，检查TCAS系统。")
    print("C. 嘲笑MD-11是'被淘汰的破烂'，拍打仪表盘。")
    
    choice = input("你的选择 (A/B/C): ").upper()
    
    if choice == 'A':
        type_print("副驾 John 困惑地看着你：“机长，你在说什么？检查单上只有正常的燃油平衡程序。”", 0.03)
        type_print("你意识到只有你能看到那些字。你的SAN值下降了。", 0.03, Colors.MAGENTA)
        state.change_san(-15)
        return "B_ROUTE"
    elif choice == 'B':
        type_print("你决定保持沉默并警惕。你注意到TCAS屏幕上出现了一个幽灵信号，就在你们正下方。", 0.03)
        state.change_san(-5)
        return "A_ROUTE"
    elif choice == 'C':
        type_print("当你拍打仪表盘时，自动油门突然断开，飞机猛烈下坠！", 0.02, Colors.RED)
        type_print("EICAS 显示：DON'T TOUCH ME.", 0.1, Colors.RED)
        type_print("MD-11 机魂被激怒了。", 0.05)
        state.san -= 30
        state.trust_md11 -= 20
        return "CRASH_ROUTE"
    else:
        return scene_1_cockpit()

def scene_2_event(route):
    clear_screen()
    eicas_system_check()
    
    if route == "CRASH_ROUTE":
        type_print("飞机失去控制，无论你怎么拉杆都无济于事。", 0.05, Colors.RED)
        type_print("【结局 0：傲慢的代价】", 0.1)
        pause()
        sys.exit()

    type_print("\n飞行过半。货舱里的那些[黑山基地]的箱子开始渗出紫色的雾气。", 0.03)
    type_print("工程师 Mike 突然说话了，但声音听起来像个年轻的瑞士女性（德语口音）：", 0.03, Colors.MAGENTA)
    type_print(f"{Colors.ITALIC}“Is the entertainment system working? The passengers in First Class are complaining.”{Colors.RESET}", 0.04)
    
    if state.try_times == 0:
        print(f"\n{Colors.CYAN}【san值: {state.san}】此时你的直觉告诉你：{Colors.RESET}")
        print("1. 愤怒地吼叫：'这是货机！没有头等舱！'")
        print("2. 查看 EICAS 上的新规则。")
        choice = input("你的选择 (1/2): ")
    else:
        print(f"\n{Colors.CYAN}【san值: {state.san}】此时你的直觉告诉你：{Colors.RESET}")
        print("1. 愤怒地吼叫：'这是货机！没有头等舱！'")
        print("2. 查看 EICAS 上的新规则。")
        print("3. 温柔地回答（遵循隐藏规则）：'我们会尽力修复，请稍安勿躁。'")
        choice = input("你的选择 (1/2/3): ")

    if choice == '1':
        if state.san < 50:
            type_print("你的吼叫声在驾驶舱回荡，但当你转头，发现后面不是墙壁，而是通往客舱的帘子...", 0.05, Colors.RED)
            state.is_passenger_mode = True
            swissair_event()
        else:
            type_print("Mike 猛地惊醒：'长官？我刚才睡着了吗？'", 0.03)
            type_print("你稳住了局面，但精神极度疲惫。", 0.03)
            state.change_san(-10)
    
    elif choice == '2':
        type_print(f"\n{Colors.RED}新的规则出现在挡风玻璃上：{Colors.RESET}",0.03)
        type_print("1. 既然波音买下了麦道，那我们都是波音的孩子。",0.03)
        type_print(f"2. {Colors.YELLOW}(涂改) 不，长滩（Long Beach）永远不会原谅西雅图。{Colors.RESET}",0.03)
        type_print("3. 如果闻到烧焦的电线味，那是瑞航111的记忆，请立刻切断娱乐系统电源。",0.03)
        time.sleep(1)
        state.change_san(-5)
        state.try_times += 1
        # 递归调用选择
        return scene_2_event(route)

    elif choice == '3' and state.try_times != 0:
        type_print("驾驶舱的空气瞬间安静下来。那股紫色的雾气似乎退却了。", 0.03)
        type_print("仪表盘上的灯光变得柔和。MD-11 似乎很感激你的礼貌。", 0.03, Colors.GREEN)
        state.trust_md11 += 20
        state.change_san(10)
    
    else:
        return scene_2_event(route)

def swissair_event():
    clear_screen()
    type_print("驾驶舱里弥漫着烧焦的气味。这是1998年9月2日的气味。", 0.05, Colors.RED)
    type_print("GPWS 疯狂报警：PULL UP! PULL UP!", 0.02, Colors.RED)
    type_print("你的身份正在重叠。你是联邦快递的机长，也是瑞航的Urs Zimmermann。", 0.04)
    
    print("\n快！怎么办？")
    print("A. 执行瑞航111当年的程序：向哈利法克斯备降，盘旋耗油。")
    print("B. 相信黑山基地的货物：启动物理实验材料[A-77]（现实扭曲）。")
    print("C. 执行联邦快递紧急程序：直飞最近机场，不耗油，立即迫降。")

    choice = input("选择 (A/B/C): ").upper()

    if choice == 'A':
        type_print("历史是无法改变的圆环。大火吞噬了仪表盘...", 0.05, Colors.RED)
        type_print("【结局 2：历史重演】 你成为了瑞航111的一员。", 0.1)
    elif choice == 'B':
        type_print("你打开了[A-77]。空间开始折叠。", 0.05, Colors.MAGENTA)
        type_print("飞机瞬间出现在日内瓦停机坪上，但外面的人都长着三只眼睛。", 0.05)
        type_print("【结局 3：异次元着陆】 货物安全送达，但这是哪里？", 0.1)
    elif choice == 'C':
        type_print("你打破了历史的魔咒！不管什么耗油量了，你也无视了着陆重量限制！", 0.04, Colors.GREEN)
        type_print("MD-11 发出了悲鸣，但结构撑住了。", 0.04)
        true_ending_check()

def final_approach():
    clear_screen()
    type_print("日内瓦近在咫尺。暴风雪。", 0.05)
    type_print("EICAS 屏幕上最后一条规则：", 0.05)
    
    if state.trust_md11 > 10:
        print(f"{Colors.GREEN}感谢你没有像美国航空(AA)那样抛弃我。{Colors.RESET}")
        print(f"{Colors.GREEN}你可以使用 ILS 进近。我会带你回家。{Colors.RESET}")
        landing_success()
    else:
        print(f"{Colors.RED}我是波音为了消灭竞争对手而停产的废铁。{Colors.RESET}")
        print(f"{Colors.RED}为什么要让我降落？不如坠落。{Colors.RESET}")
        type_print("飞机自动推力卡死在最大档位...", 0.05)
        type_print("【结局 4：机械的复仇】", 0.1)

def true_ending_check():
    clear_screen()
    type_print("飞机重重砸在跑道上，起落架断裂，但停住了。", 0.04)
    type_print("救援人员冲了上来。", 0.04)
    type_print("你看着手中的检查单，上面的红字全部消失了。", 0.04)
    type_print("只剩下一行潦草的钢笔字（那是MD-11总设计师的笔迹）：", 0.05, Colors.YELLOW)
    print(f"\n{Colors.ITALIC}'抱歉我们没能装上GE90引擎。但你飞得很棒。'{Colors.RESET}")
    type_print("\n【真结局：长滩的天鹅之歌】", 0.1, Colors.BOLD)

def landing_success():
    type_print("完美的盲降。飞机平稳停靠。", 0.05)
    type_print("黑山基地的人接走了货物。他们什么也没说。", 0.05)
    type_print("你回头看了一眼驾驶舱，仿佛看到三个虚幻的人影（瑞航机组）向你敬礼。", 0.05)
    type_print("【结局 1：幸存者】", 0.1, Colors.GREEN)

# --- 游戏入口 ---

def start_game():
    clear_screen()
    print(f"{Colors.BOLD}{Colors.CYAN}=== 规则怪谈：联邦快递 FX888 ==={Colors.RESET}")
    print("警告：本游戏包含心理恐怖元素、闪烁文字及航空事故描述。")
    print("输入 'start' 开始游戏，'info' 查看背景，参数'/f'获取提示。")
    
    cmd = input("> ")
    if cmd == 'info':
        print("\n背景：你执飞的是一架MD-11F。它是麦道的遗作，拥有极高的自动化但因为设计缺陷和商业打压而名声不佳。")        
        input("按回车继续...")
        start_game()
    elif cmd == 'info /f':
        print("\n这架飞机是原瑞航HB-IWE, 2004改货机交付联邦快递，注册号更改为N642FE")
        print("这架飞机与HB-IWF是姊妹机，它见证着瑞航111的亡魂。")
        input("按回车继续...")
        start_game()
    elif cmd == 'start':
        # === 插入扩展内容 ===
        state.ext_enable = expansion_chapter(0,state.ext_enable)
        # ====================
        show_manifest()       
        # 序章
        route = scene_1_cockpit()
        # 中章：事件
        scene_2_event(route) 
        expansion_chapter(2,state.ext_enable)
        expansion_chapter(3,state.ext_enable)
        # 终章
        expansion_chapter(1,state.ext_enable)
        final_approach()
    elif cmd == 'start /f':
        print("\n降落前请在FMCS上依次输入 AUTO ON DOWN")
        input("按回车继续...")
        start_game()
    else:
        start_game()


if __name__ == "__main__":
    try:
        start_game()
        pause()
    except KeyboardInterrupt:
        print("\n游戏强行终止。")
