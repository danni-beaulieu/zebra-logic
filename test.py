from puzzle_parser import PuzzleParser, Strategy

parser = PuzzleParser(["puzzles", "puzzlesEasy", "puzzlesModerate"])
parser.load_puzzles()

# parser.retrieve_answers(Strategy.BASELINE, "output/baseline_zero/4o")
# parser.retrieve_answers(Strategy.COT_ZERO, "output/cot_zero/4o")
# parser.retrieve_answers(Strategy.PS_ZERO, "output/ps_zero/4o")

# parser.tabulate_score("output/baseline_zero/4o")
# parser.tabulate_score("output/cot_zero/4o")
# parser.tabulate_score("output/ps_zero/4o")

parser.retrieve_answers(Strategy.BASELINE, "output/baseline_zero/4turbo", "gpt-4-turbo")
parser.retrieve_answers(Strategy.COT_ZERO, "output/cot_zero/4turbo", "gpt-4-turbo")
parser.retrieve_answers(Strategy.PS_ZERO, "output/ps_zero/4turbo", "gpt-4-turbo")

parser.tabulate_score("output/baseline_zero/4turbo")
parser.tabulate_score("output/cot_zero/4turbo")
parser.tabulate_score("output/ps_zero/4turbo")
