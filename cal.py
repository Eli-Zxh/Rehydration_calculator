import tkinter as tk
from tkinter import messagebox, ttk

def calculate_quick_ratio(total_volume, fluid_type, m_NaCl=0.9, m_NaHCO3=5, m_glucose=5):
    # 保留计算逻辑的函数，补充具体的计算逻辑
    NaHCO3 = 0
    NaCl = 0
    glucose = 0

    if fluid_type == "1:1含钠液":
        NaHCO3 = 0
        NaCl = 9 * total_volume / (20 * m_NaCl) 
    elif fluid_type == "1:2含钠液":
        NaHCO3 = 0
        NaCl = 0.3 * total_volume / m_NaCl
    elif fluid_type == "1:4含钠液":
        NaHCO3 = 0
        NaCl = 9 * total_volume / (50 * m_NaCl)
    elif fluid_type == "2:1等张含钠液":
        NaHCO3 = 7 * total_volume / (15 * m_NaHCO3)
        NaCl = 3 * total_volume / (5 * m_NaCl)
    elif fluid_type == "2:3:1含钠液":
        NaHCO3 = 7 * total_volume / (30 * m_NaHCO3)
        NaCl = 3 * total_volume / (10 * m_NaCl)
    elif fluid_type == "4:3:2含钠液":
        NaHCO3 = 14 * total_volume / (45 * m_NaHCO3)
        NaCl = 2 * total_volume / (5 * m_NaCl)

    glucose = total_volume - NaCl - NaHCO3

    return round(NaHCO3), round(NaCl), round(glucose)

def calculate(current_weight, weight_loss, phase, osmolality=None, concentration=None):
    try:
        current_weight = float(current_weight)
        weight_loss = float(weight_loss)
        percent_loss = weight_loss / (current_weight + weight_loss)
        
        if percent_loss < 0.05 and percent_loss > 0:
            stage = "轻度"
            total_water = 120 * (current_weight + weight_loss)
        elif percent_loss < 0.1 and percent_loss >= 0.05:
            stage = "中度"
            total_water = 150 * (current_weight + weight_loss)
        elif percent_loss < 1 and percent_loss >= 0.1:
            stage = "重度"
            total_water = 180 * (weight_loss + current_weight)
        else:
            raise ValueError("请输入正确的体重和体重减少量")

        if phase == "快速补液阶段":
            tstage_water = total_water / 2 - 20 * (weight_loss + current_weight)
            if osmolality is None:
                raise ValueError("在快速补液阶段必须选择渗透压")
            # 根据选择的渗透压计算逻辑
            elif osmolality == "低渗":
                NaCl = 4 * tstage_water / 9
                glucose = 111 * tstage_water / 225
                NaHCO3 = 14 * tstage_water / 225
            elif osmolality == "等渗":
                NaCl = tstage_water / 3
                glucose = 93 * tstage_water / 150
                NaHCO3 = 7 * tstage_water / 150
            elif osmolality == "高渗":
                NaCl = tstage_water / 3
                glucose = 2 * tstage_water / 3
                NaHCO3 = 0
        elif phase == "扩容阶段":
            tstage_water = (weight_loss + current_weight)*20
            # 扩容阶段的计算逻辑
            NaHCO3 = 28 * (weight_loss + current_weight) / 15
            NaCl = 40 * (weight_loss + current_weight) / 3
            glucose = 72 * (weight_loss + current_weight) / 15
        elif phase == "继续补液阶段":
            # 继续补液阶段的计算逻辑
            tstage_water = total_water / 2
            if concentration is None:
                raise ValueError("在继续补液阶段请输入1/2张或者1/3张")
            elif concentration == "1/3张":
                NaCl = tstage_water / 3
                glucose = 2 * tstage_water / 3
                NaHCO3 = 0
            elif concentration == "1/2张":
                NaCl = tstage_water / 3
                glucose = 31 * tstage_water / 50
                NaHCO3 = 7 * tstage_water / 150
        else:
            raise ValueError("请选择一个阶段")

        # 将结果转换为整数
        NaHCO3 = round(NaHCO3)
        NaCl = round(NaCl)
        glucose = round(glucose)

        return stage, total_water, NaHCO3, NaCl, glucose, tstage_water

    except ValueError as e:
        messagebox.showerror("错误", str(e))
        return None, None, None, None, None

