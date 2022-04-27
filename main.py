from string import digits

from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget


class Calc(Widget):
    ans = '0'
    carry = ans
    pressed_equal = False
    main_answer = ''

    def solve(self, button=None):
        if self.pressed_equal:
            self.quest_screen.text = ''
            self.pressed_equal = False
        if button != None:
            self.quest_screen.text += str(button.text)
        self.main_answer = self.quest_screen.text

        if 'Ans' in self.quest_screen.text:
            self.main_answer = str(self.main_answer.replace('Ans', self.carry))
        else:
            self.main_answer = str(self.main_answer)
        if '×' in self.main_answer:
            self.main_answer = self.main_answer.replace('×', '*')
        if '÷' in self.main_answer:
            self.main_answer = self.main_answer.replace('÷', '/')

        try:
            eval(self.main_answer)
        except ZeroDivisionError:
            self.answer_screen.text = 'Zero Division Error'
            self.answer_screen.color = 1, 0, 0, 1
        except SyntaxError:
            if self.quest_screen.text == '' or self.quest_screen.text[len(self.quest_screen.text) - 1] == '+' or \
                    self.quest_screen.text[len(self.quest_screen.text) - 1] == '-' or self.quest_screen.text[
                len(self.quest_screen.text) - 1] == '×' or self.quest_screen.text[
                len(self.quest_screen.text) - 1] == '÷':
                self.answer_screen.text = ''
            else:
                self.answer_screen.text = 'Syntax Error'
                self.answer_screen.color = 1, 0, 0, 1
        else:
            self.answer_screen.color = 1, 1, 1, 1
            if eval(self.main_answer) % 1 == 0.0:
                self.answer_screen.text = str(int(eval(self.main_answer) // 1))
            else:
                self.answer_screen.text = str(eval(self.main_answer))
            self.main_answer = ''

    def ON_(self):
        self.quest_screen.text = ''
        self.answer_screen.text = ''

    def operator(self, button):
        if self.pressed_equal:
            self.quest_screen.text = 'Ans'
            self.pressed_equal = False
        self.quest_screen.text += str(button.text)
        self.answer_screen.text = ''

    def EQUAL_(self):
        if self.quest_screen.text == '':
            pass
        self.ans = self.answer_screen.text
        if all(i in digits + '.' for i in self.ans):
            self.carry = self.ans
        self.pressed_equal = True

    def ANS_(self):
        if self.pressed_equal:
            self.quest_screen.text = 'Ans'
            self.pressed_equal = False
        else:
            self.quest_screen.text += 'Ans'
        self.solve()

    def DEL_(self):
        if self.quest_screen.text.endswith('Ans'):
            self.quest_screen.text = self.quest_screen.text[:len(self.quest_screen.text) - 2]
        self.quest_screen.text = self.quest_screen.text[:len(self.quest_screen.text) - 1]
        self.solve()

    def pop(self):
        Exit().open()


class Exit(Popup):
    pass


class CalcApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        return Calc()


if __name__ == '__main__':
    CalcApp().run()
