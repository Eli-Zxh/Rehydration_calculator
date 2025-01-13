from flask import Flask, request, jsonify

app = Flask(__name__)

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

        return {
            "stage": stage,
            "total_water": total_water,
            "NaHCO3": NaHCO3,
            "NaCl": NaCl,
            "glucose": glucose,
            "tstage_water": tstage_water
        }

    except ValueError as e:
        return {"error": str(e)}

@app.route('/calculate', methods=['POST'])
def api_calculate():
    data = request.json
    result = calculate(
        data.get('current_weight'),
        data.get('weight_loss'),
        data.get('phase'),
        data.get('osmolality'),
        data.get('concentration')
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)