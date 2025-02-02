# Anomaly Detection in Electricity

## Overview
Anomaly Detection in Electricity is a web application built using Flask that detects anomalies in electricity consumption data. Users can upload consumer, meter status, and historical data files, and the system will analyze them to identify potential unauthorized consumption or faulty meters.

## Features
- **User Authentication**: Signup and login functionality with user data stored in a JSON file.
- **File Upload System**: Users can upload CSV files containing consumer data, meter status, and historical energy usage.
- **Anomaly Detection**: Identifies anomalies based on deviations from historical consumption patterns.
- **HTML Report Generation**: Generates a detailed report summarizing the detected anomalies.
- **Flask-Based Web Interface**: Simple navigation for data submission and report viewing.

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (via Jinja templates)
- **Data Processing**: Pandas (Python)
- **Storage**: JSON files for user data
- **Deployment**: Localhost via Flask

## Installation
### Prerequisites
Ensure you have Python installed (preferably Python 3.7+).

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/umeshteja16/Anomaly-Detection-in-Electricity.git
   cd Anomaly-Detection-in-Electricity
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python app.py
   ```
4. Open the web application in your browser at:
   ```
   http://127.0.0.1:5000/
   ```

## Usage
1. **Sign Up**: Create a new user account.
2. **Login**: Enter your credentials to access the system.
3. **Upload Data**: Navigate to the data upload form and submit `consumer.csv`, `meterstatus.csv`, and `historical_data.csv`.
4. **Process Data**: The system analyzes the uploaded files and detects anomalies.
5. **View Report**: Access the generated HTML report summarizing anomalies.

## File Structure
```
Anomaly-Detection-in-Electricity/
│
├── uploads/                    # Directory for storing uploaded files & reports
├── templates/                   # HTML templates for rendering pages
│   ├── index.html               # Home page
│   ├── login.html               # Login page
│   ├── signup.html              # Signup page
│   ├── data_form.html           # Form for uploading data files
├── app.py                        # Main Flask application
├── users.json                    # Stores registered users
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
```

## Data Format
The CSV files should follow these formats:
### consumer.csv
```
consumer_id,contact_information,energy_consumption
1,John Doe,500
2,Jane Smith,750
```
### meterstatus.csv
```
consumer_id,meter_status
1,active
2,under maintenance
```
### historical_data.csv
```
consumer_id,energy_consumption
1,450
1,470
2,700
2,710
```

## License
This project is licensed under the MIT License.

## Contributing
Pull requests are welcome! Please ensure any modifications align with the project's structure and goals.

## Contact
For any queries or contributions, feel free to contact: [umeshteja270087@gmail.com].

