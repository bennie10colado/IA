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
    student_times = {student: 0 for student in students}
    for interval in range(12):
        for equipment in equipments:
            for student, times_needed in equipments[equipment].items():
                if times_needed > 0 and student_times[student] <= interval:
                    allocations[equipment][interval] = student
                    equipments[equipment][student] -= 1
                    student_times[student] += 1
                    break
    return allocations

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
