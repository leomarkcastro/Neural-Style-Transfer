import os
import random

import secrets
import datetime

import json

from PIL import Image

template = {

    "style_image": "",
    "content_image": "",

    "output_size": "512",

    "iterations": "200",
    "create_iter": "100",
    
    "model": "accurate",
    "cpu": "gpu_modified",

    "style_scale": "1.0",

    "content_weight": "5",
    "style_weight": "100",
    "tv_weight": "0.001",

    "content_layers": "relu4_2",
    "style_layers": "relu1_1,relu2_1,relu3_1,relu4_1,relu5_1",
    
    "original_color": "No",

}


def callProcess(parameter, setname="output", style_folder="style", booster_style=None, grayscale=False):
    # parameter should contain a dictionary 
    '''
        style_image
        content_image
        output_image
        ...then the parameters
    '''

    # get random image from style folder

    if "!rnd" in parameter["style_image"]:
        style_list = os.listdir(style_folder)
        random.shuffle(style_list)

        amount = int(parameter["style_image"].strip().replace("!rnd",""))

        booster_list = []
        if booster_style:
            booster_list = os.listdir(booster_style)
            random.shuffle(booster_list)

        parameter["style_image"] = ",".join(
            [f'"{style_folder}/{fi}"' for fi in style_list[:amount]] 
            + [f'"{booster_style}/{fi}"' for fi in booster_list[:1]] 
            )


    content_source_raw = parameter['content_image'].split('.')[0].split("/")[1].replace('/','_')
    print(content_source_raw)
    content_source = f"{content_source_raw}_{datetime.datetime.now().strftime('%m%d %H%M%S')}_{secrets.token_hex(4)}"


    gray_image = parameter["content_image"]

    img = Image.open(gray_image)
    #imgGray = img.convert('L')

    image = Image.new("RGB", img.size, (99,133,150))
    image.paste(img, (0, 0), img) 

    image.thumbnail([300, 300], Image.ANTIALIAS)  # resizes the image to a lower resolution

    if not os.path.exists("proc"):
        os.makedirs('proc')

    gray_image = f"proc/{secrets.token_hex(4)}_{content_source_raw}.jpg"
    
    image.save(gray_image)


    output_folder = f"output/{setname}/{content_source}"
    output_image = f"{output_folder}/stylized_{content_source_raw}_{datetime.datetime.now().strftime('%m%d %H%M%S')}.png"

    command_main = lambda style, content, output, parameters: f"neural-style {style} {content} {output} {parameters}"

    command_style = lambda image : f'-style_image {image}'
    command_image = lambda image : f'-content_image "{image}"'
    command_output = lambda image : f'-output_image "{image}"'
    command_parameters = "" #lambda image : f'-model_file vgg19-d01eb7cb.pth -gpu c -num_iterations "!iterations!"'


    command_style = command_style(parameter["style_image"])
    command_image = command_image(gray_image)
    command_output = command_output(output_image)

    # iterations
    command_parameters += f'-num_iterations {parameter["iterations"]} '
    command_parameters += f'-save_iter {parameter["create_iter"]} '

    # model
    model_to_use = {
        "accurate" : "models/vgg19-d01eb7cb.pth", 
        "balanced" : "models/vgg16-00b39a1b.pth", 
        "fast" : "models/nin_imagenet.pth"
    }
    command_parameters += f'-model_file "{model_to_use[parameter["model"]]}" '

    # cpu
    cpu_to_use = {
        "cpu": "-gpu c",
        "gpu": "-gpu 0",
        "gpu_modified": "-gpu 0 -backend cudnn -cudnn_autotune -optimizer lbfgs",
    }
    command_parameters += f'{cpu_to_use[parameter["cpu"]]} '

    # image size
    command_parameters += f'-image_size {parameter["output_size"]} '

    # style scale
    command_parameters += f'-style_scale {parameter["style_scale"]} '

    # content weight
    if "content_weight" in parameter:
        command_parameters += f'-content_weight {parameter["content_weight"]} '

    # style weight
    if "style_weight" in parameter:
        command_parameters += f'-style_weight {parameter["style_weight"]} '

    # tv weight
    if "tv_weight" in parameter:
        command_parameters += f'-tv_weight {parameter["tv_weight"]} '

    # content layers
    if "content_layers" in parameter:
        command_parameters += f'-content_layers {parameter["content_layers"]} '

    # style layers
    if "style_layers" in parameter:
        command_parameters += f'-style_layers {parameter["style_layers"]} '

    # original colors
    if parameter["original_color"] == "Yes":
        command_parameters += f'-original_colors 1 '


    command_main = command_main(command_style, command_image, command_output, command_parameters)

    print(command_main)
    print()    

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(f'{output_folder}/setting.json', 'w') as fp:
        json.dump(parameter, fp)

    os.system(command_main)

