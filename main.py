from pathlib import Path
import re
import sys
import shutil

def main():
    contest_id = sys.argv[1].strip()
    path = Path(__file__).parent / 'input' / contest_id

    a = sorted(path.glob('*.py3'))
    PATTERN = r'(.*)_(.*)_(.*)_(.*)\((.*)\)\.py3'
    d = {
        '1': {},
        '2': {},
        '3': {},
        '4': {},
        '5': {},
    }
    
    e = {
        '1': {},
        '2': {},
        '3': {},
        '4': {},
        '5': {},
    }
    for i in a:
        results = re.match(PATTERN, i.name)
        if results:
            submission_id, problem_id, ac_status, user_id, user_name = results.groups()
            if ac_status == 'AC':
                tmp = (int(submission_id), i, i.read_text())
                if user_name not in d[problem_id]:
                    d[problem_id][user_name] = tmp
                else:
                    if tmp[0] > d[problem_id][user_name][0]:
                        d[problem_id][user_name] = tmp
    for problem_id, user_info in d.items():
        for user_name, (_, file_name, source) in user_info.items():
            if source not in e[problem_id]:
                e[problem_id][source] = []
            e[problem_id][source].append(file_name)
        groupid = 0
        for source, file_names in e[problem_id].items():
            if len(file_names) > 1:
                print(problem_id, [x.name for x in file_names])
                groupid += 1
                dst_dir = Path(__file__).parent / 'output' / contest_id / problem_id / str(groupid)
                dst_dir.mkdir(parents=True, exist_ok=True)
                for file_name in file_names:
                    # copy to dst_dir
                    shutil.copy(file_name, dst_dir)
        print("++++++++++")

if __name__ == '__main__':
    main()