from similarity import find_most_similar
from corpus import CORPUS

class Bot:

    def __init__(self):
        self.event_stack = []
        self.scopetest = "test"
        self.settings = {
            "min_score": 0.5,
            "help_email": "fakeEmail@notArealEmail.com",
            "faq_page": "www.NotActuallyAnFAQ.com"
        }

        print "Ask a question:"
        while(True):
            self.allow_question()

    def allow_question(self):
        # Check for event stack
        potential_event = None
        if(len(self.event_stack)):
            potential_event = self.event_stack.pop()
        if potential_event:
            text = raw_input("Response: ")
            potential_event.handle_response(text, self)
        else:
            text = raw_input("Question: ")
            answer = self.pre_built_responses_or_none(text)
            if not answer:
                answer = find_most_similar(text)
                self.answer_question(answer, text)

    def answer_question(self, answer, text):
        if answer['score'] > self.settings['min_score']:
            # set off event asking if the response question is what they were looking for
            print "\nBest-fit question: %s. (Score: %s)\nAnswer: %s\n" % (answer['question'],
                                                                          answer['score'],
                                                                          answer['answer'])
        else:
            print "Woops! I'm having trouble finding the answer to your question. " \
                  "Would you like to see the list of questions that I am able to answer?\n"
            # set off event for corpus dump
            self.event_stack.append(Event("corpus_dump", text))

    def pre_built_responses_or_none(self, text):
        # only return answer if exact match is found
        pre_built = [
            {
                "Question": "Who made you?",
                "Answer": "I was created by TS-North.\n"
            },
            {
                "Question": "When were you born?",
                "Answer": "I first opened my eyes in alpha stage February 9th, 2018.\n"
            },
            {
                "Question": "What is your purpose?",
                "Answer": "I assist user experience by providing an interactive FAQ chat.\n"
            },
            {
                "Question": "Thanks",
                "Answer": "Glad I could help!\n"
            },
            {
                "Question": "Thank you",
                "Answer": "Glad I could help!\n"
            }
        ]
        for each_question in pre_built:
            if each_question['Question'].lower() in text.lower():
                print each_question['Answer']
                return each_question


    def dump_corpus(self):
        question_stack = []
        for each_item in CORPUS:
            question_stack.append(each_item['Question'])
        return question_stack


class Event:

    def __init__(self, kind, text):
        self.kind = kind
        self.CONFIRMATIONS = ["yes", "sure", "okay", "that would be nice", "yep"]
        self.NEGATIONS = ["no", "don't", "dont", "nope"]
        self.original_text = text

    def handle_response(self, text, bot):
        if self.kind == "corpus_dump":
            self.corpus_dump(text, bot)

    def corpus_dump(self, text, bot):
        for each_confirmation in self.CONFIRMATIONS:
            for each_word in text.split(" "):
                if each_confirmation.lower() == each_word.lower():
                    corpus = bot.dump_corpus()
                    corpus = ["-" + s for s in corpus]
                    print "%s%s%s" % ("\n", "\n".join(corpus), "\n")
                    return 0
        for each_negation in self.NEGATIONS:
            for each_word in text.split(" "):
                if each_negation.lower() == each_word.lower():
                    print "Feel free to ask another question or send an email to %s.\n" % bot.settings['help_email']
                    bot.allow_question()
                    return 0
        # base case, no confirmation or negation found
        print "I'm having trouble understanding what you are saying. My ability is quite limited, " \
              "please refer to %s or email %s if I was not able to answer your question. " \
              "For convenience, a google link has been generated below: \n%s\n" % (bot.settings['faq_page'],
                                                                                 bot.settings['help_email'],
                                                                                 "https://www.google.com/search?q=%s" %
                                                                                 ("+".join(self.original_text.split(" "))))
        return 0


Bot()
