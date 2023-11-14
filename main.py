from pathlib import Path
import re
import sys
import shutil

def main():
    contest_id = sys.argv[1].strip()
    path = Path(__file__).parent / 'input' / contest_id

    a = sorted(path.glob('*.py3'))
    PATTERN = r'(.*)_(.*)_(.*)_(.*)\((.*)\)\.py3'
    d = {}
    e = {}
    for i in a:
        results = re.match(PATTERN, i.name)
        if results:
            submission_id, problem_id, ac_status, user_id, user_name = results.groups()
            if problem_id not in d:
                d[problem_id] = {}
                e[problem_id] = {}
            if ac_status == 'AC':
                tmp = (int(submission_id), i, '\n'.join( x.strip() for x in i.read_text().split('\n') ))
                if user_name not in d[problem_id]:
                    d[problem_id][user_name] = tmp
                else:
                    if tmp[0] > d[problem_id][user_name][0]:
                        d[problem_id][user_name] = tmp

    user2problem = {}
    for problem_id, user_info in d.items():
        for user_name, (_, file_name, source) in user_info.items():
            if source not in e[problem_id]:
                e[problem_id][source] = []
            e[problem_id][source].append((file_name, user_name))
        groupid = 0
        for source, fu in e[problem_id].items():
            if len(fu) > 1:
                print(problem_id, [x.name for x, _ in fu])
                for _, user_name in fu:
                    if user_name not in user2problem:
                        user2problem[user_name] = set()
                    user2problem[user_name].add(problem_id)
                groupid += 1
                dst_dir = Path(__file__).parent / 'output' / contest_id / problem_id / str(groupid)
                dst_dir.mkdir(parents=True, exist_ok=True)
                for file_name, _ in fu:
                    # copy to dst_dir
                    shutil.copy(file_name, dst_dir)
        print("++++++++++")
    
    print()
    print("Summary:")
    for user_name, problem_ids in user2problem.items():
        print(user_name, sorted(problem_ids))

if __name__ == '__main__':
    main()