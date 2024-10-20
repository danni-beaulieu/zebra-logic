from openai import OpenAI

from puzzle_parser import PuzzleParser

client = OpenAI()

# completion = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {
#             "role": "user",
#             "content": "Solve the logic grid puzzle. Label the final solution \"Answer\".\r\n\r\n"
#                        "Entities: \r\n"
#                        "names: Gene, Jeffrey, Leroy, Olga\r\n"
#                        "brands: Bistric, Grennel, Pinkster, Travelore\r\n"
#                        "pack size (liters): 25, 30, 35, 40\r\n\r\n"
#                        "Clues: \r\n"
#                        "The Pinkster pack is 5 liters smaller than the Grennel pack.\r\n"
#                        "Olga's pack is 25 liters.\r\n"
#                        "The 30 liter pack, the Bistric pack and the Grennel pack are all different packs.\r\n"
#                        "Of Leroy's pack and the Travelore pack, one is 25 liters and the other is 30 liters.\r\n"
#                        "Gene's pack is 35 liters.\r\n"
#         }
#     ]
# )
#
# print(completion.choices[0].message)

parser = PuzzleParser(["puzzles", "puzzlesEasy", "puzzlesModerate"])
parser.load_puzzles()
parser.retrieve_answers()
