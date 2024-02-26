import json

with (open('report.json', 'r') as f,
      open('formatted_test_results.txt', 'w') as output_file):
    results = json.load(f)
    tests = results['report']['tests']
    for test in tests:
        status = test['outcome'].upper()
        test_name = ' '.join(test['name'].split('::')[-2:])
        output = f'{status} {test_name}\n\n'
        output_file.write(output)


