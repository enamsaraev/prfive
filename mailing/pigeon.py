from dataclasses import dataclass

from django.conf import settings
from django.core.mail import send_mail

from core.models import Account
from api.models import EmailEntry


@dataclass
class Pigeon:
    to: str
    message: str
    subject: str
    transfer_id: str


    def __call__(self) -> None:
        """Send email when initialize"""

        if self.__is_sent_already():
            return

        self.__msg()
        self.__write_email_log()

        return True

    def __msg(self) -> None:
        """Sending email"""

        send_mail(
            subject= self.subject,
            message=self.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.to],
        )

    def __write_email_log(self) -> None:
        """Logging sent email"""

        EmailEntry.objects.update_or_create(
            user=Account.objects.get(email=self.to),
            text=self.message,
            msg_number=self.transfer_id
        )

    def __is_sent_already(self) -> bool:
        """Check if mail is already sent"""
        
        return EmailEntry.objects.filter(
            user=Account.objects.get(email=self.to), 
            text=self.message,
            msg_number=self.transfer_id
        ).exists()
    
