import pandas as pd
import copy

class ModelManager:
    def __init__(self):
        self.dataDict = {

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

        self.dataTemplate = { # Will be used on excel template, and main menu

            "Style Image": ["text", "", ""],
            "Image to Convert": ["text", "", ""],

            "Output Size": ["text", "512", "512"],

            "Iterations": ["text", "800", "800"],
            "Create Image every iteration": ["text", "200", "200"],
            
            "Model to Use": ["list", ["accurate", "balanced", "fast"], "accurate"],
            "CPU to Use": ["list", ["cpu", "gpu", "gpu_modified"], "gpu_modified"],

            "Style Scale": ["text", "1.0", "1.0"],

            "Content Weight": ["text", "5", "5"],
            "Style Weight": ["text", "100", "100"],
            "Variation Weight": ["text", "0.001", "0.001"],

            "Preserve Color": ["list", ["Yes", "No"], "No"],

            "Content Layer": ["text", "relu4_2", "relu4_2"],
            "Style Layer": ["text", "relu1_1,relu2_1,relu3_1,relu4_1,relu5_1", "relu1_1,relu2_1,relu3_1,relu4_1,relu5_1"],
        }

        self.dataMappings = {

            "Style Image": "style_image",
            "Image to Convert": "content_image",

            "Output Size": "output_size",

            "Iterations": "iterations",
            "Create Image every iteration": "create_iter",
            
            "Model to Use": "model",
            "CPU to Use": "cpu",
            "Style Scale": "style_scale",
            "Content Weight": "content_weight",
            "Style Weight": "style_weight",
            "Variation Weight": "tv_weight",
            "Preserve Color": "original_color",

            "Content Layer": "content_layer",
            "Style Layer": "style_layer",

        }

        self.param_list = {

            "Model to Use": ["Model to Use", "Model to Use - What training model to use in creating output?",["accurate", "balanced", "fast"]],
            "CPU to Use": ["CPU to Use", "CPU to Use - What computing power to use in process" ,["cpu", "gpu", "gpu_modified"]],
            "Preserve Color": ["Preserve Color", "Preserve Color - Preserve content image palette?" ,["Yes", "No"]],

        }

    def excel_Write(self, data=None, location="./Results.xlsx"): #Assuming that the category of data is uniform with data flow

        # Create the main-list ===========================================================

        params = []

        if not data:
            params = copy.deepcopy(self.dataTemplate)

            col = list(params.keys())
            data = list(i[2] for i in params.values())
            df = pd.DataFrame([data], columns=col)

        else:
            params = data

            col = list(params.keys())

            data = list(params.values())

            datax = []
            for i in range(len(data[0])):
                datax_bit = []
                for j in range(len(col)):
                    datax_bit.append(data[j][i])
                datax.append(datax_bit)

            df = pd.DataFrame(datax, columns=col)



        writer = pd.ExcelWriter(location)
        df.to_excel(writer, index=False, sheet_name="LayoutData")

        # Get the xlsxwriter workbook and worksheet objects.
        workbook  = writer.book
        worksheet = writer.sheets['LayoutData']

        # Create the choices list ===========================================================

        param_list = []

        param_list = self.param_list

        col_opt = list(param_list.keys())
        data_opt = list(p[2] for p in param_list.values())
        data_title = list(p[0] for p in param_list.values())
        data_desc = list(p[1] for p in param_list.values())

        df_2 = pd.DataFrame(data_opt).transpose()
        df_2.columns = col_opt

        df_2.to_excel(writer, index=False, sheet_name="LayoutChoices")

        worksheet_options = writer.sheets['LayoutChoices']

        # Add some cell formats.
        format1 = workbook.add_format({'align': 'center'})

        # Create the drop down menu ========================================================

        # Loop over the params
        # If title in param_options, apply formatting

        required = {}

        for i, label in enumerate(col):
            if label in (col_opt):
                index = col_opt.index(label)

                dropdown_col = ""
                x_letters = int(i)

                while x_letters >= 26:
                    dropdown_col = dropdown_col + chr(ord('A') + x_letters//26-1)
                    x_letters -= 26
                dropdown_col = dropdown_col + chr(ord('A') + x_letters%26)

                dropdown_range = f"{dropdown_col}2:{dropdown_col}100"

                required[dropdown_col] = label

                source_col = ""
                x_letters = int(index)

                while x_letters >= 26:
                    source_col = source_col + chr(ord('A') + x_letters//26-1)
                    x_letters -= 26
                source_col = source_col + chr(ord('A') + x_letters%26)

                source_range = f"${source_col}$2:${source_col}${len(data_opt[index])+1}"

                worksheet.data_validation(dropdown_range, {
                    'validate': 'list',
                    'source': f'=LayoutChoices!{source_range}',
                    'input_title': data_title[index],
                    'input_message': data_desc[index],
                    'error_message': 'Option not available. If you have new layouts added, please generate a new excel file from the cover maker app.'
                    })

            elif self.dataTemplate[label][2] != "":
                dropdown_col = ""
                x_letters = int(i)

                while x_letters >= 26:
                    dropdown_col = dropdown_col + chr(ord('A') + x_letters//26-1)
                    x_letters -= 26
                dropdown_col = dropdown_col + chr(ord('A') + x_letters%26)

                dropdown_range = f"{dropdown_col}2:{dropdown_col}100"

                required[dropdown_col] = label

        # Set designs into the board ========================================================

        # Add some cell formats.
        # this was already declared above, will be repetitive if i do again
        #format1 = workbook.add_format({'align': 'center'})

        # Set the column width and format.
        format2 = workbook.add_format({
            'bg_color': '#fa00fa',
            'align': 'center',
            'border': 1,

            })

        for col, text in required.items():
            worksheet.write(f'{col}1', f'{text}', format2)

        worksheet.set_column('A1:AG1', 20, format1)
        worksheet.set_column('S1:T1', 35)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

        return location

    def excel_Read(self, location, mode="scrap"):
        exc = pd.read_excel(location)
        amount = len(exc.values.tolist())

        retDict = []

        for i in range(amount):
            if mode=="scrap":
                entry = self.template_to_dict(exc.iloc[i].fillna('').to_dict())
            else:
                entry = exc.iloc[i].fillna('').to_dict()

                for key, val in entry.items():
                    entry[key] = str(val)

            retDict.append(entry)

        return retDict

    def template_to_dict(self, template):
        cleared = []

        toRet = copy.deepcopy(self.dataDict)

        for key, val in template.items():
            target = self.dataMappings[key]

            if target == "_":
                toRet[key] = str(val)
            else:
                if '>' in target:
                    target = target.split('>')

                    if target[1] == '+':

                        if target[0] not in cleared:
                            cleared.append(target[0])
                            toRet[target[0]] = []

                        toRet[target[0]].append(str(val))
                    else:
                        target[1] = int(target[1])
                        toRet[target[0]][target[1]] = str(val)
                else:
                    toRet[target] = str(val)

        #toRet["Categories"] = [toRet["Categories"]] # A stupid fix

        return toRet

    def create_excelTemplate(self, loc="./Sample.xlsx"):

        self.excel_Write(location=loc)


