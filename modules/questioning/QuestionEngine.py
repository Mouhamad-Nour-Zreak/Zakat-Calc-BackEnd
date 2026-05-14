from .Answer import Answer
from .Question import Question
from Collector import Collector
from experta import KnowledgeEngine, MATCH, NOT, AS, Rule, DefFacts, L

class QuestionEngine(KnowledgeEngine):

    def __init__(self, question: Question,args = []):
        super().__init__()
        self._question = question
        self.args = args
        self._collector:Collector = Collector()

    @DefFacts()
    def init(self):
        yield self._question

    @Rule(
        Question(id=MATCH.id, text=MATCH.text,action=MATCH.action, key=MATCH.key , choices=MATCH.choices),
        NOT(Answer(question_id=L(MATCH.id))),
    )
    def ask(self, id, text,action, key , choices):
        from link.state import state_manager

        # answer_value = input(action(text, self.args))
        formatted_question = action(text, self.args)

        state_manager.current_question = formatted_question
        state_manager.current_choices = choices
        state_manager.question_ready.set()

        state_manager.answer_provided.wait()

        answer_value = state_manager.user_answer
        state_manager.answer_provided.clear()

        self.declare(Answer(question_id=id, value=answer_value, key=key))

    @Rule(
        AS.question << Question(id=MATCH.id),
        AS.answer << Answer(question_id=MATCH.id, value=MATCH.value),
        salience=1,
    )
    def validate(self, question, answer, value):
        def validated(self: QuestionEngine, question, answer):
            self._collector.append(question["key"], answer["value"])
            self.retract(question)

        def invalidated(self, question, answer):
            from link.state import state_manager

            state_manager.question_ready.set()
            self.modify(question)

        actions = {True: validated, False: invalidated}

        validation_res = question.get("validator").checker(value)

        actions[validation_res](self, question, answer)

        self.retract(answer)

    def get_collector(self):
        return self._collector
