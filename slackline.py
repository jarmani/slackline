from inspect import getargspec
from time import sleep
from slackclient import SlackClient


class SlackLine(object):

    def __init__(self, token):
        self.client = SlackClient(token)

    def send_message(self, channel, message):
        self.client.rtm_send_message(channel, message)

    def send_attachments(self, channel, attachments):
        self.client.api_call('chat.postMessage',
                             channel=channel,
                             attachments=attachments,
                             as_user=True)

    def answer(self, message='', attachments=None):
        if attachments:
            self.send_attachments(self.channel, attachments)
        else:
            self.send_message(self.channel, message)

    def help(self, cmdname, func):
        command = self.command_prefix + cmdname
        if not func:
            return 'Command *%s* does not exist' % command
        doc = getattr(func, '__doc__')

        if not doc:
            return 'Command *%s* exists but not documented' % command

        # Remove left spaces and parse {command}
        doc = '\n'.join([line.lstrip() for line in doc.split('\n')])
        return doc.format(command=self.command_prefix + cmdname)

    def cmd_help(self, cmdname):
        """
            *{command}* <name> : *Return help for command <name>*
            ex : {command} help
        """
        command = getattr(self, 'cmd_' + cmdname, None)
        self.answer(self.help(cmdname, command))

    # XXX Should be done during init not at runtime
    def parse_command(self, channel, message):
        args = message[1:].split(' ')
        self.channel = channel
        command = getattr(self, 'cmd_' + args[0], None)

        if command and callable(command):
            expected = getargspec(command)
            provided = args[1:]

            if expected.varargs:
                command(*provided)
                return

            # remove self from count
            expected_count = len(expected.args) - 1
            default_count = expected.defaults and len(expected.defaults) or 0
            required_count = expected_count - default_count

            if (len(provided) >= required_count
                    and len(provided) <= expected_count):
                command(*provided)
                return

        self.answer(self.help(args[0], command))

    def ready(self):
        print('Bot ready')

    def run(self):

        if not self.client.rtm_connect():
            print('Error connecting')
            return

        while True:

            messages = self.client.rtm_read()

            for message in messages:

                type = message.get('type')

                if type == 'hello':
                    self.ready()
                elif type == 'message':
                    channel = message.get('channel')
                    text = message.get('text', '')

                    if len(text) > 1 and text[0] == self.command_prefix:
                        self.parse_command(channel, text)

            sleep(.5)
