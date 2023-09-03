import httpx
import logging
from sqlalchemy.orm import Session
from NotificationService.schemas import Notification
from NotificationService.models import Subscription
from NotificationService.crud import list_subscriptions

logger = logging.getLogger()


class Notificator:
    def __init__(self, notification: Notification, db: Session):
        self.__notification = notification
        self.__db = db
        self.__subscribers = []

    def get_subscribers(self) -> [Subscription]:
        self.__subscribers = list_subscriptions(self.__db,
                                                app_name=self.__notification.app_name,
                                                event=self.__notification.event)
        return self.__subscribers

    async def notify_to_subscribers(self):
        errors = []
        for x in self.__subscribers:
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(x.callback_url, json=self.__notification.dict(), timeout=5)
            except Exception as e:
                errors.append({
                    'exception': repr(e),
                    'callback_url': x.callback_url
                })
                logger.error(f'exception: {e} at subscription {x.id}')
