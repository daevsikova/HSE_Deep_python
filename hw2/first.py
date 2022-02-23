def create_table(data):
    cols = len(data[0])

    result = "\\begin{center}\\begin{tabular}{" + "|c" * cols + "|}\hline\n"
    result += f" \\\\ \n".join(map(lambda row: " & ".join(row), data))
    result += "\\\\ \n\\hline\\end{tabular}\\end{center}"

    with open("artifacts/latex_table.tex", "w+") as f:
        f.write(result)

if __name__ == "__main__":
    input_data = [
        ['a', 'b', 'c'],
        ['1', '2', '3'],
        ['k', 'e', 'k']
    ]

    create_table(input_data)
