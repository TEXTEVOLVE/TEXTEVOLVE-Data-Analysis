from numpy import full
import os


def _generate_traceback_array(seq1, seq2):
    n_rows = len("-" + seq1)
    n_columns = len("-" + seq2)
    scoring_array = full([n_rows, n_columns], 0)
    traceback_array = full([n_rows, n_columns], "-")

    count = 0
    for row_index in range(1, n_rows):
        for col_index in range(1, n_columns):
            scoring_array[row_index, col_index] = count
            count += 1

    row_labels = [label for label in "-" + seq1]
    column_labels = [label for label in "-" + seq2]

    up_arrow = "\u2191"
    right_arrow = "\u2192"
    down_arrow = "\u2193"
    left_arrow = "\u2190"
    down_right_arrow = "\u2198"
    up_left_arrow = "\u2196"

    arrow = "-"
    sofit_letters = ['ך','ם','ן','ף','ץ']
    gap_penalty = -2
    match_bonus = 3
    sofit_match_bonus = 10
    mismatch_penalty = -3
    max_score = -1
    max_index = (-1, -1)

    for row in range(1, n_rows):
        for col in range(1, n_columns):
            if row == 0 and col == 0:
                score = 0
                arrow = "-"
            elif row == 0:
                previous_score = scoring_array[row, col - 1]
                score = previous_score + gap_penalty
                arrow = left_arrow
            elif col == 0:
                previous_score = scoring_array[row - 1, col]
                score = previous_score + gap_penalty
                arrow = up_arrow
            else:
                cell_to_the_left = scoring_array[row, col - 1]
                from_left_score = cell_to_the_left + gap_penalty
                above_cell = scoring_array[row - 1, col]
                from_above_score = above_cell + gap_penalty
                diagonal_left_cell = scoring_array[row - 1, col - 1]
                if seq1[row - 1] == seq2[col - 1]:
                    if seq1[row-1] in sofit_letters:
                        diagonal_left_cell_score = diagonal_left_cell + sofit_match_bonus
                    else:
                        diagonal_left_cell_score = diagonal_left_cell + match_bonus
                else:
                    diagonal_left_cell_score = diagonal_left_cell + mismatch_penalty
                score = max([0, diagonal_left_cell_score, from_above_score, from_left_score])
                scoring_array[row, col] = score
                if scoring_array[row, col] >= max_score:
                    max_index = (row, col)
                    max_score = scoring_array[row, col]
                if score == from_left_score:
                    arrow = left_arrow
                elif score == from_above_score:
                    arrow = up_arrow
                elif score == diagonal_left_cell_score:
                    arrow = up_left_arrow

            traceback_array[row, col] = arrow
            scoring_array[row, col] = score

    return traceback_array, score, max_score, max_index


def _generate_traceback_alignment(traceback_array, seq1, seq2, max_index, up_arrow="\u2191",
                                  left_arrow="\u2190", up_left_arrow="\u2196", stop="-"):
    n_rows = len(seq1) + 1
    n_columns = len(seq2) + 1
    (max_seq1, max_seq2) = max_index
    row = max_seq1
    col = max_seq2
    arrow = traceback_array[row, col]
    aligned_seq1 = ""
    aligned_seq2 = ""
    alignment_indicator = ""

    while arrow is not "-":
        print("Currently on row:", row)
        print("Currently on col:", col)
        arrow = traceback_array[row, col]
        print("Arrow:", arrow)
        if arrow == up_arrow:
            print("insert indel into top sequence")
            aligned_seq2 = "-"
            aligned_seq1 = seq1[row - 1] + aligned_seq1
            row -= 1
        # This tells the computer what to do when there is an insertion or deletion in seq1
        elif arrow == up_left_arrow:
            print("match or mismatch")
            seq1_character = seq1[row - 1]
            seq2_character = seq2[col - 1]
            aligned_seq1 = seq1[row - 1] + aligned_seq1
            aligned_seq2 = seq2[col - 1] + aligned_seq2
            if seq1_character == seq2_character:
                alignment_indicator = "|" + alignment_indicator
            else:
                alignment_indicator = " " + alignment_indicator
            row -= 1
            col -= 1
        # This tells the computer what to do when there is a match or a mismatch between sequences
        elif arrow == left_arrow:
            print("Insert indel into left sequence")
            aligned_seq1 = "-" + aligned_seq1
            aligned_seq2 = seq2[col - 1] + aligned_seq2
            alignment_indicator = " " + alignment_indicator
            col -= 1
            # This tells the computer what to do when there is an insertion or deletion in seq2
        elif arrow == stop:
            break
        else:
            raise ValueError(f"Traceback array entry at {row},{col}: {arrow} is not recognized as an up arrow")
    return aligned_seq1, aligned_seq2


