import cv2
import time
import os
import sys
import subprocess
import requests
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response, flash
from functools import wraps
from multiprocessing import Process, set_start_method
from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime
sys.path.append(os.path.abspath('webssh/webssh'))
from main import make_handlers, make_app, app_listen, ssh_main

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///channels.db'  # 使用 SQLite 数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 可选，关闭修改追踪
app.config['UPLOAD_FOLDER'] = 'uploads/'  # 模型文件上传文件夹
ALLOWED_EXTENSIONS = {'zip', 'tar.gz', 'tgz'}
db = SQLAlchemy(app)

class Channel(db.Model):
    __tablename__ = 'channels'

    channel_number = db.Column(db.Integer, primary_key=True)
    camera_name = db.Column(db.String(100))
    video_url = db.Column(db.String(200))
    status = db.Column(db.String(50))

# 模拟用户数据库
users = {'admin': 'password'}

# 新增模型数据库
class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    filepath = db.Column(db.String(200))
    upload_date = db.Column(db.String(100))
    file_size = db.Column(db.Integer)
    file_md5 = db.Column(db.String(100))

# 定义 Tasks 数据库模型
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 行号
    task_name = db.Column(db.String(100))
    video_source = db.Column(db.String(100))
    report_address = db.Column(db.String(200))
    algorithm_config = db.Column(db.String(500))
    status = db.Column(db.String(50), default="未开始")  # 添加任务状态字段，默认“未开始”

