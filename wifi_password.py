import os
from fpdf import FPDF

def get_wifi_passwords():
    """Retrieve all Wi-Fi profiles, their passwords, and security type."""
    wifi_details = []
    
    # Get list of Wi-Fi profiles
    profiles_output = os.popen("netsh wlan show profiles").read()
    
    for line in profiles_output.splitlines():
        if "All User Profile" in line:
            # Extract profile name
            profile_name = line.split(":")[1].strip()
            security_type = ""
            password = "None"
            
            # Get profile details for each profile
            profile_info_output = os.popen(f"netsh wlan show profile \"{profile_name}\" key=clear").read()
            
            for line in profile_info_output.splitlines():
                if "Authentication" in line:
                    # Extract security type (authentication method)
                    security_type = line.split(":")[1].strip()
                if "Key Content" in line:
                    # Extract password
                    password = line.split(":")[1].strip()
                    break
            
            wifi_details.append((security_type, profile_name, password))
    
    return wifi_details

def create_pdf(wifi_details, filename="wifi_passwords.pdf"):
    """Create a PDF document with the Wi-Fi details in a table format."""
    # Define the path to save the PDF on the user's Desktop
    user_desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    pdf_output_path = os.path.join(user_desktop, filename)
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add title
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, "Wi-Fi Passwords", ln=True, align='C')
    pdf.ln(10)

    # Add table headers
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(60, 10, "Security Type", border=1, align='C')
    pdf.cell(60, 10, "SSID", border=1, align='C')
    pdf.cell(60, 10, "Password", border=1, align='C')
    pdf.ln(10)  # Line break
    
    # Add Wi-Fi details in rows
    pdf.set_font("Arial", size=12)
    for security_type, profile, password in wifi_details:
        pdf.cell(60, 10, security_type, border=1, align='C')
        pdf.cell(60, 10, profile, border=1, align='C')
        pdf.cell(60, 10, password, border=1, align='C')
        pdf.ln(10)  # Line break after each row
    
    # Save PDF to the Desktop
    pdf.output(pdf_output_path)
    print(f"Wi-Fi passwords saved to '{pdf_output_path}'.")

if __name__ == "__main__":
    try:
        wifi_details = get_wifi_passwords()
        if wifi_details:
            create_pdf(wifi_details)
        else:
            print("No Wi-Fi profiles found.")
    except Exception as e:
        print(f"An error occurred: {e}")
