# -*- coding: utf-8 -*-

from telegram.ext import BaseFilter

# ANNE: neu für 'meinen' Bot
WAKE_WORDS_GREETING = ["hey rezeptbot", "ey rezeptbot", "hi rezeptbot", "hallo rezeptbot", "hallöchen rezeptbot", "hello rezeptbot","hey bot", "ey bot", "hi bot", "hallo bot", "hallöchen bot", "hello bot"]

# This class is used to filter the wake word for a new recipe search
class GreetFilter(BaseFilter):
    def filter(self, update):
        for word in WAKE_WORDS_GREETING:
            if word in update.text.lower():
                return True