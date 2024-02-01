input_file = "test_results.txt"
output_file = "formatted_test_results.txt"

with open(input_file, "r") as file:
    lines = file.readlines()

test_results = []

for line in lines:
    if "PASSED" in line or "FAILED" in line:
        parts = line.split(" ")
        test_path = parts[1].split("::")

        # Перевірте, чи у test_path достатньо елементів
        if len(test_path) >= 2:
            module = test_path[1].split("/")[0]
            test_name = test_path[2]

            result = parts[-2]
            result = "PASS" if result == "PASSED" else "FAIL"
            test_results.append(f"{result} {module} {test_name}")
        else:
            print(f"Пропускається рядок: {line}. Невірний формат test_path.")


with open(output_file, "w") as file:
    file.write("\n".join(test_results))

with open(output_file, "r") as res:
    test = res.read()
print("Formatted test results saved to:", output_file)
print(test)
