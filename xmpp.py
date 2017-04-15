import sys
from errbot import BotPlugin, botcmd, webhook
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import logging
import asyncio
import argparse

_logger = logging.getLogger(__name__)


"""Example of using hangups to send a chat message to a conversation."""

import asyncio

import hangups

from common import run_example


@asyncio.coroutine
def send_message(client, args):
    request = hangups.hangouts_pb2.SendChatMessageRequest(
        request_header=client.get_request_header(),
        event_request_header=hangups.hangouts_pb2.EventRequestHeader(
            conversation_id=hangups.hangouts_pb2.ConversationId(
                id=args.conversation_id
            ),
            client_generated_id=client.get_client_generated_id(),
        ),
        message_content=hangups.hangouts_pb2.MessageContent(
            segment=[
                hangups.ChatMessageSegment(args.message_text).serialize()
            ],
        ),
    )
    yield from client.send_chat_message(request)

@asyncio.coroutine
def get_conversation(get_info):
    """Get a conversation by id"""
    conversation_id = get_info[0]
    max_events = get_info[1]
    conversation = conv_list.get(conversation_id)
    # event0 = conversation._events[0]
    events = yield from conversation.get_events(None, max_events)
    event0 = events[-1]
    events = yield from conversation.get_events(event0.id_, max_events)
    events.append(event0)
    output = ""
    for event in events:
        ev = Message.from_conversation_event(conversation, event, None)
        if ev is not None:
            output += str(ev) + "\n"
    return output

@asyncio.coroutine
def _async_main(example_coroutine, client, args):
    """Run the example coroutine."""
    # Spawn a task for hangups to run in parallel with the example coroutine.
    task = asyncio.async(client.connect())

    # Wait for hangups to either finish connecting or raise an exception.
    on_connect = asyncio.Future()
    client.on_connect.add_observer(lambda: on_connect.set_result(None))
    done, _ = yield from asyncio.wait(
        (on_connect, task), return_when=asyncio.FIRST_COMPLETED
    )
    yield from asyncio.gather(*done)

    # Run the example coroutine. Afterwards, disconnect hangups gracefully and
    # yield the hangups task to handle any exceptions.
    try:
        yield from example_coroutine(client, args)
    finally:
        yield from client.disconnect()
        yield from task

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


    @botcmd
    def forwardmessage(self, msg, args):
        hangupargs = argparse.Namespace()
        # We need to be able to locate the conversation
        # Arguments: (Namespace(conversation_id='UgybUd1gf4E4TwB5VVl4AaABAQ', debug=False, message_text='aeiou a e' , token_path='/home/debian/.cache/hangups/refresh_token.txt'),)
        hangupargs.conversation_id='UgybUd1gf4E4TwB5VVl4AaABAQ'
        hangupargs.debug=False
        hangupargs.message_text=args
        hangupargs.token_path='/home/debian/.cache/hangups/refresh_token.txt'
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        cookies = hangups.auth.get_auth_stdin(hangupargs.token_path)
        client = hangups.Client(cookies)
        task = asyncio.async(_async_main(send_message, client, hangupargs))
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(task)
        except KeyboardInterrupt:
            task.cancel()
            loop.run_forever()
        finally:
            loop.close()
        # We are not reading the reply yet
        #output = yield from get_conversation(hangupargs.conversation_id)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(message)s',
                        stream=sys.stdout)
    oauth = OAuth()
    oauth.from_cfg('oauth.cfg')
    jid = 'reflexioneseirreflexiones@gmail.com'
    chat_client = ChatClient(jid, oauth)
    chat_client.send_msg('fernand0movilizado@gmail.com','hola')
