import os
from fpdf import FPDF

def get_wifi_passwords():
    """Retrieve all Wi-Fi profiles and their passwords."""
    wifi_details = []
    # Get list of Wi-Fi profiles
    profiles_output = os.popen("netsh wlan show profiles").read()
    
    for line in profiles_output.splitlines():
        if "All User Profile" in line:
            # Extract profile name
            profile_name = line.split(":")[1].strip()
            # Get password details for each profile
            profile_info_output = os.popen(f"netsh wlan show profile \"{profile_name}\" key=clear").read()
            for line in profile_info_output.splitlines():
                if "Key Content" in line:
                    # Extract password
                    password = line.split(":")[1].strip()
                    break
            else:
                password = "None"
            wifi_details.append((profile_name, password))
    return wifi_details

def create_pdf(wifi_details, filename="wifi_passwords.pdf"):
    """Create a PDF document with the Wi-Fi details."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add title
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, "Wi-Fi Passwords", ln=True, align='C')
    pdf.ln(10)

    # Add Wi-Fi details
    pdf.set_font("Arial", size=12)
    for i, (profile, password) in enumerate(wifi_details, start=1):
        pdf.cell(200, 10, f"{i}. SSID: {profile} | Password: {password}", ln=True)
    
    # Save PDF
    pdf.output(filename)

if __name__ == "__main__":
    try:
        wifi_details = get_wifi_passwords()
        if wifi_details:
            create_pdf(wifi_details)
            print("Wi-Fi passwords saved to 'wifi_passwords.pdf'.")
        else:
            print("No Wi-Fi profiles found.")
    except Exception as e:
        print(f"An error occurred: {e}")
