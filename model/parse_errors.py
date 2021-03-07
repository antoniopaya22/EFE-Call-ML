
def correct_errors(file)
    correct_logs = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                if row[0] == 6:
                    row[0]
            line_count += 1