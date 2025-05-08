import os 

class Puzzle:

    def __init__(self, dirname):
        self.dirname = dirname
        self.entities = ""
        self.clues = ""
        self.answers = ""
        self.response = ""
        self.content = ""
        self.attempt = ""
        self.grade = ""
        self.success = ""

    def load_puzzle(self):
        self.read_entities()
        self.read_clues()
        self.read_answers()

    def read_entities(self):
        with open(self.dirname + "/entities.txt", 'r') as file:

            entities = ""
            entities_text = file.read().strip()
            entities_lines = entities_text.splitlines()
            entity_types = entities_lines[0].split(',')

            type_index = 0
            for i in range(1, len(entities_lines)):
                if entities_lines[i]:
                    entities = entities + entity_types[type_index].strip() + ": " + entities_lines[i].strip() + "\r\n"
                    type_index = type_index + 1
            self.entities = entities

    def read_clues(self):
        with open(self.dirname + "/clues.txt", 'r') as file:
            self.clues = file.read()

    def read_answers(self):
        with open(self.dirname + "/answers.txt", 'r') as file:
            answers = []
            answers_text = file.read()
            answers_lines = answers_text.splitlines()

            for i in range(0, len(answers_lines)):
                if answers_lines[i]:
                    my_list = answers_lines[i].split(',')
                    answers.append([x.strip().lower() for x in my_list])

            self.answers = answers

    def print_puzzle(self):
        self.print_entities()
        self.print_clues()
        self.print_answers()

    def print_entities(self):
        print(self.entities)

    def print_clues(self):
        print(self.clues)

    def print_answers(self):
        print(self.answers)

    def grade_answer(self):
        answer_search = self.content.split("Answer")
        attempt_text = answer_search[len(answer_search) - 1]
        attempt_lines = attempt_text.splitlines()
        self.attempt = attempt_text

        correct = []
        for i in range(0, len(attempt_lines)):
            if attempt_lines[i]:
                match = []
                for a in self.answers:
                    match.append(all(item in attempt_lines[i].lower() for item in a))
                correct.append(match)

        grade = []
        for j in range(0, len(self.answers)):
            grade.append(self.check_one_true_at_index(correct, j))
        self.grade = grade
        self.success = all(grade)

    def output_puzzle(self, outdir, majority=False):
        prefix = "_".join(self.dirname.split("/"))
        name = prefix + ".txt"

        count = 0
        for filename in os.listdir(outdir):
            if filename.startswith(prefix) and os.path.isfile(os.path.join(outdir, filename)):
                count += 1

        if majority:
            name = prefix + "-" + str(count) + ".txt"

        with open(outdir + "/" + name, "a") as f:
            f.write("Attempt: \n\n" + self.attempt + "\n\n")
            f.write("Grade: \n" + str(self.grade) + "\n")
            f.write("Success: \n" + str(self.success) + "\n")


    @staticmethod
    def check_one_true_at_index(list_of_lists, index):
        true_count = sum(sublist[index] if index < len(sublist) else False for sublist in list_of_lists)
        return true_count == 1


