import os
import glob

def read_files(directory):
    file_paths = glob.glob(os.path.join(directory, 'entrada_*.txt'))
    results = []
    for file_path in sorted(file_paths):
        with open(file_path, 'r') as file:
            content = file.read()
            equipments, students = parse_content(content)
            allocation_result = allocate_equipments(equipments, students)
            results.append((file_path, allocation_result))
    return results

def parse_content(content):
    equipments = {}
    students_set = set()
    lines = content.strip().split('\n')
    for line in lines:
        equipment_name, students_str = line.split(':')
        students = students_str.split(';')[:-1]
        equipments[equipment_name] = {student.split('=')[0]: int(student.split('=')[1]) for student in students}
        students_set.update(equipments[equipment_name].keys())
    return equipments, list(students_set)


def allocate_equipments(equipments, students):
    allocations = {equipment: [None] * 12 for equipment in equipments}
    student_intervals = {student: set() for student in students}

    def backtrack(equip_index, interval):
        if interval == 12:
            return True if equip_index >= len(equipments) - 1 else backtrack(equip_index + 1, 0)
        
        equipment = list(equipments)[equip_index]
        for student, need in equipments[equipment].items():
            if need > 0 and interval not in student_intervals[student]:
                equipments[equipment][student] -= 1
                allocations[equipment][interval] = student
                student_intervals[student].add(interval)

                if backtrack(equip_index, interval + 1):
                    return True

                equipments[equipment][student] += 1
                allocations[equipment][interval] = None
                student_intervals[student].remove(interval)
        
        return False if interval == 0 else backtrack(equip_index, interval + 1)

    if backtrack(0, 0):
        return allocations
    else:
        return False


def save_output(output_directory, file_path, result):
    output_file_name = os.path.basename(file_path).replace('entrada', 'saida')
    output_file_path = os.path.join(output_directory, output_file_name)
    with open(output_file_path, 'w') as file:
        for equipment, slots in result.items():
            file.write(f"{equipment}:")
            for student in slots:
                if student:
                    file.write(f"-{student} ")
            file.write("\n")

def main():
    input_directory = '../entrada_50'
    output_directory = 'saida'
    os.makedirs(output_directory, exist_ok=True)

    results = read_files(input_directory)
    for file_path, result in results:
        if result:
            save_output(output_directory, file_path, result)
        else:
            print(f'Allocation failed for {file_path}')

if __name__ == "__main__":
    main()
