import os
from openai import OpenAI
from puzzle import Puzzle
from enum import Enum


Strategy = Enum('Strategy', ['BASELINE', 'COT_ZERO', 'COT_SINGLE', 'PS_ZERO'])

def content_by_strategy(puzzle, strategy):
    content = ""
    if strategy is Strategy.BASELINE:
        content = "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" + \
                  "Entities: \r\n" + puzzle.entities + "\r\n" + \
                  "Clues: \r\n" + puzzle.clues + "\r\n"
    elif strategy is Strategy.COT_ZERO:
        content = "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" + \
                  "Entities: \r\n" + puzzle.entities + "\r\n" + \
                  "Clues: \r\n" + puzzle.clues + "\r\n" + \
                  "Let's think step by step." + "\r\n"
    elif strategy is Strategy.PS_ZERO:
        content = "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" + \
                  "Entities: \r\n" + puzzle.entities + "\r\n" + \
                  "Clues: \r\n" + puzzle.clues + "\r\n" + \
                  "Let's first understand the problem and devise a plan to solve the problem. " \
                  "Then, let's carry out the plan and solve the problem step by step."
    return content


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

    def retrieve_answers(self, strategy, outdir):
        client = OpenAI()
        for puzzle in self.puzzles:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": content_by_strategy(puzzle, strategy)
                    }
                ]
            )
            puzzle.response = completion.choices[0].message
            puzzle.content = puzzle.response.content
            puzzle.grade_answer()
            print("Grade: " + str(puzzle.grade))
            print("Success: " + str(puzzle.success))
            puzzle.output_puzzle(outdir)
