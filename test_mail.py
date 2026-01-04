import smtplib
import os

# Manual settings for testing
email = "pawangahane02@gmail.com"
password = "sdkb cpde wjro oxuf".replace(" ", "")

print(f"Testing login for: {email}")
print(f"Using password: {password[:2]}****{password[-2:]}")

def test_smtp(port, use_ssl=False):
    print(f"\n--- TESTING PORT {port} ({'SSL' if use_ssl else 'STARTTLS'}) ---")
    try:
        if use_ssl:
            server = smtplib.SMTP_SSL('smtp.gmail.com', port)
        else:
            server = smtplib.SMTP('smtp.gmail.com', port)
            server.starttls()
        
        server.set_debuglevel(1)
        print(f"Authenticating as {email}...")
        server.login(email, password)
        print("\n" + "="*40)
        print(f"SUCCESS: Login worked on port {port}!")
        print("="*40)
        server.quit()
        return True
    except Exception as e:
        print(f"\nFAILED on port {port}: {e}")
        return False

print(f"Testing for: {email}")
print(f"Using password: {password[:2]}****{password[-2:]}")

if not test_smtp(587, False):
    test_smtp(465, True)

print("\nIf both failed, please ensure:")
print("1. 2-Step Verification is ON.")
print("2. You are using a 16-character App Password.")
print(f"3. The password belongs to {email}")

