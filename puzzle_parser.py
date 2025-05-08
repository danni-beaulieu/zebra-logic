import os
from openai import OpenAI
from puzzle import Puzzle
from enum import Enum

Strategy = Enum('Strategy',
                ['BASELINE', 'BASELINE_SINGLE', 'BASELINE_SINGLE_SC', 'BASELINE_TWO', 'COT_ZERO', 'COT_SINGLE',
                 'COT_TWO', 'PS_ZERO', 'SELF_C'])


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

    example_question_two = "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" \
                           "Entities: \r\nmovies: Bold Service, Fatal Sheen, Maximum Risk, Wild Ones\r\n" \
                           "directors: Adrienne Day, Danny Trevor, Gabby Jones, Virgil Katz\r\n" \
                           "nominations: 2, 3, 4, 5\r\n\r\n" \
                           "Clues: \r\nFatal Sheen is either the movie that received 2 nominations or the movie directed by Gabby Jones.\r\n" \
                           "Of the movie directed by Gabby Jones and the film directed by Virgil Katz, one got 5 nominations and the other is Fatal Sheen.\r\n" \
                           "Maximum Risk received one fewer nomination than the movie directed by Adrienne Day.\r\n" \
                           "Bold Service is either the film that received 3 nominations or the movie that received 5 nominations.\r\n" \
                           "Bold service was directed by Adrienne Day.\r\n\r\n"
    example_cot_two = "Steps:\r\n\r\nExtract information from each clue.\r\n\r\n" \
                      "1. \"Fatal Sheen is either the movie that received 2 nominations or the movie directed by Gabby Jones.\" \r\n" \
                      "-If Fatal Sheen received 2 nominations, then it was not directed by Gabby Jones.\r\n" \
                      "-If Fatal Sheen was directed by Gabby Jones, then it did not receive 2 nominations.\r\n" \
                      "-Either Fatal Sheen received 2 nominations or it was directed by Gabby Jones.\r\n\r\n" \
                      "2. \"Of the movie directed by Gabby Jones and the film directed by Virgil Katz, one got 5 nominations and the other is Fatal Sheen.\"\r\n" \
                      "-Either the movie directed by Gabby Jones received 5 nominations or Gabby Jones directed Fatal Sheen.\r\n\r\n" \
                      "-Either the movie by Virgil Katz received 5 nominations or Virgil Katz directed Fatal Sheen.\r\n\r\n" \
                      "-The movie with 5 nominations was either directed by Gabby Jones or Virgil Katz.\r\n\r\n" \
                      "-Fatal Sheen was either directed by Gabby Jones or Virgil Katz.\r\n\r\n" \
                      "-Fatal Sheen did not receive 5 nominations.\r\n\r\n" \
                      "-The movie directed by Adrienne Day did not receive 5 nominations.\r\n\r\n" \
                      "-The movie directed by Danny Trevor did not receive 5 nominations.\r\n\r\n" \
                      "3. \"Maximum Risk received one fewer nomination than the movie directed by Adrienne Day.\"\r\n" \
                      "-Maximum Risk was not directed by Adrienne Day.\r\n\r\n" \
                      "-Maximum Risk did not receive 5 nominations.\r\n\r\n" \
                      "-The number of nominations received by the movie Adrienne Day directed minus one equals the number of nominations received by Maximum Risk.\r\n\r\n" \
                      "-The number of nominations received by Maximum Risk plus one equals the number of nominations received by the movie Adrienne Day directed.\r\n\r\n" \
                      "4. \"Bold Service is either the film that received 3 nominations or the movie that received 5 nominations.\"\r\n" \
                      "-Either Bold Service received 3 or 5 nominations.\r\n" \
                      "-Bold Service did not receive 2 nominations.\r\n" \
                      "-Bold Service did not receive 4 nominations. \r\n" \
                      "5. \"Bold Service was directed by Adrienne Day.\"\r\n" \
                      "-Bold Service was directed by Adrienne Day.\r\n" \
                      "Combine information from multiple clues.\r\n\r\nFrom Clue 5 we know Bold Service was directed by Adrienne Day; " \
                      "from Clue 4 we know Bold Service received either 3 or 5 nominations; from Clue 2 we know the movie directed by Adrienne Day did not receive 5 nominations; " \
                      "therefore we know Bold Service received 3 nominations. From this and from clue 3, we know Maximum Risk received 2 nominations. " \
                      "From this and from clue 1, we know Fatal Sheen was directed by Gabby Jones since it did not receive 2 nominations. " \
                      "From all that and clue 2, we know the movie directed by Virgil Katz received 5 nominations since Gabby Jones directed Fatal Sheen. " \
                      "Because we know Maximum Risk received 2 nominations and the movie directed by Virgil Katz received 5 nominations, we know Virgil Katz did not direct Maximum Risk; " \
                      "the only other movie without a director assigned is Wild Ones; therefore, Wild Ones was directed by Virgil Katz. " \
                      "Finally, Maximum Risk must have been directed by Danny Trevor since it is the last movie without a director assigned. " \
                      "All movies have been assigned a director and all but one has been assigned a nomination number. " \
                      "Therefore, Fatal Sheen by Gabby Jones must have received 4 nominations.\r\n\r\n"
    example_answer_two = "Answer:\r\nMaximum Risk, Danny Trevor, 2 \r\nBold Service, Adrienne Day, 3 \r\n" \
                         "Fatal Sheen, Gabby Jones, 4 \r\nWild Ones, Virgil Katz, 5 \r\n\r\n"

    if strategy is Strategy.BASELINE:
        content = "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" + \
                  "Entities: \r\n" + puzzle.entities + "\r\n" + \
                  "Clues: \r\n" + puzzle.clues + "\r\n"
    elif strategy is Strategy.BASELINE_SINGLE or strategy is Strategy.BASELINE_SINGLE_SC:
        content = example_question + example_answer + \
                  "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" + \
                  "Entities: \r\n" + puzzle.entities + "\r\n" + \
                  "Clues: \r\n" + puzzle.clues + "\r\n"
    elif strategy is Strategy.BASELINE_TWO:
        content = example_question + example_answer + \
                  example_question_two + example_answer_two + \
                  "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" + \
                  "Entities: \r\n" + puzzle.entities + "\r\n" + \
                  "Clues: \r\n" + puzzle.clues + "\r\n"
    elif strategy is Strategy.COT_ZERO:
        content = "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" + \
                  "Entities: \r\n" + puzzle.entities + "\r\n" + \
                  "Clues: \r\n" + puzzle.clues + "\r\n" + \
                  "Let's think step by step." + "\r\n"
    elif strategy is Strategy.COT_SINGLE or strategy is Strategy.SELF_C:
        content = example_question + example_cot + example_answer + \
                  "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n" + \
                  "Entities: \r\n" + puzzle.entities + "\r\n" + \
                  "Clues: \r\n" + puzzle.clues + "\r\n"
    elif strategy is Strategy.COT_TWO:
        content = example_question + example_cot + example_answer + \
                  example_question_two + example_cot_two + example_answer_two + \
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

    def load_puzzles(self, repeat=1):
        for dirname in self.dirnames:
            for subdir, dirs, files in os.walk(self.parent_dir + "/" + dirname):
                for i in range(repeat):
                    for d in dirs:
                        puzzle = Puzzle(os.path.join(subdir, d))
                        puzzle.load_puzzle()
                        self.puzzles.append(puzzle)

    def retrieve_answers(self, strategy, outdir, model="gpt-4o"):
        client = OpenAI()
        for puzzle in self.puzzles:
            if strategy in [Strategy.BASELINE_SINGLE, Strategy.BASELINE_SINGLE_SC, Strategy.BASELINE_TWO,
                            Strategy.COT_SINGLE, Strategy.COT_TWO, Strategy.SELF_C] \
                    and "example" in puzzle.dirname:
                continue
            elif strategy in [Strategy.BASELINE_TWO, Strategy.COT_TWO] and "presentation" in puzzle.dirname:
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
            if strategy in [Strategy.BASELINE_SINGLE_SC, Strategy.SELF_C]:
                puzzle.output_puzzle(outdir, majority=True)
            else:
                puzzle.output_puzzle(outdir, majority=False)
