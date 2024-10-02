# meta developer: @hmtIpage

import traceback
from .. import loader, utils

class BrainfuckMod(loader.Module):
    """Модуль для кодирования и декодирования Brainfuck"""
    strings = {"name": "BrainfuckCoder"}

    @staticmethod
    def _bf_encode(text: str) -> str:
        result = []
        code = ""
        for char in text:
            char_code = ord(char)
            result.append('+' * char_code + '.')
            result.append('>')
        return ''.join(result[:-1])

    @staticmethod
    def _bf_decode(code: str) -> str:
        code = ''.join(filter(lambda x: x in ['>', '<', '+', '-', '.', ',', '[', ']'], code))
        memory = [0]
        pointer = 0
        result = []
        pc = 0
        loop_stack = []

        while pc < len(code):
            cmd = code[pc]

            if cmd == '>':
                pointer += 1
                if pointer == len(memory):
                    memory.append(0)
            elif cmd == '<':
                pointer = max(0, pointer - 1)
            elif cmd == '+':
                memory[pointer] = (memory[pointer] + 1) % 256
            elif cmd == '-':
                memory[pointer] = (memory[pointer] - 1) % 256
            elif cmd == '.':
                result.append(chr(memory[pointer]))
            elif cmd == ',':
                pass  # Ввод пока не реализован
            elif cmd == '[':
                if memory[pointer] == 0:
                    loop_start = pc
                    loop_level = 1
                    while loop_level > 0:
                        pc += 1
                        if code[pc] == '[':
                            loop_level += 1
                        elif code[pc] == ']':
                            loop_level -= 1
                else:
                    loop_stack.append(pc)
            elif cmd == ']':
                if memory[pointer] != 0:
                    pc = loop_stack[-1]
                else:
                    loop_stack.pop()

            pc += 1
        return ''.join(result)

    async def bfcodecmd(self, message):
        """Кодировать сообщение в Brainfuck"""
        text = utils.get_args_raw(message) or (await message.get_reply_message()).raw_text
        if not text:
            await utils.answer(message, "Нужно указать текст или ответить на сообщение.")
            return

        encoded = self._bf_encode(text)
        await utils.answer(message, f"<code>{encoded}</code>")

    async def bfdecodecmd(self, message):
        """Декодировать сообщение из Brainfuck"""
        code = utils.get_args_raw(message) or (await message.get_reply_message()).raw_text
        if not code:
            await utils.answer(message, "Нужно указать код или ответить на сообщение.")
            return

        try:
            decoded = self._bf_decode(code)
            await utils.answer(message, f"<code>{decoded}</code>")
        except Exception:
            await utils.answer(message, f"Ошибка декодирования:\n<code>{traceback.format_exc()}</code>")
