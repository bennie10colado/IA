import os
import glob
from collections import defaultdict

def read_input(file_path):
    equipment_usage = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                equipment, users = line.split(':')
                users = users.strip(';')
                for user in users.split(';'):
                    if user:
                        name, freq = user.split('=')
                        equipment_usage[equipment].append((name, int(freq)))
    return equipment_usage

def backtracking_schedule(usage, schedules, current_slot=0, user_slots={}, equipment_index=0):
    # Se todos os equipamentos têm 12 alocações, a solução é válida
    if all(len(schedules[equip]) == 12 for equip in schedules):
        return True

    # Se o índice do equipamento excede o número de equipamentos, falha
    if equipment_index >= len(usage):
        return False

    equipment = list(usage.keys())[equipment_index]
    for user, freq in usage[equipment]:
        # Tentativa de alocação em cada slot de tempo
        for time_slot in range(12):
            # Condição para verificar se o aluno já está alocado em outro equipamento no mesmo slot
            if freq > 0 and all(time_slot not in slots for slots in user_slots.values()):
                # Alocação
                schedules[equipment].append((time_slot, user))
                user_slots.setdefault(user, []).append(time_slot)

                # Tentativa de continuar o backtracking com a próxima alocação
                if backtracking_schedule(usage, schedules, current_slot + 1, user_slots, equipment_index):
                    return True
                
                # Desfaz a alocação se não levar a uma solução válida
                schedules[equipment].pop()
                user_slots[user].remove(time_slot)

    # Tentativa com o próximo equipamento se o atual falhar em satisfazer as condições
    if backtracking_schedule(usage, schedules, current_slot, user_slots, equipment_index + 1):
        return True

    return False



def solve(file_path):
    usage = read_input(file_path)
    schedules = defaultdict(list)
    if backtracking_schedule(usage, schedules):
        return schedules
    else:
        return "No valid schedule found."


    

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