# 检查文件类型是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            return redirect(url_for('basic_info'))
        else:
            return "用户名或密码错误", 401
    return render_template('login.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def basic_info():
    device_info = {
        'device_id': 'RJ-BMOX-000738FADB3FA8289232CA9F49C0329',
        'status': '已授权',
        'software_version': '0.0.54',
        'box_time': '2024-07-09 10:11:32',
        'storage_space': '10.8GB',
        'chip_temperature': '45 °C',
        'system_version': 'BM1684-16 2.7.0'
    }
    chart_data = {
        'timestamps': ['2024/7/9 10:11:16', '2024/7/9 10:11:21', '2024/7/9 10:11:26', '2024/7/9 10:11:31'],
        'cpu_usage': [5, 6, 6, 6],
        'tpu_usage': [50, 55, 55, 55],
        'chip_temp': [45, 45, 45, 45]
    }
    return render_template('basic_info.html', device_info=device_info, chart_data=chart_data)

@app.route('/model_settings')
@login_required
def model_settings():
    models = Model.query.all()  # 从数据库中读取所有已上传的模型
    return render_template('model_settings.html', models=models)

@app.route('/upload_model', methods=['POST'])
@login_required
def upload_model():
    if 'file' not in request.files:
        flash('没有选择文件')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('没有选择文件')
        return redirect(request.url)

    # 检查文件类型
    if not allowed_file(file.filename):
        flash('文件类型不支持，请上传 zip、tar.gz 或 tgz 格式的文件')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # 保存文件到服务器
        file.save(filepath)

        # 获取文件大小和MD5值
        file_size = os.path.getsize(filepath)
        file_md5 = hashlib.md5(open(filepath, 'rb').read()).hexdigest()
        upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 将文件信息存储到数据库
        new_model = Model(
            filename=filename,
            filepath=filepath,
            upload_date=upload_date,
            file_size=file_size,
            file_md5=file_md5
        )
        db.session.add(new_model)
        db.session.commit()

        flash('文件上传成功')
        return redirect(url_for('model_settings'))
    else:
        flash('不支持的文件类型')
        return redirect(request.url)


@app.route('/delete_model/<int:model_id>', methods=['POST'])
@login_required
def delete_model(model_id):
    model = Model.query.get(model_id)
    
    if model:
        try:
            os.remove(model.filepath)  # 删除服务器上的文件
        except FileNotFoundError:
            flash('文件未找到')
        db.session.delete(model)
        db.session.commit()
        flash('模型删除成功')
    else:
        flash('模型未找到')

    return redirect(url_for('model_settings'))

@app.route('/overwrite_model/<int:model_id>', methods=['POST'])
@login_required
def overwrite_model(model_id):
    model = Model.query.get(model_id)

    if 'file' not in request.files:
        flash('没有选择文件')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('没有选择文件')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 覆盖现有文件
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        file_md5 = hashlib.md5(open(filepath, 'rb').read()).hexdigest()
        upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 更新数据库中的记录
        model.filename = filename
        model.filepath = filepath
        model.upload_date = upload_date
        model.file_size = file_size
        model.file_md5 = file_md5

        db.session.commit()

        flash('模型覆盖成功')
        return redirect(url_for('model_settings'))

    else:
        flash('不支持的文件类型')
        return redirect(request.url)

# 保留原始代码逻辑

@app.route('/channel_management')
@login_required
def channel_management():
    channels = Channel.query.all()
    return render_template('channel_management.html', channels=channels)

@app.route('/task_management')
@login_required
def task_management():
    channels = Channel.query.all()
    models = Model.query.all()  # 获取所有算法模型
    tasks = Tasks.query.all()  # 从数据库中加载所有任务
    return render_template('task_management.html', channels=channels,models=models,tasks=tasks)

@app.route('/save_task', methods=['POST'])
def save_task():
    data = request.json
    row_id = data.get('id')
    task = Tasks.query.get(row_id)
    
    if task:
        # 更新已有的任务
        task.task_name = data.get('task_name')
        task.video_source = data.get('video_source')
        task.report_address = data.get('report_address')
        task.algorithm_config = data.get('algorithm_config')
        task.status = data.get('status', '未开始')  # 如果没有传递状态，默认设置为“未开始”
    else:
        # 新增任务
        task = Tasks(
            id=row_id,
            task_name=data.get('task_name'),
            video_source=data.get('video_source'),
            report_address=data.get('report_address'),
            algorithm_config=data.get('algorithm_config'),
            status='未开始'  # 新增任务的默认状态
        )
        db.session.add(task)
    
    db.session.commit()  # 保存到数据库
    return jsonify({"message": "任务保存成功"})

@app.route('/live_preview')
@login_required
def live_preview():
    cameras = [
        {'id': '01', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '02', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '03', 'status': '离线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '04', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
    ]
    return render_template('live_preview.html', cameras=cameras)

# 全局变量，用于存储当前正在播放的视频流地址
current_streams = {}

# 根据给定的视频流地址生成视频帧
def generate_frames(video_url):
    cap = cv2.VideoCapture(video_url)
    while True:
        success, frame = cap.read()
        time.sleep(0.020)
        if not success:
            time.sleep(0.002)
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    cap.release()

@app.route('/video/<nine_grid_id>')
@login_required
def video(nine_grid_id):
    video_url = current_streams.get(nine_grid_id)
    if video_url:
        return Response(generate_frames(video_url), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Video stream not found", 404

@app.route('/nine_tables')
@login_required
def nine_tables():
    cameras = [
        {'id': '01', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '02', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '03', 'status': '离线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '04', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
    ]
    return render_template('nine_tables.html', cameras=cameras)

@app.route('/alarm_management')
@login_required
def alarm_management():
    alarms = [
        {
            'id': '06',
            'video_channel': '02',
            'alarm_date': '2024-07-09 10:03:33',
            'report_address': 'http://192.168.1.106:5201/receive',
            'report_status': '上传失败',
            'alarm_content': '未佩戴口罩',
            'image_url': 'path_to_image1.jpg'
        },
        {
            'id': '06',
            'video_channel': '02',
            'alarm_date': '2024-07-09 09:35:06',
            'report_address': 'http://192.168.1.106:5201/receive',
            'report_status': '上传失败',
            'alarm_content': '未佩戴口罩',
            'image_url': 'path_to_image2.jpg'
        },
        {
            'id': '06',
            'video_channel': '02',
            'alarm_date': '2024-07-09 09:33:36',
            'report_address': 'http://192.168.1.106:5201/receive',
            'report_status': '上传失败',
            'alarm_content': '未佩戴口罩',
            'image_url': 'path_to_image3.jpg'
        }
    ]
    return render_template('alarm_management.html', alarms=alarms)

@app.route('/submit_channels', methods=['POST'])
def submit_channels():
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效数据'}), 400

    for channel in data:
        channel_number = channel.get('channelNumber')
        camera_name = channel.get('cameraName')
        video_url = channel.get('videoUrl')
        status = channel.get('status')

        existing_channel = Channel.query.get(channel_number)

        if existing_channel:
            existing_channel.camera_name = camera_name
            existing_channel.video_url = video_url
            existing_channel.status = status
        else:
            new_channel = Channel(
                channel_number=channel_number,
                camera_name=camera_name,
                video_url=video_url,
                status=status
            )
            db.session.add(new_channel)

    try:
        db.session.commit()
        return jsonify({'message': '数据提交成功！'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 保留原有的 SSH 逻辑代码并运行
def run_ssh_main():
    ssh_main()

def run_flask_app():
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 创建所有数据库表

    p2 = Process(target=run_flask_app)
    p2.start()
    p2.join()
