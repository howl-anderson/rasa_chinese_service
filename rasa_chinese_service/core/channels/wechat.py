import asyncio
import os

import aiohttp
from wechaty import (
    Contact,
    Message,
    Wechaty,
)
from wechaty.user.url_link import UrlLink
from wechaty_puppet import FileBox

rasa_server = os.environ.get("RASA_SERVER") or "http://localhost:5005"
rasa_url = os.environ.get("RASA_URL")
if not rasa_url:
    rasa_url = rasa_server + "/webhooks/rest/webhook"


async def rasa_proc(sender_id: str, request_text: str, msg=None):
    request = {
        "sender": sender_id,
        "message": request_text,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(rasa_url, json=request) as resp:
            print(resp.status)
            responses = await resp.json()
            wechaty_responses = []
            for response in responses:
                text = response.get("text")
                if text:
                    wechaty_responses.append(text)

                image = response.get("image")
                if image:
                    pass
                    # TODO: test me
                    # wechaty_responses.append(FileBox.from_url(image, "PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"))

                custom_response = response.get("custom")
                if custom_response:
                    pass
                    # TODO: test me
                    # url_link = custom_response.get("url")
                    # if url_link:
                    #     # TODO: has a bug in UrlLink?
                    #     wechaty_responses.append(
                    #         UrlLink.create(
                    #             url_link.get("url"),
                    #             url_link.get("title"),
                    #             url_link.get("thumbnail_url"),
                    #             url_link.get("description")
                    #         )
                    #     )

            return wechaty_responses


async def on_message(msg: Message):
    """
    Message Handler for the Bot
    """
    from_contact = msg.talker()
    request_text = msg.text()
    room = msg.room()

    if from_contact.is_self():
        # skip message from myself!
        return None

    from_contact_id = from_contact.contact_id
    # sender_id = "weixin_" + from_contact_id
    sender_id = from_contact_id

    if room is None:  # private message
        responses = await rasa_proc(sender_id, request_text, msg)
        print(">>>", responses)
        if not isinstance(responses, (list, tuple)):
            await msg.say(responses)
        else:
            for response in responses:
                await msg.say(response)
    else:  # message come from room chat
        pass
        # TODO: test me
        # # TODO: has a bug in mention_self() test?
        # if await msg.mention_self():  # this message mentioned me!
        #     pass
        #     # print("in room private message")
        #     # response_text = await generate_response(sender_id, request_text, msg)
        #     # await room.say(response_text, [from_contact_id])
        # else:  # message which not mention me
        #     print("in room broadcast message")
        #     print(room, request_text, room.room_id)


async def on_scan(qrcode: str, status: int, data):
    """
    Scan Handler for the Bot
    """
    print('Status: ' + str(status) + ', View QR Code Online: https://wechaty.js.org/qrcode/' + qrcode)


async def on_login(user: Contact):
    """
    Login Handler for the Bot
    """
    print(user)
    # TODO: To be written


async def main():
    """
    Async Main Entry
    """
    #
    # Make sure we have set WECHATY_PUPPET_SERVICE_TOKEN in the environment variables.
    #
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Java Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = Wechaty()

    bot.on('scan', on_scan)
    bot.on('login', on_login)
    bot.on('message', on_message)

    await bot.start()

    print('[Python Wechaty] Ding Dong Bot started.')


if __name__ == "__main__":
    asyncio.run(main())
