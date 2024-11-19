import csv
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

class Command(BaseCommand):
    help = "Send bulk emails with personalized messages from a CSV file."

    def handle(self, *args, **kwargs):
        csv_file_path = r"C:\inetpub\wwwroot\NewStructure\user1.csv" 

        try:
            # Membaca CSV
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')

                # Menangani BOM jika ada pada header
                if '\ufeffemail' in reader.fieldnames:
                    reader.fieldnames = [fieldname.lstrip('\ufeff') for fieldname in reader.fieldnames]

                for row in reader:
                    email = row.get('email')
                    username = row.get('username')
                    password = row.get('password')

                    # Validasi data
                    if not email or not username or not password:
                        self.stdout.write(self.style.ERROR(f"Invalid data: {row}"))
                        continue

                    # Persiapkan konten email
                    subject = "Portal HRD Login Credentials"
                    
                    # Pesan HTML
                    html_message = f"""
                        <html>
                            <body>
                                <p>Assalamualaikum,</p>
                                <p>Semangat pagi</p>
                                <p>Berikut saya kirimkan Username & Password untuk login portal HRD:</p>
                                <ul>
                                    <li><strong>Username:</strong> {username}</li>
                                    <li><strong>Password:</strong> {password}</li>
                                </ul>
                                <p>Akses dengan link berikut: <a href="http://172.20.40.153:8001/user/login/" target="_blank">User Login</a></p>
                                <p>Terimakasih atas perhatiannya.<br>Semoga sehat selalu</p>
                                <p>Human Resources<br>
                                Training And Development<br>
                                252/257<br>
                                PT. YAMAHA MOTOR PARTS MANUFACTURING INDONESIA<br>
                                Karawang-Jawa Barat</p>
                            </body>
                        </html>
                    """

                    # Pesan teks biasa (untuk fallback)
                    text_message = (
                        f"Assalamualaikum,\n\n"
                        f"Semangat pagi\n\n"
                        f"Berikut saya kirimkan Username & Password untuk login portal HRD\n\n"
                        f"Username           : {username}\n"
                        f"Password           : {password}\n\n"
                        f"Akses dengan link berikut: User Login\n\n"
                        f"Terimakasih atas perhatiannya.\n"
                        f"Semoga sehat selalu\n\n"
                        f"Human Resources\n"
                        f"Training And Development\n"
                        f"252/257\n"
                        f"PT. YAMAHA MOTOR PARTS MANUFACTURING INDONESIA\n"
                        f"Karawang-Jawa Barat"
                    )

                    # Menggunakan alamat pengirim dari settings.py
                    from_email = settings.DEFAULT_FROM_EMAIL

                    # Kirim email
                    try:
                        # Mengirim email dengan alternatif HTML
                        email_message = EmailMultiAlternatives(
                            subject=subject,
                            body=text_message,  # Teks biasa untuk fallback
                            from_email=from_email,
                            to=[email],
                        )
                        email_message.attach_alternative(html_message, "text/html")  # Attach HTML version
                        email_message.send()
                        self.stdout.write(self.style.SUCCESS(f"Email sent to: {email}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Failed to send email to {email}: {e}"))

            self.stdout.write(self.style.SUCCESS("All emails processed successfully."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"CSV file not found at path: {csv_file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
