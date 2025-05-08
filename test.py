from puzzle_parser import PuzzleParser, Strategy
from grader import Grader

parser = PuzzleParser(["puzzles", "puzzlesEasy", "puzzlesModerate"])
# parser.load_puzzles()

# parser.retrieve_answers(Strategy.BASELINE, "output/test/4o")
# parser.tabulate_score("output/test/4o")

# parser.retrieve_answers(Strategy.BASELINE, "output/baseline_zero/4o")
# parser.retrieve_answers(Strategy.COT_ZERO, "output/cot_zero/4o")
# parser.retrieve_answers(Strategy.PS_ZERO, "output/ps_zero/4o")
#
# parser.tabulate_score("output/baseline_zero/4o")
# parser.tabulate_score("output/cot_zero/4o")
# parser.tabulate_score("output/ps_zero/4o")
#
# parser.retrieve_answers(Strategy.BASELINE, "output/baseline_zero/4turbo", "gpt-4-turbo")
# parser.retrieve_answers(Strategy.COT_ZERO, "output/cot_zero/4turbo", "gpt-4-turbo")
# parser.retrieve_answers(Strategy.PS_ZERO, "output/ps_zero/4turbo", "gpt-4-turbo")
#
# parser.tabulate_score("output/baseline_zero/4turbo")
# parser.tabulate_score("output/cot_zero/4turbo")
# parser.tabulate_score("output/ps_zero/4turbo")
#
# parser.retrieve_answers(Strategy.BASELINE, "output/baseline_zero/4", "gpt-4")
# parser.retrieve_answers(Strategy.COT_ZERO, "output/cot_zero/4", "gpt-4")
# parser.retrieve_answers(Strategy.PS_ZERO, "output/ps_zero/4", "gpt-4")
# 
# parser.tabulate_score("output/baseline_zero/4")
# parser.tabulate_score("output/cot_zero/4")
# parser.tabulate_score("output/ps_zero/4")
# 
# parser.retrieve_answers(Strategy.BASELINE, "output/baseline_zero/35turbo", "gpt-3.5-turbo")
# parser.retrieve_answers(Strategy.COT_ZERO, "output/cot_zero/35turbo", "gpt-3.5-turbo")
# parser.retrieve_answers(Strategy.PS_ZERO, "output/ps_zero/35turbo", "gpt-3.5-turbo")
# 
# parser.tabulate_score("output/baseline_zero/35turbo")
# parser.tabulate_score("output/cot_zero/35turbo")
# parser.tabulate_score("output/ps_zero/35turbo")
#
# parser.retrieve_answers(Strategy.BASELINE_SINGLE, "output/baseline_single/4o")
# parser.retrieve_answers(Strategy.COT_SINGLE, "output/cot_single/4o")
#
# parser.tabulate_score("output/baseline_single/4o")
# parser.tabulate_score("output/cot_single/4o")
#
# parser.retrieve_answers(Strategy.BASELINE_SINGLE, "output/baseline_single/4turbo", "gpt-4-turbo")
# parser.retrieve_answers(Strategy.COT_SINGLE, "output/cot_single/4turbo", "gpt-4-turbo")
#
# parser.tabulate_score("output/baseline_single/4turbo")
# parser.tabulate_score("output/cot_single/4turbo")
#
# parser.retrieve_answers(Strategy.BASELINE_SINGLE, "output/baseline_single/4", "gpt-4")
# parser.retrieve_answers(Strategy.COT_SINGLE, "output/cot_single/4", "gpt-4")
#
# parser.tabulate_score("output/baseline_single/4")
# parser.tabulate_score("output/cot_single/4")
#
# parser.retrieve_answers(Strategy.BASELINE_SINGLE, "output/baseline_single/35turbo", "gpt-3.5-turbo")
# parser.retrieve_answers(Strategy.COT_SINGLE, "output/cot_single/35turbo", "gpt-3.5-turbo")
#
# parser.tabulate_score("output/baseline_single/35turbo")
# parser.tabulate_score("output/cot_single/35turbo")
# 
# parser.retrieve_answers(Strategy.BASELINE_TWO, "output/baseline_two/4o")
# parser.retrieve_answers(Strategy.COT_TWO, "output/cot_two/4o")
# 
# parser.tabulate_score("output/baseline_two/4o")
# parser.tabulate_score("output/cot_two/4o")
# 
# parser.retrieve_answers(Strategy.BASELINE_TWO, "output/baseline_two/4turbo", "gpt-4-turbo")
# parser.retrieve_answers(Strategy.COT_TWO, "output/cot_two/4turbo", "gpt-4-turbo")
# 
# parser.tabulate_score("output/baseline_two/4turbo")
# parser.tabulate_score("output/cot_two/4turbo")
# 
# parser.retrieve_answers(Strategy.BASELINE_TWO, "output/baseline_two/4", "gpt-4")
# parser.retrieve_answers(Strategy.COT_TWO, "output/cot_two/4", "gpt-4")
# 
# parser.tabulate_score("output/baseline_two/4")
# parser.tabulate_score("output/cot_two/4")
# 
# parser.retrieve_answers(Strategy.BASELINE_TWO, "output/baseline_two/35turbo", "gpt-3.5-turbo")
# parser.retrieve_answers(Strategy.COT_TWO, "output/cot_two/35turbo", "gpt-3.5-turbo")
# 
# parser.tabulate_score("output/baseline_two/35turbo")
# parser.tabulate_score("output/cot_two/35turbo")


grader = Grader()
parser.load_puzzles(3)

# parser.retrieve_answers(Strategy.BASELINE_SINGLE, "output/baseline_single/4o")
# parser.retrieve_answers(Strategy.COT_SINGLE, "output/cot_single/4o")

grader.tabulate_score("output/baseline_sc/4o", True)
grader.tabulate_score("output/self_c/4o", True)

# parser.retrieve_answers(Strategy.BASELINE_SINGLE_SC, "output/baseline_sc/4turbo", "gpt-4-turbo")
# parser.retrieve_answers(Strategy.SELF_C, "output/self_c/4turbo", "gpt-4-turbo")

grader.tabulate_score("output/baseline_sc/4turbo", True)
grader.tabulate_score("output/self_c/4turbo", True)

# parser.retrieve_answers(Strategy.BASELINE_SINGLE_SC, "output/baseline_sc/4", "gpt-4")
# parser.retrieve_answers(Strategy.SELF_C, "output/self_c/4", "gpt-4")

grader.tabulate_score("output/baseline_sc/4", True)
grader.tabulate_score("output/self_c/4", True)

# parser.retrieve_answers(Strategy.BASELINE_SINGLE_SC, "output/baseline_sc/35turbo", "gpt-3.5-turbo")
# parser.retrieve_answers(Strategy.SELF_C, "output/self_c/35turbo", "gpt-3.5-turbo")

grader.tabulate_score("output/baseline_sc/35turbo", True)
grader.tabulate_score("output/self_c/35turbo", True)
