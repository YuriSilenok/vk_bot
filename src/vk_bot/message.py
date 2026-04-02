class Message:
    def __init__(self, bot, text: str, from_id: int, peer_id: int, date: int, payload: dict, attachments: list):
        self.bot = bot
        self.text = text
        self.from_id = from_id
        self.peer_id = peer_id
        self.date = date
        self.payload = payload
        self.attachments = attachments

    def __repr__(self):
        return f"Message(text='{self.text}', from_id={self.from_id})"

    def answer(self, text):
        self.bot.send_message(
            chat_id=self.from_id,
            text=text,
        )
