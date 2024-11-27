# Headache Logger

A web-based application for tracking and analyzing headache experiences with detailed logging capabilities. 

Do you suffer from headaches like I do? This project is designed to help you log your headache experiences, track patterns, and gain insights into your headache patterns. Whether you're a patient or a healthcare professional, this app provides a user-friendly interface to capture and manage headache logs. You can analyze your headache patterns and make informed decisions about your well-being.

<p align="center">
  <img src="assets/demo.png" width="400" alt="Headache Logger Demo">
</p>

## Features

- Log headache experiences with:
  - Required fields: duration, severity (1-10), and location
  - Optional fields: triggers (food/drink, stress, sleep), weather conditions, screen time, menstrual cycle information, symptoms, and medication details
- View and manage previous headache logs
- Delete individual logs
- Export logs to CSV for further analysis
- Responsive design that works on both desktop and mobile
- User-friendly interface with clear feedback messages

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/headache-logger.git
cd headache-logger
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Start logging your headaches!

## Tech Stack

- Backend: Flask (Python web framework)
- Database: SQLAlchemy with SQLite
- Frontend: HTML, CSS (Bootstrap), JavaScript
- Dependencies: See requirements.txt

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Improvements

- User authentication
- Data visualization
- Advanced filtering and reporting
- Mobile app version
- Data backup and restore
- Multi-language support
