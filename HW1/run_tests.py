import filecmp
import subprocess
import sys
import os

tests = [
    ('simple', 34685, 462358, 234),
    ('simple', 360000, 500000, 1439),
    ('improved', 460000, 460020, 800),
    ('improved', 578316, 769366, 1203),
    ('improved', 700965, 596288, 480),
    ('improved',408831,681203,871),
    ('improved',411237,489879,421),
    ('simple',30,55,700),
    ('simple',428247,724845,940),
    ('simple',451562,652489,561),
    ('simple',122955,805099,1023)
]

tests_dir = 'tests'
gold_dir = 'gold'

# remove all previous tests from tests dir
for the_file in os.listdir(tests_dir):
    file_path = os.path.join(tests_dir, the_file)
    if os.path.isfile(file_path):
        os.unlink(file_path)

# run all tests
for test in tests:
    test_filename = ''.join(map(lambda x: str(x) + '.',test)) + 'txt'
    test_params = ''.join(map(lambda x: str(x) + ' ',test))
    with open(tests_dir + '/' + test_filename, 'w') as f:
        p = subprocess.Popen(("python", "main.py",  test[0], str(test[1]), str(test[2]), str(test[3])), stdout=f)
    p.wait()
    # remove first line from test result (map load time)
    with open(tests_dir + '/' + test_filename, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(tests_dir + '/' + test_filename, 'w') as fout:
        fout.writelines(data[1:])
    # compare with gold
    test_works = filecmp.cmp(tests_dir + '/' + test_filename, gold_dir + '/' + test_filename)
    if not test_works:
        print('!!FAIL!! ' + test_params)
        sys.exit(1)
    else:
        print('**PASS** ' + test_params)
print('Passed all tests')
sys.exit(0)