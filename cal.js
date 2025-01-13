function openTab(evt, tabName) {
    const tabContent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabContent.length; i++) {
        tabContent[i].classList.remove("active");
    }
    const tabButtons = document.getElementsByClassName("tab-button");
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove("active");
    }
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

document.addEventListener('DOMContentLoaded', function() {
    const phaseRadios = document.querySelectorAll('input[name="phase"]');
    phaseRadios.forEach(radio => {
        radio.addEventListener('change', updateOsmolalityOptions);
    });
    updateOsmolalityOptions();
});

function updateOsmolalityOptions() {
    const phase = document.querySelector('input[name="phase"]:checked').value;
    const osmolalityGroup = document.getElementById('osmolality-group');
    const concentrationGroup = document.getElementById('concentration-group');
    if (phase === "快速补液阶段") {
        osmolalityGroup.style.display = 'block';
        concentrationGroup.style.display = 'none';
    } else if (phase === "继续补液阶段") {
        concentrationGroup.style.display = 'block';
        osmolalityGroup.style.display = 'none';
    } else {
        osmolalityGroup.style.display = 'none';
        concentrationGroup.style.display = 'none';
    }
}

function onCalculate() {
    const currentWeight = parseFloat(document.getElementById('current-weight').value);
    const weightLoss = parseFloat(document.getElementById('weight-loss').value);
    const phase = document.querySelector('input[name="phase"]:checked').value;
    const osmolality = document.querySelector('input[name="osmolality"]:checked') ? document.querySelector('input[name="osmolality"]:checked').value : null;
    const concentration = document.querySelector('input[name="concentration"]:checked') ? document.querySelector('input[name="concentration"]:checked').value : null;

    const result = calculate(currentWeight, weightLoss, phase, osmolality, concentration);
    if (result) {
        document.getElementById('description').value = `阶段: ${result.stage}\n总水量: ${result.totalWater} ml\n所需5%NaHCO3溶液: ${result.NaHCO3} ml\n所需0.9%NaCl溶液: ${result.NaCl} ml\n所需5%葡萄糖: ${result.glucose} ml`;
        document.getElementById('NaHCO3').value = result.NaHCO3;
        document.getElementById('NaCl').value = result.NaCl;
        document.getElementById('glucose').value = result.glucose;
        document.getElementById('result-group').style.display = 'block';
        document.getElementById('special-note').style.display = 'block';
        document.getElementById('special-note-text').value = "注意事项: 根据实际情况调整补液方案。";
    } else {
        alert("请输入正确的体重和体重减少量");
    }
}

function onCalculateQuickRatio() {
    const totalVolume = parseFloat(document.getElementById('total-volume').value);
    const fluidType = document.querySelector('input[name="fluid-type"]:checked').value;
    const customNaCl = document.getElementById('custom-NaCl').value ? parseFloat(document.getElementById('custom-NaCl').value) : 0.9;
    const customNaHCO3 = document.getElementById('custom-NaHCO3').value ? parseFloat(document.getElementById('custom-NaHCO3').value) : 5;
    const customGlucose = document.getElementById('custom-Glucose').value ? parseFloat(document.getElementById('custom-Glucose').value) : 5;

    const result = calculateQuickRatio(totalVolume, fluidType, customNaCl, customNaHCO3, customGlucose);
    if (result) {
        document.getElementById('quick-NaHCO3').value = result[0];
        document.getElementById('quick-NaCl').value = result[1];
        document.getElementById('quick-Glucose').value = result[2];
    } else {
        alert("请输入正确的总补液量");
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const concentrationModeRadios = document.querySelectorAll('input[name="concentration-mode"]');
    concentrationModeRadios.forEach(radio => {
        radio.addEventListener('change', updateCustomConcentrationOptions);
    });
    updateCustomConcentrationOptions();
});

function updateCustomConcentrationOptions() {
    const concentrationMode = document.querySelector('input[name="concentration-mode"]:checked').value;
    const customConcentrationGroup = document.getElementById('custom-concentration-group');
    if (concentrationMode === "自定义浓度") {
        customConcentrationGroup.style.display = 'block';
    } else {
        customConcentrationGroup.style.display = 'none';
    }
}

