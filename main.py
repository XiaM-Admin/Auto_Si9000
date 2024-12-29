import sys
from Utils import allowed_model, get_model_arg, input_arg, calc_impedance, reverse_calc_impedance, show_model_image

def 正算():
    print("选择的计算模式为 正算模式")
    print("选择的阻抗模型为", sys.argv[2])
    show_model_image(sys.argv[2])
    model_arg = get_model_arg(sys.argv[2])
    model_arg_dict = {model_arg[i]:0 for i in range(len(model_arg))}
    model_arg_dict = input_arg(model_arg_dict)
    print("正算结果为：\r\n", round(calc_impedance(sys.argv[2], model_arg_dict), 3))

def 反算():
    print("选择的计算模式为 反算模式")
    print("选择的阻抗模型为", sys.argv[2])
    show_model_image(sys.argv[2])
    Z: float = float(input("请输入目标阻抗值："))
    model_arg = get_model_arg(sys.argv[2])
    model_arg_dict = {model_arg[i]:0 for i in range(len(model_arg))}
    model_arg_dict = input_arg(model_arg_dict)
    print("反算结果为：\r\n", reverse_calc_impedance(sys.argv[2], model_arg_dict, Z))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 引导用户输入参数
        print("//Auto_Si9000//")
        print("1. 正算")
        print("2. 反算")
        calc_mode = input("请选择计算模式：")
        print("支持的模型有：", allowed_model)
        model = input("请选择阻抗模型(请输入模型名称)：")

        if calc_mode == "1":
            # 将参数添加到sys.argv中
            sys.argv.append(calc_mode)
            sys.argv.append(model)
            正算()
            input("请按任意键退出")
            exit()
        elif calc_mode == "2":
            # 将参数添加到sys.argv中
            sys.argv.append(calc_mode)
            sys.argv.append(model)
            反算()
            input("请按任意键退出")
            exit()
        else:
            print("请输入正确的模式！")
            input("请按任意键退出")
            exit()

    if sys.argv[1] == "模型":
        print("支持的模型有：", allowed_model)
        exit()

    if sys.argv[1] == "正算":  
        if sys.argv[2] in allowed_model:
            正算()
            input("请按任意键退出")
            exit()
        else:
            print("请提供正确的模型！")
            print("支持的模型有：", allowed_model)
            exit()
    
    elif sys.argv[1] == "反算":
        if sys.argv[2] in allowed_model:
            反算()
            input("请按任意键退出")
            exit()
        else:
            print("请提供正确的模型！")
            print("支持的模型有：", allowed_model)
            input("请按任意键退出")
            exit()
    else:
        print("请提供正确的参数！")
        input("请按任意键退出")
        exit()



""" 外层单线不对地
# ////////////外层单线不对地////////////
# calc = Calc()
# calc.外层单线不对地(0.077, 3.9, 0.113, 0.06)

# Cp = Calc_Plus()
# Cp.外层单线不对地s(0.4, 4.4, 0.4, 0.045,Count=10,Step=0.01)

# calc = Calc_Plus()
# new_width = calc.外层单线不对地reverse(Z=50, H1=0.077, Er1=3.9, W1=0.1, T1=0.06)
# print(new_width)
"""

""" 外层单线对地
# ////////////外层单线对地////////////
# calc = Calc()
# calc.外层单线对地(0.077, 3.9, 0.097,0.132, 0.06)

# calc = Calc_Plus()
# new_width = calc.外层单线对地reverse(Z=50, H1=0.077, Er1=3.9, W1=0.11,D1=0.126, T1=0.06)
# print(new_width)
"""

""" 内层单线不对地
# ////////////内层单线不对地////////////
# calc = Calc_Plus()
# new_width = calc.内层单线不对地(H1=0.83, Er1=4.4, H2=0.112, Er2=3.9, W1=0.11, T1=0.03)
# print(new_width)

# calc = Calc_Plus()
# new_width = calc.内层单线不对地reverse(Z=50, H1=0.83, Er1=4.4, H2=0.112, Er2=3.9, W1=0.09, T1=0.03)
# print(new_width)
"""

""" 内层单线对地
# ////////////内层单线对地////////////
# calc = Calc_Plus()
# new_width = calc.内层单线对地(H1=0.83, Er1=4.4, H2=0.112, Er2=3.9, W1=0.095, D1=0.128, T1=0.03)
# print(new_width)

# calc = Calc_Plus()
# new_width = calc.内层单线对地reverse(Z=50, H1=0.83, Er1=4.4, H2=0.112, Er2=3.9, W1=0.12, D1=0.116, T1=0.03)
# print(new_width)
"""

""" 外层双线不对地
# ////////////外层双线不对地////////////
# calc = Calc_Plus()
# new_width = calc.外层双线不对地(H1=0.077, Er1=3.9, W1=0.115, S1=0.189, T1=0.06)
# print(new_width)

# calc = Calc_Plus()
# new_width = calc.外层双线不对地reverse(Z=90, H1=0.077, Er1=3.9, W1=0.1, S1=0.204, T1=0.06)
# print(new_width)
"""

""" 内层双线不对地
# ////////////内层双线不对地////////////
# calc = Calc_Plus()
# new_width = calc.内层双线不对地(H1=0.83, Er1=4.4, H2=0.112, Er2=3.9, W1=0.103, S1=0.167, T1=0.03)
# print(new_width)

# calc = Calc_Plus()
# new_width = calc.内层双线不对地reverse(Z=90, H1=0.83, Er1=4.4, H2=0.112, Er2=3.9, W1=0.09, S1=0.18, T1=0.03)
# print(new_width)
"""

""" 外层双线对地
# ////////////外层双线对地////////////
# calc = Calc_Plus()
# new_width = calc.外层双线对地(H1=0.077, Er1=3.9, W1=0.108, S1=0.182, D1=0.161, T1=0.06)
# print(new_width)

# calc = Calc_Plus()
# new_width = calc.外层双线对地reverse(Z=90, H1=0.077, Er1=3.9, W1=0.08, S1=0.21, D1=0.175, T1=0.06)
# print(new_width)
"""

""" 内层双线对地
# ////////////内层双线对地////////////
# calc = Calc_Plus()
# new_width = calc.内层双线对地(H1=0.83, Er1=4.4, H2=0.112, Er2=3.9, W1=0.092, S1=0.138, D1=0.154, T1=0.03)
# print(new_width)

# calc = Calc_Plus()
# new_width = calc.内层双线对地reverse(Z=90, H1=0.83, Er1=4.4, H2=0.112, Er2=3.9, W1=0.11, S1=0.12, D1=0.145, T1=0.03)
# print(new_width)
"""
