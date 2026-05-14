import threading
from modules.zakah.MainEngine import MainEngine

class StateManager:
    def __init__(self):
        self.engine = MainEngine()
        self.engine_thread = None
        self.current_question = None
        self.current_choices = None
        self.question_data = None
        self.user_answer = None
        self.is_finished = False
        self.final_zakah = None

        self.question_ready = threading.Event()
        self.answer_provided = threading.Event()

    def start_engine(self):
        if self.engine_thread is None or not self.engine_thread.is_alive():
            self.engine.reset()
            self.engine_thread = threading.Thread(target=self.engine.run, daemon=True)
            self.engine_thread.start()

    def get_question(self):
        self.question_ready.wait()  
        question_to_send = self.current_question
        choices_to_send = self.current_choices
        self.question_ready.clear()
        return {
            "status": "in_progress",
            "question": question_to_send,
            "choices": choices_to_send,
        }

    def provide_answer(self, answer: str):
        self.user_answer = answer

        self.answer_provided.set()

        self.question_ready.wait()

        if self.is_finished:
            return {
                "status": "finished",
                "result": self.final_zakah,
            }
        else:
            question_to_send = self.current_question
            choices_to_send = self.current_choices
            self.question_ready.clear()
            print(type(choices_to_send))
            return {
                "status": "in_progress",
                "question": question_to_send,
                "choices": choices_to_send,
            }

state_manager = StateManager()
