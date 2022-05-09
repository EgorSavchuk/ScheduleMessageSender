import time
import vk_api
import pytz
from pprint import pformat as pf
from datetime import datetime
from vk_api.utils import get_random_id


class ScheduleMessageSender:

    msc = pytz.timezone('Europe/Moscow')

    CNT = 0
    ADMIN_MESSAGE = 'ScheduleMessageSender: Сообщений отправлено {count}/{all}'

    @staticmethod
    def auth_handler():
        key = input("Enter authentication code: ")
        remember_device = False
        return key, remember_device

    def __init__(self, login, password, chat_id, messages, logging=False, log_send=None):
        self.login = login
        self.password = password
        self.chat_id = chat_id
        self.messages = messages
        self.logging = logging
        self.log_send = log_send
        vk_session = vk_api.VkApi(self.login, self.password, auth_handler=self.auth_handler, app_id=2685278)

        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

        self.vk = vk_session.get_api()

    def start(self):
        while True:
            now = datetime.strftime(datetime.now(self.msc), '%H:%M')
            for key, value in self.messages.items():
                if value == now:
                    self.vk.messages.send(user_id=self.chat_id, message=key, random_id=get_random_id())
                    self.messages[key] = 'Отправлено'
                    self.CNT += 1
                    if self.log_send is not None:
                        self.vk.messages.send(user_id=self.log_send,
                                              message=self.ADMIN_MESSAGE.format(count=self.CNT, all=len(self.messages)),
                                              random_id=get_random_id())
            if self.logging:
                log = open('log', 'w')
                log.write(pf(self.messages, sort_dicts=False))
            time.sleep(10)