def smith_waterman(seq1, seq2):
    traceback_array, score, max_score, max_index = _generate_traceback_array(seq1, seq2)
    seq1, seq2 = _generate_traceback_alignment(traceback_array, seq1, seq2, max_index)
    return seq1, seq2, score


def run():
    os.getcwd()
    # within the os module, returns the current working directory of a process.
    cwd = os.getcwd()
    # creates an object known as 'cwd' to which the command os.getcwd() is associated.
    print("Current working directory:{0}".format(cwd))
    # prints the current working directory using the object cwd.
    base_directory = os.path.join(cwd, "Alignment Data1")
    # joins the current working directory and the subfile which we want to read under the object 'basedirectory'
    with os.scandir(base_directory) as folders:
        folders = [folder for folder in folders if folder.is_dir()]
        for folder in folders:
            print(folder)
        # 'scans' basedirectory, iterates through all folders in the subfolder (if any exist), and lists them.
        test_directory = os.path.join(base_directory, folder)
        # creates an object called 'testdirectory' which joins the basedirectory with the specific folder we want to
        # read. we have now told the computer exactly which folders we want to read and how to find them.
        with os.scandir(test_directory) as texts:
            texts = [text for text in texts if not (text.name.endswith("DS_Store"))]
            for text in texts:
                print(text)
            # print(texts)
            # calls each file within the folder a 'text' and tells the computer to iterate through each file.
            # tells the computer to ignore files ending in DS_Store or html.
            # print(texts) tells the computer to print all files within the subfolder.
            base_text_pattern = "JTS"
            base_text = [text for text in texts if base_text_pattern in text.name][0]
            basetextfilepath = os.path.join(test_directory, base_text)
            # tells the computer that the first text in the order of iterations should have 'JTS' in the filename.
            # tells the computer to iterate through the folder looking for the base text.
            # tells the computer to join the base text to the text directory and read them together.
            base_text_contents = open(basetextfilepath, encoding='utf-8').read()
            # tells the computer to read the files within the directory in utf-8 encoding.
            texts = [text for text in texts if base_text_pattern not in text.name]
            # tells the computer to iterate through all the files in the folder where the name does not have 'JTS'
            for text in texts:
                # call the entire algorithm within this loop
                # print(text)
                text_filepath = os.path.join(test_directory, text)
                text_contents = open(text_filepath, encoding='utf-8').read()
                # print(basetextcontents)
                # print(textcontents)
                print()
                aligned_seq1, aligned_seq2, score = smith_waterman(base_text_contents, text_contents)
                print(base_text, text)
                print_alignment(aligned_seq1, aligned_seq2)
                print(score)


def print_alignment(string1, string2):
    string1 = string1.replace("\n", "")
    string2 = string2.replace("\n", "")
    index = 0
    increment = 50
    maxchar = len(string1)
    while index < maxchar:
        if index + increment < maxchar:
            remaining_chars = 50
        else:
            remaining_chars = maxchar - index
        print(string1[index:index + increment])
        print(pipes(remaining_chars))
        print(string2[index:index + increment])
        print("")
        index = index + increment


def pipes(n):
    empty = ("")
    for i in range(n):
        empty = empty + "|"
    return empty


if __name__ == "__main__":
    run()
