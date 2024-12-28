import tkinter as tk
from tkinter import messagebox

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
            elif concentration == "1/2张":
                NaCl = tstage_water / 3
                glucose = 2 * tstage_water / 3
                NaHCO3 = 0
            elif concentration == "1/3张":
                NaCl = tstage_water / 3
                glucose = 31 * tstage_water / 50
                NaHCO3 = 7 * tstage_water / 50
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
                ("轻度", "快速补液阶段", "高渗", None): "1/3张补液",
                ("中度", "快速补液阶段", "低渗", None): "4:3:2含钠液",
                ("中度", "快速补液阶段", "等渗", None): "2:3:1含钠液",
                ("中度", "快速补液阶段", "高渗", None): "1/3张补液",
                ("重度", "快速补液阶段", "低渗", None): "4:3:2含钠液",
                ("重度", "快速补液阶段", "等渗", None): "2:3:1含钠液",
                ("重度", "快速补液阶段", "高渗", None): "1/3张补液",
                ("轻度", "扩容阶段", None, None): "2:1等张液",
                ("中度", "扩容阶段", None, None): "2:1等张液",
                ("重度", "扩容阶段", None, None): "2:1等张液",
                ("轻度", "继续补液阶段", None, "1/2张"): "1/2张补液",
                ("轻度", "继续补液阶段", None, "1/3张"): "1/3张补液",
                ("中度", "继续补液阶段", None, "1/2张"): "1/2张补液",
                ("中度", "继续补液阶段", None, "1/3张"): "1/3张补液",
                ("重度", "继续补液阶段", None, "1/2张"): "1/2张补液",
                ("重度", "继续补液阶段", None, "1/3张"): "1/3张补液",
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
            # 检查是否满足特殊条件
            special_conditions = {
                ("轻度", "扩容阶段"): f"注意：轻度脱水无需扩容，可以考虑使用{weight}ml的口服补液盐，如果考虑静脉补液，考虑上表。",
                ("中度", "扩容阶段"): f"注意：中度脱水无需扩容，可以考虑使用{weight}ml的口服补液盐，如果考虑静脉补液，考虑上表。",
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

    # 创建主窗口
    root = tk.Tk()
    root.title("补液计算器")

    # 输入框和标签
    tk.Label(root, text="现在的体重 (kg):").grid(row=0, column=0, padx=10, pady=10)
    entry_current_weight = tk.Entry(root)
    entry_current_weight.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="减轻的体重 (kg):").grid(row=1, column=0, padx=10, pady=10)
    entry_weight_loss = tk.Entry(root)
    entry_weight_loss.grid(row=1, column=1, padx=10, pady=10)

    # 单选按钮选择阶段
    var = tk.StringVar(value="快速补液阶段")
    tk.Radiobutton(root, text="快速补液阶段", variable=var, value="快速补液阶段").grid(row=2, column=0, padx=10, pady=5)
    tk.Radiobutton(root, text="扩容阶段", variable=var, value="扩容阶段").grid(row=2, column=1, padx=10, pady=5)
    tk.Radiobutton(root, text="继续补液阶段", variable=var, value="继续补液阶段").grid(row=3, column=0, padx=10, pady=5)

    # 单选按钮选择渗透压（仅在快速补液阶段显示）
    var_osmolality = tk.StringVar(value="等渗")
    osmolality_frame = tk.Frame(root)
    osmolality_frame.grid(row=4, column=0, columnspan=2, pady=5)

    tk.Radiobutton(osmolality_frame, text="低渗", variable=var_osmolality, value="低渗").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(osmolality_frame, text="等渗", variable=var_osmolality, value="等渗").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(osmolality_frame, text="高渗", variable=var_osmolality, value="高渗").pack(side=tk.LEFT, padx=5)

    # 单选按钮选择浓度（仅在继续补液阶段显示）
    var_concentration = tk.StringVar(value="1/2张")
    concentration_frame = tk.Frame(root)
    concentration_frame.grid(row=4, column=0, columnspan=2, pady=5)

    tk.Radiobutton(concentration_frame, text="1/2张", variable=var_concentration, value="1/2张").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(concentration_frame, text="1/3张", variable=var_concentration, value="1/3张").pack(side=tk.LEFT, padx=5)

    # 计算按钮
    calculate_button = tk.Button(root, text="计算", command=on_calculate)
    calculate_button.grid(row=5, column=0, columnspan=2, pady=20)

    # 描述信息文本框
    tk.Label(root, text="描述信息:").grid(row=6, column=0, padx=10, pady=10)
    text_description = tk.Text(root, height=5, width=50)
    text_description.grid(row=6, column=1, padx=10, pady=10)

    # 结果标签和输入框
    label_NaHCO3 = tk.Label(root, text="所需5%NaHCO3溶液:")
    label_NaHCO3.grid(row=7, column=0, padx=10, pady=10)
    entry_NaHCO3 = tk.Entry(root)
    entry_NaHCO3.grid(row=7, column=1, padx=10, pady=10)
    entry_NaHCO3.grid_remove()

    label_NaCl = tk.Label(root, text="所需0.9%NaCl溶液:")
    label_NaCl.grid(row=8, column=0, padx=10, pady=10)
    entry_NaCl = tk.Entry(root)
    entry_NaCl.grid(row=8, column=1, padx=10, pady=10)
    entry_NaCl.grid_remove()

    label_glucose = tk.Label(root, text="所需5%葡萄糖:")
    label_glucose.grid(row=9, column=0, padx=10, pady=10)
    entry_glucose = tk.Entry(root)
    entry_glucose.grid(row=9, column=1, padx=10, pady=10)
    entry_glucose.grid_remove()

    # 注意事项文本框
    tk.Label(root, text="注意事项:").grid(row=10, column=0, padx=10, pady=10)
    text_special_note = tk.Text(root, height=3, width=50)
    text_special_note.grid(row=10, column=1, padx=10, pady=10)
    text_special_note.grid_remove()

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
    root.mainloop()

if __name__ == "__main__":
    create_gui()