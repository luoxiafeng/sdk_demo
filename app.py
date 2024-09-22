from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def dashboard():
    device_info = {
        'device_id': 'RJ-BMOX-000738FADB3FA8289232CA9F49C0329',
        'status': '已授权',
        'software_version': '0.0.54',
        'box_time': '2024-07-09 10:11:32',
        'storage_space': '10.8GB',
        'chip_temperature': '45 °C',
        'system_version': 'BM1684-16 2.7.0'
    }
    
    # Data for charts
    chart_data = {
        'timestamps': ['2024/7/9 10:11:16', '2024/7/9 10:11:21', '2024/7/9 10:11:26', '2024/7/9 10:11:31'],
        'cpu_usage': [5, 6, 6, 6],
        'tpu_usage': [50, 55, 55, 55],
        'chip_temp': [45, 45, 45, 45]
    }
    
    return render_template('dashboard.html', device_info=device_info, chart_data=chart_data)
@app.route('/channel_management')
def channel_management():
    channels = [
        {'camera_id': '005', 'video_url': 'rtsp://192.168.1.106:8554/test_stream', 'status': '连接视频失败', 'national_channel_id': '', 'operation': '编辑'},
        {'camera_id': '01', 'video_url': 'rtsp://admin:passw0rd@192.168.1.103:554/Streaming/Channels/101', 'status': '正常', 'national_channel_id': '', 'operation': '编辑'},
        {'camera_id': '02', 'video_url': 'rtsp://admin:passw0rd@192.168.1.103:554/Streaming/Channels/201', 'status': '正常', 'national_channel_id': '', 'operation': '编辑'},
        {'camera_id': '03', 'video_url': 'rtsp://admin:passw0rd@192.168.1.103:554/Streaming/Channels/301', 'status': '视频流不存在', 'national_channel_id': '', 'operation': '编辑'},
    ]
    
    return render_template('channel_management.html', channels=channels)

@app.route('/task_management')
def task_management():
    tasks = [
        {'task_id': '001', 'video_source': '02', 'report_address': '明烟明火检测, 口罩检测, 爬爬检测', 'algorithm_info': ['明烟明火检测', '口罩检测', '爬爬检测'], 'status': '未运行'},
        {'task_id': '002', 'video_source': '02', 'report_address': '安全帽检测, 反光衣检测, 未穿长袖检测', 'algorithm_info': ['安全帽检测', '反光衣检测', '未穿长袖检测'], 'status': '未运行'},
        {'task_id': '003', 'video_source': '02', 'report_address': '人员拥挤检测, 口罩检测, 反光衣检测', 'algorithm_info': ['人员拥挤检测', '口罩检测', '反光衣检测'], 'status': '未运行'},
        {'task_id': '004', 'video_source': '02', 'report_address': '脸部抓拍, 打架检测, 街道垃圾检测', 'algorithm_info': ['脸部抓拍', '打架检测', '街道垃圾检测'], 'status': '未运行'},
        {'task_id': '0045', 'video_source': '02', 'report_address': '越线检测, 安全帽检测, 反光衣检测', 'algorithm_info': ['越线检测', '安全帽检测', '反光衣检测'], 'status': '未运行'},
        {'task_id': '006', 'video_source': '02', 'report_address': '倒地检测V2, 安全帽检测V3', 'algorithm_info': ['倒地检测V2', '安全帽检测V3'], 'status': '未运行'},
    ]
    
    return render_template('task_management.html', tasks=tasks)

@app.route('/task_management/add', methods=['GET'])
def add_task():
    video_sources = [
        '02 - rtsp://admin:passw0rd@192.168.1.103:554/Streaming/Channels/201',
        '03 - rtsp://admin:passw0rd@192.168.1.104:554/Streaming/Channels/301'
    ]
    
    algorithms = [
        '明烟明火检测', '口罩检测', '攀爬检测', '人脸识别', '人体骨骼', '非机动车停车', '区域车停禁停', '车牌识别',
        '小动物检测', '人员拥挤检测', '人数超员检测', '人数监控(人体)', '离岗检测', '翻越围栏', '区域入侵',
        '越线检测', '街道垃圾检测', '打架检测', '电梯电动车检测', '安全帽检测', '反光衣检测', '未穿长袖检测',
        '工服检测', '工作安全带', '抽烟打电话检测', '驾驶员注意力分析', '倒地检测V2', '睡岗检测', '安全帽检测V3'
    ]
    
    return render_template('add_task.html', video_sources=video_sources, algorithms=algorithms)

@app.route('/live_preview')
def live_preview():
    cameras = [
        {'id': '01', 'status': '在线', 'video_url': 'rtsp://192.168.1.101:554/live'},
        {'id': '02', 'status': '在线', 'video_url': 'rtsp://192.168.1.102:554/live'},
        {'id': '03', 'status': '离线', 'video_url': 'rtsp://192.168.1.103:554/live'},
        {'id': '04', 'status': '在线', 'video_url': 'rtsp://192.168.1.104:554/live'},
    ]
    
    return render_template('live_preview.html', cameras=cameras)

if __name__ == '__main__':
    app.run(debug=True)