function calculateNum(totalWater) {
    // 计算num的逻辑
    if (totalWater <= 200) {
        return [200, 1, 0, null];
    } else if (totalWater > 200 && totalWater <= 500) {
        return [500, 1, 0, null];
    } else if (totalWater > 500) {
        const n = Math.floor(totalWater / 500);
        const left = totalWater - n * 500;
        let numLeft;
        if (left <= 200) {
            numLeft = 200;
        } else if (left > 200 && left <= 500) {
            numLeft = 500;
        } else {
            return [500, n, left];
        }
        return [500, n, left, numLeft];
    }
}

function calculate(currentWeight, weightLoss, phase, osmolality = null, concentration = null) {
    try {
        currentWeight = parseFloat(currentWeight);
        weightLoss = parseFloat(weightLoss);
        const percentLoss = weightLoss / (currentWeight + weightLoss);

        let stage, totalWater, tstageWater, NaHCO3, NaCl, glucose;

        if (percentLoss < 0.05 && percentLoss > 0) {
            stage = "轻度";
            totalWater = 120 * (currentWeight + weightLoss);
        } else if (percentLoss < 0.1 && percentLoss >= 0.05) {
            stage = "中度";
            totalWater = 150 * (currentWeight + weightLoss);
        } else if (percentLoss < 1 && percentLoss >= 0.1) {
            stage = "重度";
            totalWater = 180 * (weightLoss + currentWeight);
        } else {
            throw new Error("请输入正确的体重和体重减少量");
        }

        if (phase === "快速补液阶段") {
            tstageWater = totalWater / 2 - 20 * (weightLoss + currentWeight);
            if (osmolality === null) {
                throw new Error("在快速补液阶段必须选择渗透压");
            }
            // 根据选择的渗透压计算逻辑
            if (osmolality === "低渗") {
                NaCl = 4 * tstageWater / 9;
                glucose = 111 * tstageWater / 225;
                NaHCO3 = 14 * tstageWater / 225;
            } else if (osmolality === "等渗") {
                NaCl = tstageWater / 3;
                glucose = 93 * tstageWater / 150;
                NaHCO3 = 7 * tstageWater / 150;
            } else if (osmolality === "高渗") {
                NaCl = tstageWater / 3;
                glucose = 2 * tstageWater / 3;
                NaHCO3 = 0;
            }
        } else if (phase === "扩容阶段") {
            tstageWater = (weightLoss + currentWeight) * 20;
            // 扩容阶段的计算逻辑
            NaHCO3 = 28 * (weightLoss + currentWeight) / 15;
            NaCl = 40 * (weightLoss + currentWeight) / 3;
            glucose = 72 * (weightLoss + currentWeight) / 15;
        } else if (phase === "继续补液阶段") {
            // 继续补液阶段的计算逻辑
            tstageWater = totalWater / 2;
            if (concentration === null) {
                throw new Error("在继续补液阶段请输入1/2张或者1/3张");
            } else if (concentration === "1/3张") {
                NaCl = tstageWater / 3;
                glucose = 2 * tstageWater / 3;
                NaHCO3 = 0;
            } else if (concentration === "1/2张") {
                NaCl = tstageWater / 3;
                glucose = 31 * tstageWater / 50;
                NaHCO3 = 7 * tstageWater / 150;
            }
        } else {
            throw new Error("请选择一个阶段");
        }

        // 将结果转换为整数
        NaHCO3 = Math.round(NaHCO3);
        NaCl = Math.round(NaCl);
        glucose = Math.round(glucose);

        return { stage, totalWater, NaHCO3, NaCl, glucose, tstageWater };

    } catch (e) {
        alert("错误: " + e.message);
        return { stage: null, totalWater: null, NaHCO3: null, NaCl: null, glucose: null, tstageWater: null };
    }
}

