from __future__ import absolute_import, unicode_literals

from prac_celery.celery import app

from mailing.pigeon import Pigeon


@app.task
def send_mail(to: str, message: str, subject: str, transfer_id: str):
    """Async email sending"""

    Pigeon(
        to=to,
        message=message,
        subject=subject,
        transfer_id=transfer_id,
    )()