import os
from openai import OpenAI
from puzzle import Puzzle
from enum import Enum
import ast


Strategy = Enum('Strategy', ['BASELINE', 'BASELINE_SINGLE', 'COT_ZERO', 'COT_SINGLE', 'PS_ZERO'])

def content_by_strategy(puzzle, strategy):
    content = ""
    example_question = "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" \
                       "Entities: \r\nnames: Gene, Jeffrey, Leroy, Olga\r\n" \
                       "brands: Bistric, Grennel, Pinkster, Travelore\r\n" \
                       "pack size (liters): 25, 30, 35, 40\r\n\r\n" \
                       "Clues: \r\nThe Pinkster pack is 5 liters smaller than the Grennel pack.\r\n" \
                       "Olga's pack is 25 liters.\r\n" \
                       "The 30 liter pack, the Bistric pack and the Grennel pack are all different packs.\r\n" \
                       "Of Leroy's pack and the Travelore pack, one is 25 liters and the other is 30 liters.\r\n" \
                       "Gene's pack is 35 liters.\r\n\r\n"
    example_cot = "Steps:\r\n\r\nExtract information from each clue.\r\n\r\n" \
                  "1. \"The Pinkster pack is 5 liters smaller than the Grennel pack.\" \r\n" \
                  "-The Pinkster pack can be 25, 30, or 35 liters.\r\n" \
                  "-The Grennel pack can be 30, 35, or 40 liters.\r\n" \
                  "-The Pinkster pack size equals the Grennel pack size minus 5 liters.\r\n\r\n" \
                  "2. \"Olga's pack is 25 liters.\"\r\n-Olga is associated to pack size 25.\r\n\r\n" \
                  "3. \"The 30 liter pack, the Bistric pack and the Grennel pack are all different packs.\"\r\n" \
                  "-The Bistric pack is not 30 liters.\r\n-The Grennel pack is not 30 liters.\r\n\r\n" \
                  "4. \"Of Leroy's pack and the Travelore pack, one is 25 liters and the other is 30 liters.\"\r\n" \
                  "-Leroy's pack is not the Travelore pack.\r\n-Leroy's pack is either 25 liters or 30 liters.\r\n" \
                  "-The Travelore pack is either 25 liters or 30 liters.\r\n" \
                  "-If Leroy's pack is 25 liters, the Travelore pack is 30 liters.\r\n" \
                  "-If the Travelore pack is 25 liters, Leroy's pack is 30 liters.\r\n\r\n" \
                  "5. \"Gene's pack is 35 liters.\"\r\n- Gene is associated to pack size 35.\r\n\r\n" \
                  "Combine information from multiple clues.\r\n\r\nFrom clue 2, we know Olga is associated to pack " \
                  "size 25; combining this with clue 4, we know Leroy's pack must be 30 liters; since Leroy's pack " \
                  "is 30 liters, the Travelore pack must be 25 liters; therefore, we know Olga is associated to the " \
                  "Travelore pack. From all this and clue 3, we know Leroy's pack is not the Bistric pack or the " \
                  "Grennel pack; since the Pinkster pack is the only other pack left, we know Leroy is associated to " \
                  "the Pinkster pack and the Pinkster pack is 30 liters. From all this and clue 1, we know the " \
                  "Grennel pack must be 35 liters. From all this and clue 5, we know Gene is associated to the " \
                  "Grennel pack. This leaves Jeffrey associated to the Bistric pack with size 40 liters.\r\n\r\n"
    example_answer = "Answer:\r\nOlga, Travelore, 25 \r\nLeroy, Pinkster, 30 \r\n" \
                     "Gene, Grennel, 35 \r\nJeffrey, Bistric, 40\r\n\r\n"

    if strategy is Strategy.BASELINE:
        content = "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" + \
                  "Entities: \r\n" + puzzle.entities + "\r\n" + \
                  "Clues: \r\n" + puzzle.clues + "\r\n"
    elif strategy is Strategy.BASELINE_SINGLE:
        content = example_question + example_answer + \
                  "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" + \
                  "Entities: \r\n" + puzzle.entities + "\r\n" + \
                  "Clues: \r\n" + puzzle.clues + "\r\n"
    elif strategy is Strategy.COT_ZERO:
        content = "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" + \
                  "Entities: \r\n" + puzzle.entities + "\r\n" + \
                  "Clues: \r\n" + puzzle.clues + "\r\n" + \
                  "Let's think step by step." + "\r\n"
    elif strategy is Strategy.COT_SINGLE:
        content = example_question + example_cot + example_answer + \
                  "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" + \
                  "Entities: \r\n" + puzzle.entities + "\r\n" + \
                  "Clues: \r\n" + puzzle.clues + "\r\n"
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

    def retrieve_answers(self, strategy, outdir, model="gpt-4o"):
        client = OpenAI()
        for puzzle in self.puzzles:
            if strategy in [Strategy.BASELINE_SINGLE, Strategy.COT_SINGLE] and "example" in puzzle.dirname:
                continue
            completion = client.chat.completions.create(
                model=model,
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
            # print("Grade: " + str(puzzle.grade))
            # print("Success: " + str(puzzle.success))
            puzzle.output_puzzle(outdir)

    def tabulate_score(self, expdir):
        sum_grade = 0
        total_success = 0
        num_outputs = 0

        for subdir, dirs, files in os.walk(expdir):
            for f in files:
                with open(expdir + "/" + f, 'r') as file:
                    result = file.read()
                    grade_search = result.split("Grade:")[1].strip().splitlines()[0]
                    grade_list = ast.literal_eval(grade_search)
                    sum_grade = sum_grade + sum(grade_list) / len(grade_list) * 100
                    success_search = result.split("Success:")[1].strip().splitlines()[0]
                    if success_search == 'True':
                        total_success = total_success + 1
                    num_outputs = num_outputs + 1

        with open(expdir + "/score.txt", "a") as f:
            f.write("Grade Average: \n" + str(sum_grade / num_outputs) + "\n")
            f.write("Success Percent: \n" + str(total_success / num_outputs * 100) + "\n")
