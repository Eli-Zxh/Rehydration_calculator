# Rehydration_calculator
//因为受不了临床上每次都要亲自算，写的补液计算器小项目

本项目计算根据：
1.《儿科学》人民卫生出版社 第十版
2.中华医学会儿科学分会消化学组,《中华儿科杂志》编辑委员会. 中国儿童急性感染性腹泻病临床实践指南[J]. 中华儿科杂志,2016,54(7)：483-488.
3.World Health Organization. Diarrhoea treatment: a manual for physicians and other senior health workers. 4th ed. Geneva: WHO; 2005.

采用的输入输出值为：
输入值
患者体重m1
可调节参数：
医院采用的100ml，200ml以及500ml补液袋
10%NaCl或者0.9%NaCl
4%NaHCO3
部分疾病类型以及补液方式
输出值
葡萄糖等渗液体积
NaCl溶液体积
NaHCO3溶液体积

采用计算规则为：
 现体重current_weight，降低体重weight_loss
weight_loss/(weight_loss+current_weight)<5%,轻度，直接喝ORSⅢ50ml/kg
5%<weight_loss/(weight_loss+current_weight)<10%,中度，直接喝ORSⅢ
weight_loss/(weight_loss+current_weight)> 10%,重度
补液总量t=150or180(weight_loss+current_weight)
扩容：
生理盐水NaCl=20(weight_loss+current_weight)*2/3=40(weight_loss+current_weight)/3,
5%葡萄糖
glucose=20(weight_loss+current_weight)-NaCl-NaHCO3=72(weight_loss+current_weight)/15
5%碳酸氢钠
NaHCO3=20(weight_loss+current_weight)*1.4/(3*5)=28(weight_loss+current_weight)/15
快速补液阶段：补t1=t/2-20(weight_loss+current_weight)=55or70(weight_loss+current_weight)
血钠<130mmol/L,低渗,4:3:2含钠液
生理盐水NaCl=4t1/9
glucose=111t1/225
NaHCO3=2t1*1.4/(9*5)=14t1/225
等渗130-150，2:3:1含钠液
NaCl=t1/3
glucose=93t1/150
NaHCO3=1.4t1/(6*5)=7t1/150
高渗>150,1:2(存疑)
NaCl=t1/3
  glucose=2t1/3
继续补液：书上说补充继续丢失量用1/3张到1/2张
t2=t/2
2:3:1
NaCl=t/6
glucose=31t/100
NaHCO3=7t/300
1:2
NaCl=t2/3=t/6
  glucose=2t2/3=t/3

轻中度 如果要静脉补液
t=90or120or150(weight_loss+current_weight)
快速补液阶段：
低渗4:3:2
NaCl=2t/9
glucose=37t/150
NaHCO3=1.4t/45 =7t/225
等渗2:3:1
NaCl=t/6
glucose=31t/100
NaHCO3=1.4t/60=7t/300
高渗1:2
NaCl=t/6
glucose=t/3
继续补液阶段同重度继续补液
                                                                                                                                                 