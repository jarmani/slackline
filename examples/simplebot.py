#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import random
import sys

from slackline import SlackLine


class SimpleBot(SlackLine):

    command_prefix = '!'

    def cmd_ping(self):
        """
            *{command}* : *Say pong*
        """
        self.answer('pong')

    def cmd_echo(self, *args):
        """
            *{command}* <text> : *Repeat text*
            ex: {command} I'm the boss
        """
        self.answer(' '.join(args))

    def cmd_meme(self, meme, line1='_', line2='_'):
        """
            *{command}* <meme> [line1] [line2] : *Generate a meme*
            ex: {command} mordor Why-does-not I-do-not
            [line1] and [line2] are optinnals and -_ are replaced by spaces
            It uses http://memegen.link/, see meme list there
        """
        url = 'http://memegen.link/' + '/'.join([meme, line1, line2]) + '.jpg'
        self.answer(url)

    def cmd_rand(self, *args):
        """
            *{command}* One / Two / ... : *help you to make hard choice*
            ex: {command} Coffee / Tea
        """
        choice = random.choice(' '.join(args).split('/')).strip()
        self.answer(choice)

if __name__ == '__main__':
    bot = SimpleBot(sys.argv[1])
    bot.run()
