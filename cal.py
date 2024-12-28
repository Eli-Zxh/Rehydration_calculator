import tkinter as tk
from tkinter import messagebox

def calculate(current_weight, weight_loss, phase, osmolality=None):
    try:
        current_weight = float(current_weight)
        weight_loss = float(weight_loss)
        percent_loss = weight_loss/(current_weight+weight_loss)
        if percent_loss < 0.05 & percent_loss > 0:
            stage = "轻度"
            total_water = 50*(current_weight + weight_loss)
        elif percent_loss < 0.1 & percent_loss >= 0.05:
            stage = "中度"
            total_water = 100*(current_weight + weight_loss)
        elif percent_loss < 1 & percent_loss >= 0.1:
            stage = "重度"
            total_water = 180(weight_loss + current_weight)
        else:
            raise ValueError("请输入正确的体重和体重减少量")

        if phase == "快速补液阶段":
            t1stage_water = total_water/2-20(weight_loss+current_weight)
            if osmolality is None:
                raise ValueError("在快速补液阶段必须选择渗透压")
            # 根据选择的渗透压计算逻辑
            elif osmolality == "低渗":
                NaCl=4*t1stage_water/9
                glucose=111*t1stage_water/225
                NaHCO3=14*t1stage_water/225
            elif osmolality == "等渗":
                NaCl=t1stage_water/3
                glucose=93*t1stage_water/150
                NaHCO3=7*t1stage_water/150
            elif osmolality == "高渗":
                NaCl=t1stage_water/3
                glucose=2*t1stage_water/3
                NaHCO3 = 0
        elif phase == "扩容阶段":
            # 扩容阶段的计算逻辑
            NaHCO3 = 28(weight_loss+current_weight)/15
            NaCl = 40(weight_loss+current_weight)/3
            glucose = 72(weight_loss+current_weight)/15
        elif phase == "继续补液阶段":
            # 继续补液阶段的计算逻辑
            t2stage_water = total_water/2
            if osmolality is None:
                raise ValueError("在继续补液阶段请输入1/2张或者1/3张")
            elif osmolality == "1/2张":
                NaCl=t2stage_water/3
                glucose = 2*t2stage_water/3
                NaHCO3 = 0
            elif osmolality == "1/3张":
                NaCl=t2stage_water/3
                glucose = 31*t2stage_water/50
                NaHCO3 = 7*t2stage_water/50
        else:
            raise ValueError("请选择一个阶段")

        return stage, NaHCO3, NaCl, glucose

    except ValueError as e:
        messagebox.showerror("错误", str(e))
        return None, None, None

def create_gui():
    def on_calculate():
        current_weight = entry_current_weight.get()
        weight_loss = entry_weight_loss.get()
        phase = var.get()
        osmolality = var_osmolality.get() if var.get() == "快速补液阶段" else None

        NaHCO3, NaCl, glucose = calculate(current_weight, weight_loss, phase, osmolality)
        if NaHCO3 is not None:
            result_text = f"NaHCO3: {NaHCO3:.2f} g\nNaCl: {NaCl:.2f} g\n葡萄糖: {glucose:.2f} g"
            result_label.config(text=result_text)

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

    # 计算按钮
    calculate_button = tk.Button(root, text="计算", command=on_calculate)
    calculate_button.grid(row=5, column=0, columnspan=2, pady=20)

    # 结果标签
    result_label = tk.Label(root, text="", justify=tk.LEFT)
    result_label.grid(row=6, column=0, columnspan=2)

    # 显示或隐藏渗透压选择框
    def update_osmolality_options(*args):
        if var.get() == "快速补液阶段":
            osmolality_frame.grid()
        else:
            osmolality_frame.grid_remove()

    var.trace("w", update_osmolality_options)

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    create_gui()