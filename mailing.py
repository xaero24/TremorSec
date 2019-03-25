import smtplib, ssl

def sender(verificationCode):
    sender_email = "tremorsec@gmail.com"  # Enter your address
    receiver_email = "michaelafu@gmail.com"  # Enter receiver address
    password = "`1234qwert"
    message = """\
    Your TremorSec verification code

    Hello there!
    This is an automatic message from TremorSec.
    Your verification code is: """ + str(verificationCode) + """\

    Please enter the code in the application.

    For any questions, feel free to contact us at:
    tremorsec@gmail.com

    Regards,
    TremorSec team."""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
