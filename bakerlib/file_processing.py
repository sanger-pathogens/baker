from os.path import exists


def add_if_not_there(output_file, line_to_add, prefix=[], suffix=[]):
    if not exists(output_file):
        with open(output_file, 'w'):
            pass
    with open(output_file, "r+") as output_file:
        for line in output_file:
            if line_to_add in line:
                break
        else:
            for p in prefix:
                output_file.write(p + '\n')
            output_file.write(line_to_add + "\n")
            for s in suffix:
                output_file.write(s + '\n')
