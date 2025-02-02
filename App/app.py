from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import json
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper function to load users from JSON file
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            users = json.load(f)
        return users
    else:
        return {}

# Helper function to save users to JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

# Route for main page with navigation
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/About')
def About():
    return render_template('About.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        
        if username in users and users[username]['password'] == password:
            flash('Login successful!', 'success')
            return redirect(url_for('data_form'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    
    return render_template('login.html')

# Route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            flash('All fields are required. Please fill out all fields.', 'error')
        elif password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
        else:
            users = load_users()
            if username in users:
                flash('Username already exists. Please choose a different one.', 'error')
            else:
                users[username] = {'email': email, 'password': password}
                save_users(users)
                flash('Signup successful! Please login.', 'success')
                return redirect(url_for('login'))
    
    return render_template('signup.html')

# Route to render the data entry form
@app.route('/data_form', methods=['GET'])
def data_form():
    return render_template('data_form.html')

# Function to process data files and generate anomaly report
def process_anomaly_detection(consumer_data, meter_status_data, historical_data):
    historical_data = pd.read_csv(historical_data)

    average_energy_by_consumer = historical_data.groupby('consumer_id')['energy_consumption'].mean().to_dict()
    std_dev_energy_by_consumer = historical_data.groupby('consumer_id')['energy_consumption'].std().to_dict()

    consumer_data = pd.read_csv(consumer_data)
    meter_status_data = pd.read_csv(meter_status_data)

    present_data = pd.merge(consumer_data, meter_status_data, on='consumer_id')

    threshold_factor = 3
    anomalies = []

    for index, row in present_data.iterrows():
        consumer_id = row['consumer_id']
        contact_info = row['contact_information']
        energy_usage = row['energy_consumption']
        meter_status = row['meter_status']

        if consumer_id in average_energy_by_consumer and consumer_id in std_dev_energy_by_consumer:
            average_energy = average_energy_by_consumer[consumer_id]
            std_dev_energy = std_dev_energy_by_consumer[consumer_id]
            
            difference = abs(energy_usage - average_energy)
            
            if meter_status.lower() in ['under maintenance', 'inactive']:
                issue = 'faulty_meter'
            else:
                issue = 'unauthorized_consumption'
            
            if difference > threshold_factor * std_dev_energy:
                anomaly_details = {
                    'anomalyid': len(anomalies) + 1,
                    'consumerid': consumer_id,
                    'contactinfo': contact_info,
                    'issue': issue
                }
                
                anomalies.append(anomaly_details)

    anomalies_json = json.dumps(anomalies, indent=4)

    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'anomalies_report.json'), 'w') as f:
        f.write(anomalies_json)

    html_report = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Anomaly Detection Report</title>
        <style>
            body { font-family: Arial, sans-serif; }
            h1, h2 { color: #2E4053; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #f2f2f2; text-align: left; }
        </style>
    </head>
    <body>
        <h1>Anomaly Detection Report</h1>
        <h2>Summary of Anomalies Detected</h2>
        <table>
            <thead>
                <tr>
                    <th>Anomaly Type</th>
                    <th>Count</th>
                </tr>
            </thead>
            <tbody>
    """

    anomaly_counts = {}
    for anomaly in anomalies:
        issue = anomaly['issue']
        if issue in anomaly_counts:
            anomaly_counts[issue] += 1
        else:
            anomaly_counts[issue] = 1

    for issue, count in anomaly_counts.items():
        html_report += f"""
        <tr>
            <td>{issue.replace('_', ' ').capitalize()}</td>
            <td>{count}</td>
        </tr>
        """

    html_report += """
            </tbody>
        </table>
        <h2>Detailed Anomaly Report</h2>
        <table>
            <thead>
                <tr>
                    <th>Anomaly ID</th>
                    <th>Consumer ID</th>
                    <th>Contact Info</th>
                    <th>Issue</th>
                </tr>
            </thead>
            <tbody>
    """

    for anomaly in anomalies:
        html_report += f"""
        <tr>
            <td>{anomaly['anomalyid']}</td>
            <td>{anomaly['consumerid']}</td>
            <td>{anomaly['contactinfo']}</td>
            <td>{anomaly['issue'].replace('_', ' ').capitalize()}</td>
        </tr>
        """

    html_report += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'anomalies_report.html'), 'w') as f:
        f.write(html_report)

# Route to process form submission
@app.route('/process_data', methods=['POST'])
def process_data():
    if request.method == 'POST':
        consumer_data = request.files['consumer_data']
        meter_data = request.files['meter_data']
        historical_data = request.files['historical_data']

        consumer_data_path = os.path.join(app.config['UPLOAD_FOLDER'], consumer_data.filename)
        meter_data_path = os.path.join(app.config['UPLOAD_FOLDER'], meter_data.filename)
        historical_data_path = os.path.join(app.config['UPLOAD_FOLDER'], historical_data.filename)

        consumer_data.save(consumer_data_path)
        meter_data.save(meter_data_path)
        historical_data.save(historical_data_path)

        # Process the uploaded data
        process_anomaly_detection(consumer_data_path, meter_data_path, historical_data_path)

        flash('Data received and processed successfully!', 'success')
        return redirect(url_for('show_report'))

# Route to show the report
@app.route('/show_report')
def show_report():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'anomalies_report.html')

if __name__ == '__main__':
    app.run(debug=True)
