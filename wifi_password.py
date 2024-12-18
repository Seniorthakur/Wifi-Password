import subprocess
import os
from fpdf import FPDF

# Function to retrieve WiFi profiles and passwords
def get_wifi_profiles():
    profiles = []
    try:
        # Run the command to get all WiFi profiles on Windows
        command = "netsh wlan show profiles"
        result = subprocess.check_output(command, shell=True, encoding="utf-8")

        # Extract the SSID (WiFi names) from the command output
        profile_names = [line.split(":")[1][1:-1] for line in result.split("\n") if "All User Profile" in line]

        # Get details for each profile
        for profile_name in profile_names:
            profile_info = {"SSID": profile_name}
            profile_details = subprocess.check_output(f"netsh wlan show profile {profile_name} key=clear", shell=True, encoding="utf-8")
            
            # Extract security type
            for line in profile_details.split("\n"):
                if "Security key" in line:
                    profile_info["Security Type"] = line.split(":")[1][1:-1]
                if "Key Content" in line:
                    profile_info["Password"] = line.split(":")[1][1:-1]
                    
            profiles.append(profile_info)
    except subprocess.CalledProcessError:
        print("An error occurred while retrieving WiFi profiles.")
    
    return profiles

# Function to create a PDF file with WiFi details
def create_pdf(profiles, filename):
    # Define the path to the Downloads folder
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set title
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt="WiFi Profile Report", ln=True, align="C")

    # Set content font
    pdf.set_font("Arial", size=12)

    # Add WiFi profile information to the PDF
    for profile in profiles:
        pdf.ln(10)  # Line break
        pdf.cell(200, 10, txt=f"WiFi Profile: {profile['SSID']}", ln=True)
        pdf.cell(200, 10, txt=f"SSID: {profile['SSID']}", ln=True)
        pdf.cell(200, 10, txt=f"Security Type: {profile['Security Type']}", ln=True)
        pdf.cell(200, 10, txt=f"Password: {profile.get('Password', 'Not available')}", ln=True)

    # Save the PDF to the Downloads folder
    pdf_output_path = os.path.join(download_folder, filename)
    pdf.output(pdf_output_path)
    print(f"WiFi profile report saved to {pdf_output_path}")

if __name__ == "__main__":
    # Get WiFi profiles and their details
    wifi_profiles = get_wifi_profiles()

    if wifi_profiles:
        # Create and save PDF in Downloads folder
        create_pdf(wifi_profiles, "wifi_profiles_report.pdf")
    else:
        print("No WiFi profiles found.")