function calculateQuickRatio(totalVolume, fluidType, mNaCl = 0.9, mNaHCO3 = 5, mGlucose = 5) {
    let NaHCO3 = 0;
    let NaCl = 0;
    let glucose = 0;

    if (fluidType === "1:1含钠液") {
        NaHCO3 = 0;
        NaCl = (9 * totalVolume) / (20 * mNaCl);
    } else if (fluidType === "1:2含钠液") {
        NaHCO3 = 0;
        NaCl = (0.3 * totalVolume) / mNaCl;
    } else if (fluidType === "1:4含钠液") {
        NaHCO3 = 0;
        NaCl = (9 * totalVolume) / (50 * mNaCl);
    } else if (fluidType === "2:1等张含钠液") {
        NaHCO3 = (7 * totalVolume) / (15 * mNaHCO3);
        NaCl = (3 * totalVolume) / (5 * mNaCl);
    } else if (fluidType === "2:3:1含钠液") {
        NaHCO3 = (7 * totalVolume) / (30 * mNaHCO3);
        NaCl = (3 * totalVolume) / (10 * mNaCl);
    } else if (fluidType === "4:3:2含钠液") {
        NaHCO3 = (14 * totalVolume) / (45 * mNaHCO3);
        NaCl = (2 * totalVolume) / (5 * mNaCl);
    }

    glucose = totalVolume - NaCl - NaHCO3;

    return [Math.round(NaHCO3), Math.round(NaCl), Math.round(glucose)];
}

function updateCustomConcentrationOptions() {
    const concentrationMode = document.querySelector('input[name="concentration-mode"]:checked').value;
    const customConcentrationGroup = document.getElementById('custom-concentration-group');
    if (concentrationMode === "自定义浓度") {
        customConcentrationGroup.style.display = 'block';
    } else {
        customConcentrationGroup.style.display = 'none';
    }
}

