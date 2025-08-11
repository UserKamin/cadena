import random


class QuestionPicker:
    def __init__(self):
        """Initialize with the full list of questions"""
        self.questions = {
            1: "Full name.",
            2: "Zodiac sign.",
            3: "3 Fears.",
            4: "3 things I love.",
            5: "My best friend.",
            6: "Last song I listened to.",
            7: "4 Turn ons.",
            8: "4 Turn offs.",
            9: "What colour underwear I'm wearing right now.",
            10: "How many tattoos/piercings I have.",
            11: "The reason why I joined twitter.",
            12: "How I feel right now.",
            13: "Something I really, really want.",
            14: "My current relationship status.",
            15: "Meaning behind my username.",
            16: "My favourite movie(s).",
            17: "My favourite song(s).",
            18: "My favourite band(s).",
            19: "3 Things that upset me.",
            20: "3 Things that make me happy.",
            21: "What I find attractive in other people.",
            22: "Someone I miss.",
            23: "Someone I love.",
            24: "My relationship with my parents.",
            25: "My favourite holiday.",
            26: "My closest twitter friend.",
            27: "Someone from twitter that I'd date.",
            28: "A confession.",
            29: "3 Things that annoy me easily.",
            30: "My favourite animal(s).",
            31: "My pets.",
            32: "One thing I've lied about.",
            33: "Something that's currently worrying me.",
            34: "An embarrassing moment.",
            35: "Where I work.",
            36: "Something that's constantly on my mind.",
            37: "3 Habits I have.",
            38: "My future goals.",
            39: "Something I fantasise about.",
            40: "My favourite store(s).",
            41: "My favourite food(s).",
            42: "What I did yesterday.",
            43: "Something I'm talented at.",
            44: "My idea of a perfect date.",
            45: "My celebrity crush(es).",
            46: "A photo of myself.",
            47: "My favourite blog(s).",
            48: "Number of kids I want.",
            49: "Do I smoke/drink.",
            50: "Any question you'd like."
        }

        self.available_numbers = list(range(1, 51))
        self.asked_questions = []

    def pick_question(self):
        """Pick a random question and remove it from available pool"""
        if not self.available_numbers:
            return None, "All questions have been asked!"

        # Pick random number from available pool
        number = random.choice(self.available_numbers)
        question = self.questions[number]

        # Remove from available and add to asked
        self.available_numbers.remove(number)
        self.asked_questions.append((number, question))

        return number, question

    def get_status(self):
        """Get current status of questions"""
        total = len(self.questions)
        asked = len(self.asked_questions)
        remaining = len(self.available_numbers)
        return f"Asked: {asked}/{total} | Remaining: {remaining}"

    def reset(self):
        """Reset to start over"""
        self.available_numbers = list(range(1, 51))
        self.asked_questions = []

    def show_asked_questions(self):
        """Show all previously asked questions"""
        if not self.asked_questions:
            return "No questions asked yet."

        result = "Previously asked questions:\n"
        for num, question in self.asked_questions:
            result += f"{num}. {question}\n"
        return result


def main():
    """Interactive question picker"""
    picker = QuestionPicker()

    print("=== SEND ME A NUMBER - Interactive Question Picker ===")
    print("Commands: 'continue'/'next'/'next question' for next question")
    print("         'status' to see progress")
    print("         'history' to see asked questions")
    print("         'reset' to start over")
    print("         'quit'/'exit' to stop")
    print("-" * 55)

    while True:
        user_input = input("\nPress Enter or type a command: ").strip().lower()

        if user_input in ['quit', 'exit', 'q']:
            print("Thanks for playing!")
            break
        elif user_input == 'status':
            print(picker.get_status())
        elif user_input == 'history':
            print(picker.show_asked_questions())
        elif user_input == 'reset':
            picker.reset()
            print("Questions reset! Ready to start over.")
        elif user_input in ['', 'continue', 'next', 'next question']:
            number, question = picker.pick_question()
            if number is None:
                print(question)  # This will be the "All questions asked" message
                reset_choice = input(
                    "Would you like to reset and start over? (y/n): ")
                if reset_choice.lower() in ['y', 'yes']:
                    picker.reset()
                    print("Reset complete!")
                else:
                    break
            else:
                print(f"\n🎲 Number {number}: {question}")
                print(f"   ({picker.get_status()})")
        else:
            print(
                "Unknown command. Try 'continue', 'status', 'history', 'reset', or 'quit'")


if __name__ == "__main__":
    main()
