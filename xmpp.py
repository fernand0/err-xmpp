import sys
from errbot import BotPlugin, botcmd, webhook
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import logging
import asyncio
import argparse
import subprocess

_logger = logging.getLogger(__name__)


"""Example of using hangups to send a chat message to a conversation."""

import asyncio

import hangups

from common import run_example
from cliHangups import *

@asyncio.coroutine
def sendMessage(message):
    dirs = appdirs.AppDirs('hangups_cli', 'hangups_cli')
    default_log_path = os.path.join(dirs.user_data_dir, 'hangups.log')
    default_token_path = os.path.join(dirs.user_data_dir, 'refresh_token.txt')
    conversation_path = os.path.join(dirs.user_data_dir, 'conversation_list.txt')
    user_path = os.path.join(dirs.user_data_dir, 'user_list.txt')

    conversation_map = {}
    try:
        with open(conversation_path, 'r') as conv_file:
            for line in conv_file.readlines():
                split = line.split(':')
                key = split[1].strip().replace(" ", "_")
                value = split[0].strip()
                conversation_map[key] = value
    except FileNotFoundError as err:
        pass

    user_map = {}
    try:
        with open(user_path, 'r') as user_file:
            for line in user_file.readlines():
                split = line.split(':')
                key = split[1].strip().replace(" ", "_")
                value = split[0].strip()
                user_map[key] = value
    except FileNotFoundError as err:
        pass

    conversation_choices = sorted(list(conversation_map.keys()),
                                  key=lambda x:'zzz' + x if x[:7] == "Unknown" else x)
    user_choices = sorted(list(user_map.keys()),
                          key=lambda x:'zzz' + x if x[:7] == "Unknown" else x)

    command = []
    command.append('send')
    command.append(['conversation', conversation_map['fernand0movilizado_Bot']])
    command.append(['message', message])

    for path in ['', default_token_path, conversation_path, user_path]:
        directory = os.path.dirname(path)
        if directory and not os.path.isdir(directory):
            try:
                os.makedirs(directory)
            except OSError as err:
                sys.exit('Failed to create directory: {}'.format(err))

    # Setup logging
    log_level = logging.WARNING
    logging.basicConfig(filename='', level=log_level, format=LOG_FORMAT)
    # asyncio's debugging logs are VERY noisy, so adjust the log level
    logging.getLogger('asyncio').setLevel(logging.WARNING)

    unused_cli = Cli(default_token_path, conversation_path, user_path, command, '')

@asyncio.coroutine
def getMessage():
    dirs = appdirs.AppDirs('hangups_cli', 'hangups_cli')
    default_log_path = os.path.join(dirs.user_data_dir, 'hangups.log')
    default_token_path = os.path.join(dirs.user_data_dir, 'refresh_token.txt')
    conversation_path = os.path.join(dirs.user_data_dir, 'conversation_list.txt')
    user_path = os.path.join(dirs.user_data_dir, 'user_list.txt')

    conversation_map = {}
    try:
        with open(conversation_path, 'r') as conv_file:
            for line in conv_file.readlines():
                split = line.split(':')
                key = split[1].strip().replace(" ", "_")
                value = split[0].strip()
                conversation_map[key] = value
    except FileNotFoundError as err:
        pass

    user_map = {}
    try:
        with open(user_path, 'r') as user_file:
            for line in user_file.readlines():
                split = line.split(':')
                key = split[1].strip().replace(" ", "_")
                value = split[0].strip()
                user_map[key] = value
    except FileNotFoundError as err:
        pass

    conversation_choices = sorted(list(conversation_map.keys()),
                                  key=lambda x:'zzz' + x if x[:7] == "Unknown" else x)
    user_choices = sorted(list(user_map.keys()),
                          key=lambda x:'zzz' + x if x[:7] == "Unknown" else x)

    command = []
    command.append('get')
    command.append(['conversation', conversation_map['fernand0movilizado_Bot'], 5])

    for path in ['', default_token_path, conversation_path, user_path]:
        directory = os.path.dirname(path)
        if directory and not os.path.isdir(directory):
            try:
                os.makedirs(directory)
            except OSError as err:
                sys.exit('Failed to create directory: {}'.format(err))

    # Setup logging
    log_level = logging.WARNING
    logging.basicConfig(filename='', level=log_level, format=LOG_FORMAT)
    # asyncio's debugging logs are VERY noisy, so adjust the log level
    logging.getLogger('asyncio').setLevel(logging.WARNING)

    unused_cli = Cli(default_token_path, conversation_path, user_path, command, '')

