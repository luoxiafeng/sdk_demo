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


if __name__ == '__main__':
    app.run(debug=True)
