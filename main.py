from flask import Flask, render_template, request, jsonify
import random
import requests
import threading  # Import threading for timer

app = Flask(__name__)

ESP32_IP = "http://192.168.225.11"  # Change this to ESP32's actual IP
otp = None
status = "LOCKED"
failed_attempts = 0
lockdown_mode = False
ADMIN_PASSWORD = "admin123"  # You can change this password as needed

# Function to lock the system after 15 seconds
def lock_system():
    global status
    status = "LOCKED"
    requests.post(f"{ESP32_IP}/update_otp", data={"status": "LOCKED"})  # Notify ESP32
    print("Status changed to LOCKED after 15 seconds")  # Debugging

@app.route('/generate_otp', methods=['POST'])
def generate_otp():
    global otp, failed_attempts
    otp = random.randint(1000, 9999)
    failed_attempts = 0
    print(f"Generated OTP: {otp}")
    return jsonify({'otp': otp, 'status': status})

@app.route('/lock_system', methods=['POST'])
def lock_system_route():
    global status
    status = "LOCKED"
    return jsonify({'status': status})

@app.route('/validate_otp', methods=['POST'])
def validate_otp():
    global otp, status, failed_attempts, lockdown_mode

    if lockdown_mode:
        return jsonify({'success': False, 'status': "LOCKDOWN", 'message': "System is locked. Enter admin password."}), 403

    entered_otp = request.form.get('otp')
    if not entered_otp:
        return jsonify({'success': False, 'message': "OTP is required"}), 400

    try:
        entered_otp = int(entered_otp)
    except ValueError:
        return jsonify({'success': False, 'message': "Invalid OTP format"}), 400

    if otp and entered_otp == otp:
        status = "UNLOCKED"
        otp = None
        failed_attempts = 0
        requests.post(f"{ESP32_IP}/update_otp", data={"status": "UNLOCKED"})
        threading.Timer(15, lock_system).start()
        return jsonify({'success': True, 'status': status, 'message': "Access granted"}), 200
    else:
        failed_attempts += 1
        if failed_attempts >= 3:
            lockdown_mode = True
            requests.get(f"{ESP32_IP}/call")
            return jsonify({'success': False, 'status': "LOCKDOWN", 'message': "Too many failed attempts"}), 403
        return jsonify({'success': False, 'status': status, 'message': "Incorrect OTP"}), 401

@app.route('/get_status', methods=['GET'])
def get_status():
    return jsonify({'status': status, 'otp': otp, 'lockdown': lockdown_mode})

@app.route('/update_status', methods=['POST'])
def update_status():
    global status
    status = request.form.get('status', "LOCKED")
    return jsonify({'message': 'Status updated', 'status': status})

@app.route('/')
def index():
    return render_template('index.html', status=status)

# ✅ Only ONE password route
@app.route('/verify_password', methods=['POST'])
def verify_password():
    global lockdown_mode, failed_attempts
    entered_password = request.form.get('password')

    if entered_password == ADMIN_PASSWORD:
        lockdown_mode = False
        failed_attempts = 0
        return jsonify({'success': True, 'message': 'Password accepted. You can now enter the OTP again.'})
    else:
        return jsonify({'success': False, 'message': 'Incorrect password. Try again.'})

# 🔚 Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
