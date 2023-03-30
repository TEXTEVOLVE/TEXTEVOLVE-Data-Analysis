from numpy import full
import os

def _generate_traceback_array(seq1, seq2):
    n_rows = len("-" + seq1)
    n_columns = len("-" + seq2)
    scoring_array = full([n_rows, n_columns], 0)
    traceback_array = full([n_rows, n_columns], "-")

    count = 0
    for row_index in range(n_rows):
        for col_index in range(n_columns):
            scoring_array[row_index, col_index] = count
            count += 1

    n_rows = len(seq1) + 1  # need an extra row up top
    n_columns = len(seq2) + 1  # need an extra column on the left
    row_labels = [label for label in "-" + seq1]
    column_labels = [label for label in "-" + seq2]

    scoring_array = full([n_rows, n_columns], 0)
    traceback_array = full([n_rows, n_columns], "-")

    up_arrow = "\u2191"
    right_arrow = "\u2192"
    down_arrow = "\u2193"
    left_arrow = "\u2190"
    down_right_arrow = "\u2198"
    up_left_arrow = "\u2196"

    arrow = "-"
    gap_penalty = -0
    match_bonus = 5
    mismatch_penalty = -1

    # iterate over columns first because we want to do
    # all the columns for row 1 before row 2
    for row in range(n_rows):
        for col in range(n_columns):
            if row == 0 and col == 0:
                # We're in the upper right corner
                score = 0
                arrow = "-"
            elif row == 0:
                # We're on the first row
                # but NOT in the corner

                # Look up the score of the previous cell (to the left) in the score array\
                previous_score = scoring_array[row, col - 1]
                # add the gap penalty to it's score
                score = previous_score + gap_penalty
                arrow = left_arrow
            elif col == 0:
                # We're on the first column but not in the first row
                previous_score = scoring_array[row - 1, col]
                score = previous_score + gap_penalty
                arrow = up_arrow
            else:
                # We're in a 'middle' cell of the alignment

                # Calculate the scores for coming from above,
                # from the left, (representing an insertion into seq1)
                cell_to_the_left = scoring_array[row, col - 1]
                from_left_score = cell_to_the_left + gap_penalty

                # or from above (representing an insertion into seq2)
                above_cell = scoring_array[row - 1, col]
                from_above_score = above_cell + gap_penalty

                # diagonal cell, representing a substitution (e.g. A --> T)
                diagonal_left_cell = scoring_array[row - 1, col - 1]

                # NOTE: since the table has an extra row and column (the blank ones),
                # when indexing back to the sequence we want row -1 and col - 1.
                # since row 1 represents character 0 of the sequence.
                if seq1[row - 1] == seq2[col - 1]:
                    diagonal_left_cell_score = diagonal_left_cell + match_bonus
                else:
                    diagonal_left_cell_score = diagonal_left_cell + mismatch_penalty

                score = max([from_left_score, from_above_score, diagonal_left_cell_score])
                # take the max

                # make note of which cell was the max in the traceback array
                # using Unicode arrows
                if score == from_left_score:
                    arrow = left_arrow
                elif score == from_above_score:
                    arrow = up_arrow
                elif score == diagonal_left_cell_score:
                    arrow = up_left_arrow

            traceback_array[row, col] = arrow
            scoring_array[row, col] = score

    return traceback_array


def _generate_traceback_alignment(traceback_array, seq1, seq2, up_arrow="\u2191",
                                 left_arrow="\u2190", up_left_arrow="\u2196", stop="-"):
    row = len(seq1)
    col = len(seq2)
    arrow = traceback_array[row, col]
    aligned_seq1 = ""
    aligned_seq2 = ""
    alignment_indicator = ""
    while arrow is not "-":
        # print("Currently on row:",row)
        # print("Currently on col:",col)
        arrow = traceback_array[row, col]
        # print("Arrow:",arrow)

        if arrow == up_arrow:
            # print("insert indel into top sequence")
            # We want to add the new indel onto the left
            # side of the growing aligned sequence
            aligned_seq2 = "-" + aligned_seq2
            aligned_seq1 = seq1[row - 1] + aligned_seq1
            alignment_indicator = " " + alignment_indicator
            row -= 1

        elif arrow == up_left_arrow:
            # print("match or mismatch")
            # Note that we look up the row-1 and col-1 indexes
            # because there is an extra "-" character at the
            # start of each sequence
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

        elif arrow == left_arrow:
            # print("Insert indel into left sequence")
            aligned_seq1 = "-" + aligned_seq1
            aligned_seq2 = seq2[col - 1] + aligned_seq2
            alignment_indicator = " " + alignment_indicator
            col -= 1

        elif arrow == stop:
            break
        else:
            raise ValueError(
                f"Traceback array entry at {row},{col}: {arrow} is not recognized as an up arrow "
                f"({up_arrow}),left_arrow ({left_arrow}), up_left_arrow ({up_left_arrow}), or a stop ({stop}).")
        # print(traceback_array,-row,-col,traceback_array[-row,-col])
        # print(aligned_seq1)
        # print(alignment_indicator)
        # print(aligned_seq2)
    return aligned_seq1, aligned_seq2


def needleman_wunsch(seq1, seq2):
    traceback_array = _generate_traceback_array(seq1, seq2)
    return _generate_traceback_alignment(traceback_array, seq1, seq2)


def run():
    os.getcwd()
    # within the os module, returns the current working directory of a process.
    cwd = os.getcwd()
    # creates an object known as 'cwd' to which the command os.getcwd() is associated.
    print("Current working directory:{0}".format(cwd))
    # prints the current working directory using the object cwd.
    base_directory = os.path.join(cwd, "Alignment Data0")
    # joins the current working directory and the subfile which we want to read under the object 'basedirectory'
    with os.scandir(base_directory) as folders:
        folders = [folder for folder in folders if folder.is_dir()]
        for folder in folders:
            print(folder)
        # 'scans' basedirectory, iterates through all folders in the subfolder (if any exist), and lists them.
        test_directory = os.path.join(base_directory, folder)
        # creates an object called 'testdirectory' which joins the basedirectory with the specific folder we want to read.
        # we have now told the computer exactly which folders we want to read and how to find them.
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
                aligned_seq1, aligned_seq2 = needleman_wunsch(base_text_contents, text_contents)
                print(base_text,text)
                print(aligned_seq1)
                print(aligned_seq2)


if __name__ == "__main__":
    run()
