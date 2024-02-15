import os

import yagmail
from helpers import constants
from logger import wbm_logger

__appname__ = os.path.splitext(os.path.basename(__file__))[0]
color_me = wbm_logger.ColoredLogger(__appname__)
LOG = color_me.create_logger()


def send_email_notification(
    email: str, subject: str, body: str, attachment: str = None
):
    """Send email notification with optional attachment.

    Args:
        email (str): Sender's email address.
        subject (str): Email subject.
        body (str): Email body.
        attachment (str, optional): Path to the attachment file. Defaults to None.
    """

    if not constants.email_password:
        LOG.warning(
            color_me.yellow(
                f"E-mail password not found in the ENV variables! I will not be able to send you e-mails."
            )
        )
        return

    try:
        # Initialize yagmail SMTP connection
        yag = yagmail.SMTP(
            email,
            constants.email_password,
            smtp_starttls=True,
            smtp_ssl=False,
            smtp_skip_login=False,
            host="smtp-mail.outlook.com",
            port=587,
        )

        # Send email with attachment if provided
        if attachment:
            yag.send(to=email, subject=subject, contents=body, attachments=attachment)
        else:
            yag.send(to=email, subject=subject, contents=body)

        LOG.info(color_me.green(f"Email notification sent successfully to '{email}'"))
    except Exception as e:
        LOG.error(
            color_me.red(f"Failed to send email notification to '{email}' | {str(e)}")
        )