class myXmppBridge(BotPlugin):
    """ 
    A plugin to send and receive messages with XMPP when you are using a
    differente backend
    """

    def get_configuration_template(self):
        '''
        Defines the configuration structure this plugin supports

        You should delete it if your plugin doesn't use any configuration like this
        '''
        return {'XMPP_BRIDGE_JID': 'user@example.com',
                'XMPP_BRIDGE_PASSWORD': 'password',
                'XMPP_BRIDGE_NICK': 'bridgebot',
                'XMPP_BRIDGE_HOST': 'conferenc.example.com'
               }

    def check_configuration(self, configuration):
        '''
        Triggers when the configuration is checked, shortly before activation

        Raise a errbot.utils.ValidationException in case of an error

        You should delete it if you're not using it to override any default behaviour
        '''
        super(myXmppBridge, self).check_configuration(configuration)

    def callback_mention(self, message, mentioned_people):
        for identifier in mentioned_people:
            self.forwardmessage(message.frm, 'User %s has been mentioned' % identifier)
        if self.bot_identifier in mentioned_people:
            yield('hola %s'%message.frm)
            self.forwardmessage(message.frm, 'Errbot has been mentioned !')

    @botcmd
    def fm(self, msg, args):
        yield(self.forwardmessage(msg, args))

    @botcmd(admin_only=True)
    def forwardmessage(self, msg, args):
        arg1='hangups_cli  send -c fernand0movilizado_Bot -m %s'%args
        arg2='hangups_cli  get -n 5 -c fernand0movilizado_Bot'
        p=subprocess.Popen(arg1,shell=True,stdout=subprocess.PIPE)
        data = p.communicate()
        # We need to wait. We need to select the adequate part of the reply
        p=subprocess.Popen(arg2,shell=True,stdout=subprocess.PIPE)
        data = p.communicate()[0].decode()
        yield(data)
        yield(args)
        yield(data[:data.find(args)])

    @botcmd(admin_only=True)
    def forwardmessage2(self, msg, args):
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #loop = asyncio.get_event_loop()
        #task = asyncio.Task(sendMessage(args))
        #try:
        #    loop.run_until_complete(task)
        #except KeyboardInterrupt:
        #    task.cancel()
        #    loop.run_forever()
        #finally:
        #    loop.close()
        sendMessage(args)
        yield("respuesta")
        getMessage()
        yield("fin")
 
        #hangupargs = argparse.Namespace()
        ## We need to be able to locate the conversation
        ## Arguments: (Namespace(conversation_id='UgybUd1gf4E4TwB5VVl4AaABAQ', debug=False, message_text='aeiou a e' , token_path='/home/debian/.cache/hangups/refresh_token.txt'),)
        #hangupargs.conversation_id='UgybUd1gf4E4TwB5VVl4AaABAQ'
        #hangupargs.debug=False
        #hangupargs.message_text=args
        #hangupargs.token_path='/home/debian/.cache/hangups/refresh_token.txt'
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #cookies = hangups.auth.get_auth_stdin(hangupargs.token_path)
        #client = hangups.Client(cookies)
        #task = asyncio.async(_async_main(send_message, client, hangupargs))
        #loop = asyncio.get_event_loop()
        #try:
        #    loop.run_until_complete(task)
        #except KeyboardInterrupt:
        #    task.cancel()
        #    loop.run_forever()
        #finally:
        #    loop.close()
        ## We are not reading the reply yet

        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #cookies = hangups.auth.get_auth_stdin(hangupargs.token_path)
        #client = hangups.Client(cookies)
        #task = asyncio.async(_async_main(sync_recent_conversations, client, hangupargs.conversation_id))
        #loop = asyncio.get_event_loop()
        #try:
        #    loop.run_until_complete(task)
        #except KeyboardInterrupt:
        #    task.cancel()
        #    loop.run_forever()
        #finally:
        #    loop.close()

 
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(message)s',
                        stream=sys.stdout)
    oauth = OAuth()
    oauth.from_cfg('oauth.cfg')
    jid = 'reflexioneseirreflexiones@gmail.com'
    chat_client = ChatClient(jid, oauth)
    chat_client.send_msg('fernand0movilizado@gmail.com','hola')
