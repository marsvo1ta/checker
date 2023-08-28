input_file = "test_results.txt"
output_file = "formatted_test_results.txt"

with open(input_file, "r") as file:
    lines = file.readlines()

# Extract and format test results
test_results = []

for line in lines:
    if "PASSED" in line or "FAILED" in line:
        parts = line.split(" ")
        test_path = parts[1].split("::")
        module = test_path[1].split("/")[0]
        test_name = test_path[2]
        result = parts[-2]
        result = "PASS" if result == "PASSED" else "FAIL"
        test_results.append(f"{result} {module} {test_name}")

# Save formatted test results to a file
with open(output_file, "w") as file:
    file.write("".join(test_results))

with open(output_file, "r") as res:
    test = res.read()
print("Formatted test results saved to:", output_file)
print(test)
