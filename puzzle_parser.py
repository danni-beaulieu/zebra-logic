import os

from openai import OpenAI

from puzzle import Puzzle


class PuzzleParser:

    def __init__(self, dirnames):
        self.parent_dir = "data"
        self.dirnames = dirnames
        self.puzzles = []

    def load_puzzles(self):
        for dirname in self.dirnames:
            for subdir, dirs, files in os.walk(self.parent_dir + "/" + dirname):
                for d in dirs:
                    puzzle = Puzzle(os.path.join(subdir, d))
                    puzzle.load_puzzle()
                    self.puzzles.append(puzzle)

    def retrieve_answers(self):
        client = OpenAI()
        for puzzle in self.puzzles:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n"
                                   "Entities: \r\n" + puzzle.entities + "\r\n" +
                                   "Clues: \r\n" + puzzle.clues + "\r\n"
                    }
                ]
            )
            puzzle.response = completion.choices[0].message
            puzzle.content = puzzle.response.content
            puzzle.grade_answer()
            print("Grade: " + str(puzzle.grade))
            print("Success: " + str(puzzle.success))
            puzzle.output_puzzle("output/baseline")
