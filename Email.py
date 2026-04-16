import time
import smtplib
import lgpio
from email.message import EmailMessage

# --- Configuration ---
# Email settings (163 Mail)
FROM_EMAIL = "m15995388582@163.com"
EMAIL_PASS = "XLaXve6eUBjwDMDY" # Replace with your 16-digit code
TO_EMAIL = "m15995388582@163.com"

# Hardware settings
SENSOR_PIN = 4 # GPIO 04
chip = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(chip, SENSOR_PIN)

# Tracking variables
last_email_hour = -1 # Initialize to -1 to trigger the first check immediately

def send_notification(status_text):
    """Function to send email via 163 SMTP server"""
    msg = EmailMessage()
    msg['Subject'] = 'Plant Moisture Report'
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    
    # Get current timestamp for the email body
    current_ts = time.strftime('%Y-%m-%d %H:%M:%S')
    body = f"Timestamp: {current_ts}\nStatus: {status_text}"
    msg.set_content(body)

    try:
        # Use SSL port 465 for 163.com
        with smtplib.SMTP_SSL('smtp.163.com', 465) as server:
            server.login(FROM_EMAIL, EMAIL_PASS)
            server.send_message(msg)
            print(f"Email sent successfully: {status_text}")
    except Exception as e:
        print(f"Failed to send email: {e}")

print("--- Raspberry Pi Plant Monitor Started ---")

try:
    while True:
        # IMPORTANT: Get fresh time inside the loop
        current_time = time.localtime()
        # Adjust hour if your Pi is set to UTC (e.g., +8 for Beijing Time)
        # If your Pi system time is already correct, just use current_time.tm_hour
        current_hour = current_time.tm_hour 

        # PDF Requirement: 4 daily readings (Every 6 hours)
        # Logic: If it's the first run OR 6 hours have passed OR the day has reset
        hour_diff = current_hour - last_email_hour
        
        # Handle the 24-hour reset (e.g., last was 22:00, now is 04:00)
        if hour_diff < 0:
            hour_diff += 24

        if last_email_hour == -1 or hour_diff >= 6:
            print(f"Time to check sensor (Hour: {current_hour})")
            
            # Read digital output from sensor
            # 0 usually means Moisture Detected (LED ON)
            # 1 usually means Dry (LED OFF)
            sensor_state = lgpio.gpio_read(chip, SENSOR_PIN)
            
            if sensor_state == 0:
                status = "Water NOT needed"
            else:
                status = "Please water your plant"
            
            # Send the email
            send_notification(status)
            
            # Update the last email hour
            last_email_hour = current_hour
        else:
            # Optional: Print status to console without sending email
            print(f"Waiting... Current Hour: {current_hour}. Next check in {6 - hour_diff} hours.", end="\r")

        # IMPORTANT: Sleep for 60 seconds to prevent 100% CPU usage
        time.sleep(60)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")
finally:
    lgpio.gpiochip_close(chip)

