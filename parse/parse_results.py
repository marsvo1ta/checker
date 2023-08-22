import xml.etree.ElementTree as ET

tree = ET.parse('results.xml')
root = tree.getroot()

num_passed = len(root.findall('.//testcase'))
num_failed = len(root.findall('.//testcase/failure'))
num_skipped = len(root.findall('.//testcase/skipped'))

message = f"Test Results:\nPassed: {num_passed}\nFailed: {num_failed}\nSkipped: {num_skipped}"

with open('test_results.txt', 'w') as f:
    f.write(message)
