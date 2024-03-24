from flask import *
import pandas as pd

app = Flask(__name__)
icpNo = "未备案网站，请自行甄别"
compnames = []
compName = 'Rhythm Comp System'


if __name__ == "__main__":
    config_file = open('config.json', 'r', encoding='utf-8')
    config = json.load(config_file)
    compnames = config["main"]["comp"]
    xlsdata = {}
    temp = {}
    for filename in compnames:
        chartFile = "./uploads/" + filename + ".xls"
        data = pd.ExcelFile(chartFile)
        sheet_names = data.sheet_names
        for name in sheet_names:
            dataor = pd.read_excel(chartFile, sheet_name=name, header=None)
            lists = dataor.values.tolist()
            xlsdata.setdefault(filename,temp)
            xlsdata[filename].setdefault(name,None)
            xlsdata[filename][name] = lists
    print(xlsdata)
    #app.run(ssl_context=('./server.crt', './server.key'),debug=True)