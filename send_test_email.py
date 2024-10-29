

import os
import django
import ssl
from django.core.mail import EmailMessage
from django.core.mail import get_connection

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portalHrd.settings')
django.setup()

# Create a context that ignores certificate verification
context = ssl._create_unverified_context()

# Email configuration
subject = 'Test Email'
message = 'This is a test email.'
from_email = 'training_YPMI@yamaha-motor.co.id'
recipient_list = ['boby_ypmi@yamaha-motor.co.id']

# Create the email message
email = EmailMessage(subject, message, from_email, recipient_list)

try:
    # Get the email connection
    connection = get_connection()
    connection.open()  # Establish the connection
    email.connection = connection  # Set the connection for the email object

    # Send the email
    email.send(fail_silently=False)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    if 'connection' in locals():
        connection.close()  # Close the connection if it was opened
