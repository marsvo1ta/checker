import json

with (open('report.json', 'r') as f,
      open('formatted_test_results.txt', 'w') as output_file):
    results = json.load(f)
    tests = results['report']['tests']
    count_failed_test = []
    for idx, test in enumerate(tests, start=1):
        status = test['outcome'].upper()
        if status == 'FAILED':
            count_failed_test.append(str(idx))
        test_name = ' '.join(test['name'].split('::')[-2:])
        output = f'{idx}. {status} {test_name}\n\n'
        output_file.write(output)
    length = len(count_failed_test)
    if length == 1:
        output_file.write(f'{length} test failed: {count_failed_test[0]}')
    else:
        output_file.write(f'{length} tests failed: {"".join(count_failed_test)}')
