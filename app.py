import json
import secrets
import binascii
from dataclasses import dataclass
from werkzeug.utils import secure_filename
import os
from flask import *
from flask import session
import locale
from time import localtime, strftime
from glob import glob
import pandas as pd

app = Flask(__name__,static_url_path="/")
# 上传的文件夹名称
UPLOAD_FOLDER = 'uploads'
# 上传的文件夹路径
UPLOAD_PATH = os.path.join(app.root_path,'upload')
# 允许上传的文件格式
ALLOWED_EXTENSIONS = {'txt', 'xls', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@dataclass
class Admin():
    id: int
    username: str
    password: str

id_temp = 1
admins = []
compName = 'Rhythm Comp System'
icpNo = "未备案网站，请自行甄别"
compnames = []

@app.before_request
def before_request():
    g.admin = None
    session.pop("compname",compName)
    session['compname'] = compName
    if 'user_id' in session:
        user = [u for u in admins if u.id == session['user_id']]
        g.admin = user


@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == "POST":
        #登录操作
        session.pop('user_id',None)
        username = request.form.get("username",None)
        password = request.form.get("password",None)
        print(username,password)
        user = [u for u in admins if u.username == username]
        if len(user) > 0:
            user = user[0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('admin'))
    return render_template("login.html",compName = session.get("compname"), icp = icpNo)

@app.route('/logout')
def logout():
    session.clear()
    return render_template("logout.html",compName = session.get("compname"), icp = icpNo)

@app.route('/admin')
def admin():
    if not g.admin:
        return redirect(url_for("login"))
    return render_template("admin.html",compName = session.get("compname"), icp = icpNo)

# 拆解filename，获取后缀并判断是否允许上传
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET','POST'])
def upload():
    if not g.admin:
        return redirect(url_for("login"))
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 最关键的代码，调用save函数，传入存储路径作为参数，用os.path.join拼接文件夹和文件名
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload'))
    return render_template("upload.html",compName = session.get("compname"),icp = icpNo)

# 获取upload目录下所有文件名
# os.walk函数能获取对应路径下的文件名
def get_filenames(file_dir):
    filenames = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            filenames.append(file)
    return filenames

def get_edit_time(path):
    """
    获取path下所有文件的最后修改时间，返回其中最新的修改时间。\n
    返回的是一个已经格式化的时间，具体格式为：年月日 时：分：秒。\n
    注意：该函数会忽略path下子文件夹中的文件。
    """
    time_list = []
    glob_path = os.path.join(path, "*.*")
    file_list = glob(glob_path)
    for i in file_list:
        time = os.path.getmtime(i)
        locale.setlocale(locale.LC_CTYPE, 'chinese')
        edit_time_locale = localtime(time)
        fromat_time = strftime("%Y年%m月%d日 %H:%M:%S", edit_time_locale)
        time_list.append(fromat_time)
    return time_list

@app.route('/directory')
def directory():
    # 调用get_filenames获取到upload文件夹下的所有文件名，将文件名传入directory.html中
    # 使用a标签包裹每一个文件名，点击即可下载~
    filenames = get_filenames('uploads')
    buildtime = get_edit_time("./uploads")
    return render_template("directory.html",compName = session.get("compname"), filenames=filenames, buildtimes = buildtime)

@app.route('/download/<filename>')
# 在目录页面下，用户点击对应的a标签，调用download函数，filename作为参数
# 使用send_from_directory方法返回对应目录下的对应文件，直接下载即可
def download(filename):
    return send_from_directory(UPLOAD_PATH, filename, as_attachment=True)

@app.route('/delete/<filename>')
# 在directory.html中就是一个delete的a标签按钮，点击即跳转到delete函数，filename为参数
# delete函数调用os模块中的unlink函数，传入要删除的文件的路径，用os.path.join去拼接路径和文件名
# 返回文件目录页
def delete(filename):
    os.unlink(os.path.join(UPLOAD_PATH, filename))
    return redirect(url_for('directory'))

@app.route("/charts")
def charts():
    xlsdata = {}
    temp = {}
    for filename in compnames:
        chartFile = "./uploads/" + filename + ".xls"
        data = pd.ExcelFile(chartFile)
        sheet_names = data.sheet_names
        for name in sheet_names:
            dataor = pd.read_excel(chartFile, sheet_name=name, header=None)
            lists = dataor.values.tolist()
            xlsdata.setdefault(filename, temp)
            xlsdata[filename].setdefault(name, None)
            xlsdata[filename][name] = lists
    return render_template("charts.html",compnames = compnames,compName = session.get("compname"),icp=icpNo,data = xlsdata)

@app.route('/timer')
def timer():
    return render_template("timer.html",compName = session.get("compname"),icp = icpNo)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",compName = session.get("compname"),icp = icpNo)


def init(config1):
    if config1["main"]["secure"] != "":
        app.config["SECRET_KEY"] = config1["main"]["secure"]["SECRET_KEY"]
    else:
        app.config["SECRET_KEY"] = secrets.token_hex()



#配置导入
if __name__ == '__main__':
    config_file = open('config.json','r',encoding='utf-8')
    config = json.load(config_file)
    for i in config["main"]["admins"]:
        admins.append(Admin(id_temp,i,config["main"]["admins"][i]))
        id_temp += 1
    print(admins)
    if config["main"]["name"] != "":
        compName = config["main"]['name']
    if config['addup']['ICP'] != '':
        icpNo = config['addup']['ICP']
    compnames = config["main"]["comp"]
    init(config)
    print(app.config)
    app.run(ssl_context=('./server.crt', './server.key'),debug=True)