def calculate_num(total_water):
    # 计算num的逻辑
    if total_water <= 200:
        return 200, 1, 0, None
    elif total_water > 200 and total_water <= 500:
        return 500, 1, 0, None
    elif total_water > 500:
        n = total_water // 500
        left = total_water - n * 500
        if left <= 200:
            num_left = 200
        elif left > 200 and left <= 500:
            num_left = 500
        else:
            return 500, n, left
        return 500, n, left, num_left

def create_gui():
    def on_calculate():
        current_weight = entry_current_weight.get()
        weight_loss = entry_weight_loss.get()
        phase = var.get()
        osmolality = var_osmolality.get() if var.get() == "快速补液阶段" else None
        concentration = var_concentration.get() if var.get() == "继续补液阶段" else None

        stage, total_water, NaHCO3, NaCl, glucose, tstage_water = calculate(current_weight, weight_loss, phase, osmolality, concentration)
        if NaHCO3 is not None:
            # 计算num
            num, n, left, num_left = calculate_num(tstage_water)

            # 根据stage, phase, concentration和osmolality确定style
            style_dict = {
                ("轻度", "快速补液阶段", "低渗", None): "4:3:2含钠液",
                ("轻度", "快速补液阶段", "等渗", None): "2:3:1含钠液",
                ("轻度", "快速补液阶段", "高渗", None): "1:2含钠液",
                ("中度", "快速补液阶段", "低渗", None): "4:3:2含钠液",
                ("中度", "快速补液阶段", "等渗", None): "2:3:1含钠液",
                ("中度", "快速补液阶段", "高渗", None): "1:2含钠液",
                ("重度", "快速补液阶段", "低渗", None): "4:3:2含钠液",
                ("重度", "快速补液阶段", "等渗", None): "2:3:1含钠液",
                ("重度", "快速补液阶段", "高渗", None): "1:2含钠液",
                ("轻度", "扩容阶段", None, None): "2:1等张含钠液",
                ("中度", "扩容阶段", None, None): "2:1等张含钠液",
                ("重度", "扩容阶段", None, None): "2:1等张含钠液",
                ("轻度", "继续补液阶段", None, "1/2张"): "2:3:1含钠液",
                ("轻度", "继续补液阶段", None, "1/3张"): "1:2含钠液",
                ("中度", "继续补液阶段", None, "1/2张"): "2:3:1含钠液",
                ("中度", "继续补液阶段", None, "1/3张"): "1:2含钠液",
                ("重度", "继续补液阶段", None, "1/2张"): "2:3:1含钠液",
                ("重度", "继续补液阶段", None, "1/3张"): "1:2含钠液",
            }
            style_key = (stage, phase, osmolality, concentration)
            style = style_dict.get(style_key, "未知补液")

            # 更新描述信息
            description = f"该患者目前处于{stage}脱水状态，可以考虑补充总共{total_water:.0f} mL的{style} 液体，当前阶段共计补充{tstage_water:.0f}mL的液体，考虑使用{n}个{num} mL的补液袋,其对应的剂量如下表配置："
            text_description.delete(1.0, tk.END)
            text_description.insert(tk.END, description)

            # 显示输出框
            entry_NaHCO3.grid()
            entry_NaCl.grid()
            entry_glucose.grid()
            label_NaHCO3.grid()
            label_NaCl.grid()
            label_glucose.grid()

            if left > 0:
                NaHCO3_500 = round(NaHCO3 * 500 / tstage_water)
                NaCl_500 = round(NaCl * 500 / tstage_water)
                glucose_500 = round(glucose * 500 / tstage_water)
                NaHCO3_left = round(NaHCO3 * left / tstage_water)
                NaCl_left = round(NaCl * left / tstage_water)
                glucose_left = round(glucose * left / tstage_water)

                entry_NaHCO3.delete(0, tk.END)
                entry_NaHCO3.insert(0, f"{NaHCO3_500} ml              {NaHCO3_left} ml")
                entry_NaCl.delete(0, tk.END)
                entry_NaCl.insert(0, f"{NaCl_500} ml              {NaCl_left} ml")
                entry_glucose.delete(0, tk.END)
                entry_glucose.insert(0, f"{glucose_500} ml              {glucose_left} ml")
            else:
                entry_NaHCO3.delete(0, tk.END)
                entry_NaHCO3.insert(0, f"{NaHCO3} ml")
                entry_NaCl.delete(0, tk.END)
                entry_NaCl.insert(0, f"{NaCl} ml")
                entry_glucose.delete(0, tk.END)
                entry_glucose.insert(0, f"{glucose} ml")
            
            weight = (current_weight + weight_loss)*50
            weight2 = weight*2
            # 检查是否满足特殊条件
            special_conditions = {
                ("轻度", "扩容阶段"): f"注意：轻度脱水无需扩容，可以考虑使用{weight}ml的口服补液盐，如果考虑静脉补液，考虑上表。",
                ("中度", "扩容阶段"): f"注意：中度脱水无需扩容，可以考虑使用{weight2}ml的口服补液盐，如果考虑静脉补液，考虑上表。",
            }
            special_key = (stage, phase)
            special_note = special_conditions.get(special_key, "")
            if special_note:
                text_special_note.delete(1.0, tk.END)
                text_special_note.insert(tk.END, special_note)
                text_special_note.grid()
            elif left:
                special_note = f"注意：左侧为{n}个500ml补液袋需要配满的配比，右侧为使用{num_left}ml的补液袋中剩余液体的配比"
                text_special_note.delete(1.0, tk.END)
                text_special_note.insert(tk.END, special_note)
                text_special_note.grid()
            else:
                text_special_note.grid_remove()
    
    # 修改 on_calculate_quick_ratio 函数以处理自定义浓度
    def on_calculate_quick_ratio():
        try:
            total_volume = float(entry_total_volume.get())
            fluid_type = var_fluid_type.get()
            m_NaCl = 0.9
            m_NaHCO3 = 5
            m_glucose = 5

            if var_concentration_mode.get() == "自定义浓度":
                m_NaCl = float(entry_custom_NaCl.get()) 
                m_NaHCO3 = float(entry_custom_NaHCO3.get()) 
                m_glucose = float(entry_custom_glucose.get()) 

            NaHCO3, NaCl, glucose = calculate_quick_ratio(total_volume, fluid_type, m_NaCl, m_NaHCO3, m_glucose)
    
            entry_quick_NaHCO3.delete(0, tk.END)
            entry_quick_NaHCO3.insert(0, f"{NaHCO3} ml")
            entry_quick_NaCl.delete(0, tk.END)
            entry_quick_NaCl.insert(0, f"{NaCl} ml")
            entry_quick_glucose.delete(0, tk.END)
            entry_quick_glucose.insert(0, f"{glucose} ml")

        except ValueError as e:
            messagebox.showerror("错误", str(e))

    # 创建主窗口
    root = tk.Tk()
    root.title("补液计算器")

    # 创建选项卡
    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill="both")

    # 创建第一个选项卡（保留现有内容）
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="补液方案计算")

    # 输入框和标签
    tk.Label(tab1, text="现在的体重 (kg):").grid(row=0, column=0, padx=10, pady=10)
    entry_current_weight = tk.Entry(tab1)
    entry_current_weight.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(tab1, text="减轻的体重 (kg):").grid(row=1, column=0, padx=10, pady=10)
    entry_weight_loss = tk.Entry(tab1)
    entry_weight_loss.grid(row=1, column=1, padx=10, pady=10)

    # 单选按钮选择阶段
    var = tk.StringVar(value="快速补液阶段")
    tk.Radiobutton(tab1, text="快速补液阶段", variable=var, value="快速补液阶段").grid(row=2, column=0, padx=10, pady=5)
    tk.Radiobutton(tab1, text="扩容阶段", variable=var, value="扩容阶段").grid(row=2, column=1, padx=10, pady=5)
    tk.Radiobutton(tab1, text="继续补液阶段", variable=var, value="继续补液阶段").grid(row=3, column=0, padx=10, pady=5)

    # 单选按钮选择渗透压（仅在快速补液阶段显示）
    var_osmolality = tk.StringVar(value="等渗")
    osmolality_frame = tk.Frame(tab1)
    osmolality_frame.grid(row=4, column=0, columnspan=2, pady=5)

    tk.Radiobutton(osmolality_frame, text="低渗", variable=var_osmolality, value="低渗").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(osmolality_frame, text="等渗", variable=var_osmolality, value="等渗").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(osmolality_frame, text="高渗", variable=var_osmolality, value="高渗").pack(side=tk.LEFT, padx=5)

    # 单选按钮选择浓度（仅在继续补液阶段显示）
    var_concentration = tk.StringVar(value="1/2张")
    concentration_frame = tk.Frame(tab1)
    concentration_frame.grid(row=4, column=0, columnspan=2, pady=5)

    tk.Radiobutton(concentration_frame, text="1/2张", variable=var_concentration, value="1/2张").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(concentration_frame, text="1/3张", variable=var_concentration, value="1/3张").pack(side=tk.LEFT, padx=5)

    # 计算按钮
    calculate_button = tk.Button(tab1, text="计算", command=on_calculate)
    calculate_button.grid(row=5, column=0, columnspan=2, pady=20)

    # 描述信息文本框
    tk.Label(tab1, text="描述信息:").grid(row=6, column=0, padx=10, pady=10)
    text_description = tk.Text(tab1, height=5, width=50)
    text_description.grid(row=6, column=1, padx=10, pady=10)

    # 结果标签和输入框
    label_NaHCO3 = tk.Label(tab1, text="所需5%NaHCO3溶液:")
    label_NaHCO3.grid(row=7, column=0, padx=10, pady=10)
    entry_NaHCO3 = tk.Entry(tab1)
    entry_NaHCO3.grid(row=7, column=1, padx=10, pady=10)
    entry_NaHCO3.grid_remove()  # 默认隐藏
    label_NaHCO3.grid_remove()  # 默认隐藏
    
    label_NaCl = tk.Label(tab1, text="所需0.9%NaCl溶液:")
    label_NaCl.grid(row=8, column=0, padx=10, pady=10)
    entry_NaCl = tk.Entry(tab1)
    entry_NaCl.grid(row=8, column=1, padx=10, pady=10)
    entry_NaCl.grid_remove()  # 默认隐藏
    label_NaCl.grid_remove()  # 默认隐藏

    label_glucose = tk.Label(tab1, text="所需5%葡萄糖:")
    label_glucose.grid(row=9, column=0, padx=10, pady=10)
    entry_glucose = tk.Entry(tab1)
    entry_glucose.grid(row=9, column=1, padx=10, pady=10)
    entry_glucose.grid_remove()  # 默认隐藏
    label_glucose.grid_remove()  # 默认隐藏

    # 注意事项文本框
    tk.Label(tab1, text="注意事项:").grid(row=10, column=0, padx=10, pady=10)
    text_special_note = tk.Text(tab1, height=3, width=50)
    text_special_note.grid(row=10, column=1, padx=10, pady=10)
    text_special_note.grid_remove()  # 默认隐藏

    # 显示或隐藏渗透压选择框
    def update_osmolality_options(*args):
        if var.get() == "快速补液阶段":
            osmolality_frame.grid()
            concentration_frame.grid_remove()
        elif var.get() == "继续补液阶段":
            concentration_frame.grid()
            osmolality_frame.grid_remove()
        else:
            osmolality_frame.grid_remove()
            concentration_frame.grid_remove()

    var.trace("w", update_osmolality_options)
    # 自动选择“快速补液阶段”
    var.set("快速补液阶段")
    update_osmolality_options()  # 确保选项框正确显示
    # 运行主循环

    # 创建第二个选项卡
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="快速配比")
    
    # 添加抬头提示信息
    tk.Label(tab2, text="按照0.9%NaCl、5%NaHCO3、5%葡萄糖的默认浓度").grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # 选择默认浓度或自定义浓度
    var_concentration_mode = tk.StringVar(value="默认浓度")
    tk.Radiobutton(tab2, text="默认浓度", variable=var_concentration_mode, value="默认浓度").grid(row=1, column=0, padx=10, pady=5)
    tk.Radiobutton(tab2, text="自定义浓度", variable=var_concentration_mode, value="自定义浓度").grid(row=1, column=1, padx=10, pady=5)

    # 输入框和标签
    tk.Label(tab2, text="总补液量 (ml):").grid(row=2, column=0, padx=10, pady=10)
    entry_total_volume = tk.Entry(tab2)
    entry_total_volume.grid(row=2, column=1, padx=10, pady=10)

    # 单选按钮选择液体类型
    var_fluid_type = tk.StringVar(value="4:3:2含钠液")
    tk.Radiobutton(tab2, text="4:3:2含钠液", variable=var_fluid_type, value="4:3:2含钠液").grid(row=3, column=0, padx=10, pady=5)
    tk.Radiobutton(tab2, text="2:3:1含钠液", variable=var_fluid_type, value="2:3:1含钠液").grid(row=3, column=1, padx=10, pady=5)
    tk.Radiobutton(tab2, text="1:2含钠液", variable=var_fluid_type, value="1:2含钠液").grid(row=4, column=0, padx=10, pady=5)
    tk.Radiobutton(tab2, text="1:1含钠液", variable=var_fluid_type, value="1:1含钠液").grid(row=4, column=1, padx=10, pady=5)
    tk.Radiobutton(tab2, text="2:1等张含钠液", variable=var_fluid_type, value="2:1等张含钠液").grid(row=5, column=0, padx=10, pady=5)
    tk.Radiobutton(tab2, text="1:4含钠液", variable=var_fluid_type, value="1:4含钠液").grid(row=5, column=1, padx=10, pady=5)

    # 自定义浓度输入框及其标签
    label_custom_NaCl = tk.Label(tab2, text="NaCl质量浓度:")
    label_custom_NaCl.grid(row=6, column=0, padx=10, pady=10)
    entry_custom_NaCl = tk.Entry(tab2)
    entry_custom_NaCl.grid(row=6, column=1, padx=10, pady=10)
    label_percent_NaCl = tk.Label(tab2, text="%")
    label_percent_NaCl.grid(row=6, column=2, padx=0, pady=10)
    entry_custom_NaCl.grid_remove()  # 默认隐藏
    label_custom_NaCl.grid_remove()  # 默认隐藏
    label_percent_NaCl.grid_remove()  # 默认隐藏
    
    label_custom_NaHCO3 = tk.Label(tab2, text="NaHCO3质量浓度:")
    label_custom_NaHCO3.grid(row=7, column=0, padx=10, pady=10)
    entry_custom_NaHCO3 = tk.Entry(tab2)
    entry_custom_NaHCO3.grid(row=7, column=1, padx=10, pady=10)
    label_percent_NaHCO3 = tk.Label(tab2, text="%")
    label_percent_NaHCO3.grid(row=7, column=2, padx=0, pady=10)
    entry_custom_NaHCO3.grid_remove()  # 默认隐藏
    label_custom_NaHCO3.grid_remove()  # 默认隐藏
    label_percent_NaHCO3.grid_remove()  # 默认隐藏

    label_custom_glucose = tk.Label(tab2, text="葡萄糖质量浓度:")
    label_custom_glucose.grid(row=8, column=0, padx=10, pady=10)
    entry_custom_glucose = tk.Entry(tab2)
    entry_custom_glucose.grid(row=8, column=1, padx=10, pady=10)
    label_percent_glucose = tk.Label(tab2, text="%")
    label_percent_glucose.grid(row=8, column=2, padx=0, pady=10)
    entry_custom_glucose.grid_remove()  # 默认隐藏
    label_custom_glucose.grid_remove()  # 默认隐藏
    label_percent_glucose.grid_remove()  # 默认隐藏
    
    # 计算按钮
    calculate_quick_button = tk.Button(tab2, text="计算", command=on_calculate_quick_ratio)
    calculate_quick_button.grid(row=9, column=0, columnspan=2, pady=20)
    
    # 结果标签和输入框
    label_quick_NaHCO3 = tk.Label(tab2, text="所需NaHCO3溶液:")
    label_quick_NaHCO3.grid(row=10, column=0, padx=10, pady=10)
    entry_quick_NaHCO3 = tk.Entry(tab2)
    entry_quick_NaHCO3.grid(row=10, column=1, padx=10, pady=10)

    label_quick_NaCl = tk.Label(tab2, text="所需NaCl溶液:")
    label_quick_NaCl.grid(row=11, column=0, padx=10, pady=10)
    entry_quick_NaCl = tk.Entry(tab2)
    entry_quick_NaCl.grid(row=11, column=1, padx=10, pady=10)
    
    label_quick_glucose = tk.Label(tab2, text="所需葡萄糖:")
    label_quick_glucose.grid(row=12, column=0, padx=10, pady=10)
    entry_quick_glucose = tk.Entry(tab2)
    entry_quick_glucose.grid(row=12, column=1, padx=10, pady=10)

    # 显示或隐藏自定义浓度输入框及其标签
    def update_concentration_mode(*args):
        if var_concentration_mode.get() == "自定义浓度":
            entry_custom_NaCl.grid()
            entry_custom_NaHCO3.grid()
            entry_custom_glucose.grid()
            label_custom_NaCl.grid()
            label_custom_NaHCO3.grid()
            label_custom_glucose.grid()
            label_percent_NaCl.grid()
            label_percent_NaHCO3.grid()
            label_percent_glucose.grid()
        else:
            entry_custom_NaCl.grid_remove()
            entry_custom_NaHCO3.grid_remove()
            entry_custom_glucose.grid_remove()
            label_custom_NaCl.grid_remove()
            label_custom_NaHCO3.grid_remove()
            label_custom_glucose.grid_remove()
            label_percent_NaCl.grid_remove()
            label_percent_NaHCO3.grid_remove()
            label_percent_glucose.grid_remove()

    var_concentration_mode.trace("w", update_concentration_mode)
    root.mainloop()

if __name__ == "__main__":
    create_gui()