function onCalculate() {
    const currentWeight = parseFloat(document.getElementById('current-weight').value);
    const weightLoss = parseFloat(document.getElementById('weight-loss').value);
    const phase = document.querySelector('input[name="phase"]:checked').value;
    const osmolality = phase === "快速补液阶段" ? document.querySelector('input[name="osmolality"]:checked').value : null;
    const concentration = phase === "继续补液阶段" ? document.querySelector('input[name="concentration"]:checked').value : null;

    const result = calculate(currentWeight, weightLoss, phase, osmolality, concentration);
    if (result) {
        // 计算num
        const numResult = calculateNum(result.tstageWater);
        const num = numResult[0];
        const n = numResult[1];
        const left = numResult[2];
        const numLeft = numResult[3];

        // 根据stage, phase, concentration和osmolality确定style
        const styleDict = {
            ["轻度,快速补液阶段,低渗,null"]: "4:3:2含钠液",
            ["轻度,快速补液阶段,等渗,null"]: "2:3:1含钠液",
            ["轻度,快速补液阶段,高渗,null"]: "1:2含钠液",
            ["中度,快速补液阶段,低渗,null"]: "4:3:2含钠液",
            ["中度,快速补液阶段,等渗,null"]: "2:3:1含钠液",
            ["中度,快速补液阶段,高渗,null"]: "1:2含钠液",
            ["重度,快速补液阶段,低渗,null"]: "4:3:2含钠液",
            ["重度,快速补液阶段,等渗,null"]: "2:3:1含钠液",
            ["重度,快速补液阶段,高渗,null"]: "1:2含钠液",
            ["轻度,扩容阶段,null,null"]: "2:1等张含钠液",
            ["中度,扩容阶段,null,null"]: "2:1等张含钠液",
            ["重度,扩容阶段,null,null"]: "2:1等张含钠液",
            ["轻度,继续补液阶段,null,1/2张"]: "2:3:1含钠液",
            ["轻度,继续补液阶段,null,1/3张"]: "1:2含钠液",
            ["中度,继续补液阶段,null,1/2张"]: "2:3:1含钠液",
            ["中度,继续补液阶段,null,1/3张"]: "1:2含钠液",
            ["重度,继续补液阶段,null,1/2张"]: "2:3:1含钠液",
            ["重度,继续补液阶段,null,1/3张"]: "1:2含钠液",
        };
        const styleKey = `${result.stage},${phase},${osmolality},${concentration}`;
        const style = styleDict[styleKey] || "未知补液";

        // 更新描述信息
        const description = `该患者目前处于${result.stage}脱水状态，可以考虑补充总共${result.totalWater.toFixed(0)} mL的${style} 液体，当前阶段共计补充${result.tstageWater.toFixed(0)}mL的液体，考虑使用${n}个${num} mL的补液袋,其对应的剂量如下表配置：`;
        document.getElementById('description').value = description;

        // 显示输出框
        document.getElementById('NaHCO3').style.display = 'block';
        document.getElementById('NaCl').style.display = 'block';
        document.getElementById('glucose').style.display = 'block';
        document.getElementById('label-NaHCO3').style.display = 'block';
        document.getElementById('label-NaCl').style.display = 'block';
        document.getElementById('label-glucose').style.display = 'block';

        if (left > 0) {
            const NaHCO3_500 = Math.round(result.NaHCO3 * 500 / result.tstageWater);
            const NaCl_500 = Math.round(result.NaCl * 500 / result.tstageWater);
            const glucose_500 = Math.round(result.glucose * 500 / result.tstageWater);
            const NaHCO3_left = Math.round(result.NaHCO3 * left / result.tstageWater);
            const NaCl_left = Math.round(result.NaCl * left / result.tstageWater);
            const glucose_left = Math.round(result.glucose * left / result.tstageWater);

            document.getElementById('NaHCO3').value = `${NaHCO3_500} ml              ${NaHCO3_left} ml`;
            document.getElementById('NaCl').value = `${NaCl_500} ml              ${NaCl_left} ml`;
            document.getElementById('glucose').value = `${glucose_500} ml              ${glucose_left} ml`;
        } else {
            document.getElementById('NaHCO3').value = `${result.NaHCO3} ml`;
            document.getElementById('NaCl').value = `${result.NaCl} ml`;
            document.getElementById('glucose').value = `${result.glucose} ml`;
        }
        
        const weight = (currentWeight + weightLoss) * 50;
        const weight2 = weight * 2;
        // 检查是否满足特殊条件
        const specialConditions = {
            ["轻度,扩容阶段"]: `注意：轻度脱水无需扩容，可以考虑使用${weight}ml的口服补液盐，如果考虑静脉补液，考虑上表。`,
            ["中度,扩容阶段"]: `注意：中度脱水无需扩容，可以考虑使用${weight2}ml的口服补液盐，如果考虑静脉补液，考虑上表。`,
        };
        const specialKey = `${result.stage},${phase}`;
        const specialNote = specialConditions[specialKey] || "";
        if (specialNote) {
            document.getElementById('special-note-text').value = specialNote;
            document.getElementById('special-note').style.display = 'block';
        } else if (left) {
            const specialNote = `注意：左侧为${n}个500ml补液袋需要配满的配比，右侧为使用${numLeft}ml的补液袋中剩余液体的配比`;
            document.getElementById('special-note-text').value = specialNote;
            document.getElementById('special-note').style.display = 'block';
        } else {
            document.getElementById('special-note').style.display = 'none';
        }
    }
}

function onCalculateQuickRatio() {
    try {
        const totalVolume = parseFloat(document.getElementById('total-volume').value);
        const fluidType = document.querySelector('input[name="fluid-type"]:checked').value;
        let mNaCl = 0.9;
        let mNaHCO3 = 5;
        let mGlucose = 5;

        if (document.querySelector('input[name="concentration-mode"]:checked').value === "自定义浓度") {
            mNaCl = parseFloat(document.getElementById('custom-NaCl').value);
            mNaHCO3 = parseFloat(document.getElementById('custom-NaHCO3').value);
            mGlucose = parseFloat(document.getElementById('custom-glucose').value);
        }

        const result = calculateQuickRatio(totalVolume, fluidType, mNaCl, mNaHCO3, mGlucose);

        document.getElementById('quick-NaHCO3').value = `${result[0]} ml`;
        document.getElementById('quick-NaCl').value = `${result[1]} ml`;
        document.getElementById('quick-glucose').value = `${result[2]} ml`;
    } catch (e) {
        alert("错误: " + e.message);
    }
}