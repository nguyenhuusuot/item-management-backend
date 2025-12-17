import time

def fake_send_email(email: str, message : str):
    time.sleep(5)
    print(f"Email sent to {email}: {message}")
