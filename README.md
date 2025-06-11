⚽ FC 25 Player Analytics Dashboard
A comprehensive Streamlit web application for analyzing FIFA 25 player data with interactive visualizations, advanced filtering, and detailed player comparisons.

![image](https://github.com/user-attachments/assets/2c2a8c3a-c8bd-4166-94fa-4f0609f34cc5)


🌟 Features
📊 Overview Analytics

Real-time player statistics and metrics
Top players visualization by overall rating
Position and nationality distribution charts
Interactive attribute analysis with histograms

⚔️ Player Comparison
![image](https://github.com/user-attachments/assets/889be3a9-a2be-4bd6-a356-7b04b5b22733)


Head-to-head player comparisons
Radar chart visualizations for attribute analysis
Side-by-side detailed statistics
Visual performance comparisons

🧤 Goalkeeper Analysis

![image](https://github.com/user-attachments/assets/74f49bc0-3cfc-403e-8dd2-da9dce2d4002)


Specialized goalkeeper statistics
GK-specific attribute analysis
Top performer rankings
Comprehensive goalkeeper data tables

📈 Advanced Analytics
![image](https://github.com/user-attachments/assets/df6f10e1-d6be-43d0-bb68-86755a06e9e0)


Age vs Overall rating correlations
Attribute correlation heatmaps
Team performance analysis
Statistical insights and trends

🔍 Player Search

![image](https://github.com/user-attachments/assets/3a729c1d-7019-4b1c-902b-64baab1a0e7b)


Advanced search with multiple criteria
Individual player detailed profiles
Customizable data display
Export functionality

🚀 Quick Start
Prerequisites

Python 3.8 or higher
pip package manager

Installation

Clone the repository
bashgit clone https://github.com/ziadtarekmohamed/FC-25-Player-Dashboard
cd fc25-player-dashboard

Create a virtual environment 
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install required packages
bashpip install -r requirements.txt

Prepare your data

Place your all_players.csv file in the data/ directory
Update the file path in app.py if needed


Run the application
bashstreamlit run app.py

Open in browser

Navigate to http://localhost:8501




📊 Data Requirements
The dashboard expects a CSV file with the following columns:
Required Columns

Name - Player name
OVR - Overall rating
Position - Player position
Team - Current team
Nation - Player nationality

Optional Columns

Age - Player age
PAC, SHO, PAS, DRI, DEF, PHY - Main attributes
GK Diving, GK Handling, GK Kicking, GK Positioning, GK Reflexes - Goalkeeper stats
Height, Weight - Physical attributes
Plus many more detailed statistics...

🎮 Usage
1. Filtering Data

Use the sidebar filters to narrow down players
Search by name, position, team, or nationality
Set age and overall rating ranges

2. Exploring Analytics

Navigate through different tabs for various analyses
Interact with charts and visualizations
Hover over data points for detailed information

3. Comparing Players

Select two players in the comparison tab
View radar charts and detailed comparisons
Analyze strengths and weaknesses

4. Exporting Data

Download filtered results as CSV
Save customized player lists
Export visualizations (browser screenshot)

🛠️ Customization
Adding New Features

Fork the repository
Create a feature branch: git checkout -b feature-name
Make your changes
Test thoroughly
Submit a pull request

Modifying Visualizations

Edit the Plotly chart configurations in app.py
Add new chart types in the respective tab sections
Customize colors and themes in the CSS section

📈 Screenshots
Main Dashboard
Show Image
Player Comparison
Show Image
Analytics
Show Image
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.
Development Setup

Fork the project
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

📋 Requirements
See requirements.txt for full dependency list. Key packages include:

streamlit>=1.28.0 - Web app framework
pandas>=2.0.0 - Data manipulation
plotly>=5.15.0 - Interactive visualizations
numpy>=1.24.0 - Numerical computing

🐛 Troubleshooting
Common Issues
Data Loading Error

Ensure CSV file path is correct
Check CSV file format and encoding
Verify required columns exist

Performance Issues

Large datasets may load slowly
Consider filtering data before analysis
Close unused browser tabs

Visualization Problems

Update browser to latest version
Clear browser cache
Check JavaScript is enabled

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

FIFA 25 data provided by EA Sports
Built with Streamlit
Visualizations powered by Plotly
Data analysis with Pandas

📞 Support
If you encounter any issues or have questions:

Check the Issues page
Create a new issue with detailed description
Contact: [ziadtarekmoh22@gmail.com]

🔄 Version History

v1.0.0 - Initial release with basic functionality
v1.1.0 - Added player comparison and advanced analytics
v1.2.0 - Enhanced UI/UX and goalkeeper analysis


⭐ Star this repository if you found it helpful!
