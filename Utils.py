"""
工具类
"""
from calcFun import Calc, Calc_Plus
import matplotlib.pyplot as plt
from PIL import Image
import base64, io
import numpy as np
from image_base64 import model_image_base64

allowed_model = [
    "外层单线不对地",
    "外层单线对地",
    "内层单线不对地", 
    "内层单线对地",
    "外层双线不对地",
    "外层双线对地",
    "内层双线不对地",
    "内层双线对地"
]

_allowed_model_arg = {
    "外层单线不对地": ["H1", "Er1", "W1", "T1", "C1", "C2", "CEr"],
    "外层单线对地": ["H1", "Er1", "W1", "D1", "T1", "C1", "C2", "CEr"],
    "内层单线不对地": ["H1", "Er1", "H2", "Er2", "W1", "T1"],
    "内层单线对地": ["H1", "Er1", "H2", "Er2", "W1", "D1", "T1"],
    "外层双线不对地": ["H1", "Er1", "W1", "S1", "T1", "C1", "C2", "C3", "CEr"],
    "外层双线对地": ["H1", "Er1", "W1", "S1", "D1", "T1", "C1", "C2", "C3", "CEr"],
    "内层双线不对地": ["H1", "Er1", "H2", "Er2", "W1", "S1", "T1"],
    "内层双线对地": ["H1", "Er1", "H2", "Er2", "W1", "S1", "D1", "T1"]
}

def get_model_arg(model:str)->list:
    """
    获取模型所需的参数
    """
    if model in allowed_model:
        return _allowed_model_arg[model]
    else:
        return []

def input_arg(model_arg_dict:dict)->dict:
    """
    输入参数
    """
    for arg in model_arg_dict:
        if arg == "C1" or arg == "C2" or arg == "C3" or arg == "CEr":
            print("当前参数 "+arg+" 的值可以为空，因为有一个默认值！")
        v = input("请输入 "+arg+" 的值：")
        if v == "":
            model_arg_dict[arg] = None
        else:
            model_arg_dict[arg] = float(v)
    return model_arg_dict

def calc_impedance(model:str,model_arg_dict:dict)->float:
    """
    正算阻抗
    """
    calc = Calc()
    if model == "外层单线不对地":
        return calc.外层单线不对地(model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["W1"],model_arg_dict["T1"],model_arg_dict["C1"],model_arg_dict["C2"],model_arg_dict["CEr"])
    elif model == "外层单线对地":
        return calc.外层单线对地(model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["W1"],model_arg_dict["D1"],model_arg_dict["T1"],model_arg_dict["C1"],model_arg_dict["C2"],model_arg_dict["CEr"])
    elif model == "内层单线不对地":
        return calc.内层单线不对地(model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["H2"],model_arg_dict["Er2"],model_arg_dict["W1"],model_arg_dict["T1"])
    elif model == "内层单线对地":
        return calc.内层单线对地(model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["H2"],model_arg_dict["Er2"],model_arg_dict["W1"],model_arg_dict["D1"],model_arg_dict["T1"])
    elif model == "外层双线不对地":
        return calc.外层双线不对地(model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["W1"],model_arg_dict["S1"],model_arg_dict["T1"],model_arg_dict["C1"],model_arg_dict["C2"],model_arg_dict["C3"],model_arg_dict["CEr"])
    elif model == "外层双线对地":
        return calc.外层双线对地(model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["W1"],model_arg_dict["S1"],model_arg_dict["D1"],model_arg_dict["T1"],model_arg_dict["C1"],model_arg_dict["C2"],model_arg_dict["C3"],model_arg_dict["CEr"])
    elif model == "内层双线不对地":
        return calc.内层双线不对地(model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["H2"],model_arg_dict["Er2"],model_arg_dict["W1"],model_arg_dict["S1"],model_arg_dict["T1"])
    elif model == "内层双线对地":
        return calc.内层双线对地(model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["H2"],model_arg_dict["Er2"],model_arg_dict["W1"],model_arg_dict["S1"],model_arg_dict["D1"],model_arg_dict["T1"])
    else:
        return 0

def reverse_calc_impedance(model:str,model_arg_dict:dict,Z:float)->float:
    """
    反算阻抗
    输入模型，模型参数，目标阻抗值，返回目标阻抗值对应的参数
    """
    calc = Calc_Plus()
    if model == "外层单线不对地":
        return calc.外层单线不对地reverse(Z,model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["W1"],model_arg_dict["T1"],model_arg_dict["C1"],model_arg_dict["C2"],model_arg_dict["CEr"])
    elif model == "外层单线对地":
        return calc.外层单线对地reverse(Z,model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["W1"],model_arg_dict["D1"],model_arg_dict["T1"],model_arg_dict["C1"],model_arg_dict["C2"],model_arg_dict["CEr"])
    elif model == "内层单线不对地":
        return calc.内层单线不对地reverse(Z,model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["H2"],model_arg_dict["Er2"],model_arg_dict["W1"],model_arg_dict["T1"])
    elif model == "内层单线对地":
        return calc.内层单线对地reverse(Z,model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["H2"],model_arg_dict["Er2"],model_arg_dict["W1"],model_arg_dict["D1"],model_arg_dict["T1"])
    elif model == "外层双线不对地":
        return calc.外层双线不对地reverse(Z,model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["W1"],model_arg_dict["S1"],model_arg_dict["T1"],model_arg_dict["C1"],model_arg_dict["C2"],model_arg_dict["C3"],model_arg_dict["CEr"])
    elif model == "外层双线对地":
        return calc.外层双线对地reverse(Z,model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["W1"],model_arg_dict["S1"],model_arg_dict["D1"],model_arg_dict["T1"],model_arg_dict["C1"],model_arg_dict["C2"],model_arg_dict["C3"],model_arg_dict["CEr"])
    elif model == "内层双线不对地":
        return calc.内层双线不对地reverse(Z,model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["H2"],model_arg_dict["Er2"],model_arg_dict["W1"],model_arg_dict["S1"],model_arg_dict["T1"])
    elif model == "内层双线对地":
        return calc.内层双线对地reverse(Z,model_arg_dict["H1"],model_arg_dict["Er1"],model_arg_dict["H2"],model_arg_dict["Er2"],model_arg_dict["W1"],model_arg_dict["S1"],model_arg_dict["D1"],model_arg_dict["T1"])
    else:
        return 0

# 1. 读取图片并转换为Base64编码
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


# 2. 将Base64字符串解码为图像数据
def base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    return image

def display_image(image):
    plt.ion()
    # 设置无工具栏
    plt.rcParams['toolbar'] = 'none'
    # 将PIL图像转换为numpy数组
    img_array = np.array(image)
    # print("图像数据形状:", img_array.shape)
    # print("图像数据类型:", img_array.dtype)
    
    # 检查数据类型
    if img_array.dtype == np.object_:
        raise TypeError("图像数据为object类型，无法显示。请检查图像数据是否正确解码。")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    # 显示图像
    plt.imshow(img_array)
    plt.axis('off')  # 不显示坐标轴
    plt.show()

def show_model_image(model: str):
    """
    显示模型图片，使用非阻塞模式
    """
    # logger.add("rotating_log.log")
    # Test 读取图片并转换为Base64编码
    # for model in allowed_model:
    #     model_image_base64[model] = image_to_base64(f"image/{model}.jpg")
    #     logger.info(model+" Base64: "+model_image_base64[model])

    try:
        # image_path = f'image/{model}.jpg' 
        # base64_string = image_to_base64(image_path)
        image = base64_to_image(model_image_base64[model])
        display_image(image)
    except Exception as e:
        print(f"出错: {e}")