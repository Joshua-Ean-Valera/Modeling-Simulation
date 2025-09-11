def magic_info(mat):
    n = len(mat)
    row_sums = [sum(row) for row in mat]
    col_sums = [sum(mat[i][j] for i in range (n)) for j in range(n)]
    diag_main = sum(mat[i][i] for i in range(n))
    diag_anti = sum(mat[i][n - 1 - i] for i in range(n))
    all_sums = set(row_sums + col_sums + [diag_main, diag_anti])
    is_magic = (len(all_sums) == 1)
    return row_sums, col_sums, [diag_main, diag_anti], is_magic
        
def output(output_lines, filename="output.out"):
    with open(filename, "w") as f:
        for line in output_lines:
            f.write(line + "\n")

def main():
    with open("activity1_test_cases.in") as f:
        lines = f.read().splitlines()
    
    output_lines = []    
    test_num = 1    
    for line in lines:
        if not line.strip():
            continue
        
        try:
            mat = eval(line.strip())
        except Exception:
            msg = f"Invalid input for Test #{test_num}: Could not parse line \n"
            print(msg)
            output_lines.append(msg)
            test_num += 1
            continue
        
        r = len(mat)
        c = len(mat[0]) if r > 0 else 0
        if not all(len(row) == c for row in mat):
            msg = f"Invalid input for Test {test_num}: Matrix should be square (number of rows should be equal to number of columns)\n"
            print(msg)
            output_lines.append(msg)
            test_num += 1
            continue
        
        if r != c:
            msg = f"Invalid input for Test {test_num}: Matrix should be square (number of rows should be equal to number of columns)\n"
            print(msg)
            output_lines.append(msg)
            test_num += 1
            continue
        
        matrix_str = "\n".join("\t" .join(str(x) for x in row) for row in mat)
        print(matrix_str)
        output_lines.append(matrix_str)
        row_sums, col_sums, diag_sums, is_magic = magic_info(mat)
        if is_magic:
            msg1 = f"Test case {test_num}: True (Sum: {row_sums[0]})"
            msg2 = f"Row Sums: {row_sums}"
            msg3 = f"Column Sums: {col_sums}"
            msg4 = f"Diagonal Sums: {diag_sums}\n"
            print(msg1)
            print(msg2)
            print(msg3)
            print(msg4)
            output_lines.extend([msg1, msg2, msg3, msg4])
        else:
            msg = f"Test case {test_num}: False\n"
            print(msg)
            output_lines.append(msg)
        print()
        test_num += 1
        
    output(output_lines)    
    
if __name__ == "__main__":
    main()
            