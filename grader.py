import ast
import os


class Grader:

    @staticmethod
    def tabulate_score_majority(expdir):
        final_sum_grade = 0
        final_total_success = 0
        num_outputs = 0

        for subdir, dirs, files in os.walk(expdir):
            for filename in os.listdir(expdir):
                if "-0" in filename:

                    file_count = 0
                    sum_grade = 0
                    total_success = 0
                    parts = filename.split("-0", 1)
                    prefix = parts[0]

                    for specificfile in os.listdir(expdir):

                        if specificfile.startswith(prefix) and os.path.isfile(os.path.join(expdir, specificfile)):
                            file_count += 1

                            with open(expdir + "/" + specificfile, 'r') as file:
                                result = file.read()
                                grade_search = result.split("Grade:")[1].strip().splitlines()[0]
                                grade_list = ast.literal_eval(grade_search)
                                sum_grade = sum_grade + sum(grade_list) / len(grade_list) * 100
                                success_search = result.split("Success:")[1].strip().splitlines()[0]
                                if success_search == 'True':
                                    total_success = total_success + 1

                    with open(expdir + "/score-inner_" + prefix + ".txt", "a") as f:

                        num_outputs = num_outputs + 1
                        grade_inner = sum_grade / file_count
                        final_sum_grade = final_sum_grade + grade_inner
                        success_majority = False
                        success_pct = total_success / file_count * 100
                        if success_pct >= 50:
                            success_majority = True
                            final_total_success = final_total_success + 1

                        f.write("Grade Average: \n" + str(grade_inner) + "\n")
                        f.write("Success Percent: \n" + str(success_pct) + "\n")
                        f.write("Success: \n" + str(success_majority) + "\n")

        with open(expdir + "/score.txt", "a") as f:
            f.write("Grade Average: \n" + str(final_sum_grade / num_outputs) + "\n")
            f.write("Success Percent: \n" + str(final_total_success / num_outputs * 100) + "\n")

    @staticmethod
    def tabulate_score_total(expdir):
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

    @staticmethod
    def tabulate_score(expdir, majority=False):
        if majority:
            Grader.tabulate_score_majority(expdir)
        else:
            Grader.tabulate_score_total(expdir)
