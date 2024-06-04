import json
import json

def load_data(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data


class Class:

    def __init__(self, groups, teacher, subject, type, duration, classrooms):
        self.groups = groups
        self.teacher = teacher
        self.subject = subject
        self.type = type
        self.duration = duration
        self.classrooms = classrooms

    def __str__(self):
        return "Groups {} | Teacher '{}' | Subject '{}' | Type {} | {} hours | Classrooms {} \n"\
            .format(self.groups, self.teacher, self.subject, self.type, self.duration, self.classrooms)

    def __repr__(self):
        return str(self)


class Classroom:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return "{} - {} \n".format(self.name, self.type)

    def __repr__(self):
        return str(self)


class Data:

    def __init__(self):
        self.groups = {}
        self.teachers = {}
        self.classes = {}
        self.classrooms = {}

    def load_data(self, file_path, teachers_empty_space, groups_empty_space, subjects_order):
        """
        Loads and processes input data, initialises helper structures.
        :param file_path: path to file with input data
        :param teachers_empty_space: dictionary where key = name of the teacher, values = list of rows where it is in
        :param groups_empty_space: dictionary where key = group index, values = list of rows where it is in
        :param subjects_order: dictionary where key = (name of the subject, index of the group), value = [int, int, int]
        where ints represent start times (row in matrix) for types of classes P, V and L respectively. If start time is -1
        it means that that subject does not have that type of class.
        :return: None
        """
        with open(file_path) as file:
            data = json.load(file)

        # classes: dictionary where key = index of a class, value = class
        classes = {}
        # classrooms: dictionary where key = index, value = classroom name
        classrooms = {}
        # teachers: dictionary where key = teachers' name, value = index
        teachers = {}
        # groups: dictionary where key = name of the group, value = index
        groups = {}
        class_list = []

        for cl in data['Casovi']:
            new_group = cl['Grupe']
            new_teacher = cl['Nastavnik']

            # initialise for empty space of teachers
            if new_teacher not in teachers_empty_space:
                teachers_empty_space[new_teacher] = []

            new = Class(new_group, new_teacher, cl['Predmet'], cl['Tip'], cl['Trajanje'], cl['Ucionica'])
            # add groups
            for group in new_group:
                if group not in groups:
                    groups[group] = len(groups)
                    # initialise for empty space of groups
                    groups_empty_space[groups[group]] = []

            # add teacher
            if new_teacher not in teachers:
                teachers[new_teacher] = len(teachers)
            class_list.append(new)

        # shuffle mostly because of teachers
        random.shuffle(class_list)
        # add classrooms
        for cl in class_list:
            classes[len(classes)] = cl

        # every class is assigned a list of classrooms he can be in as indexes (later columns of matrix)
        for type in data['Ucionice']:
            for name in data['Ucionice'][type]:
                new = Classroom(name, type)
                classrooms[len(classrooms)] = new

        # every class has a list of groups marked by its index, same for classrooms
        for i in classes:
            cl = classes[i]

            classroom = cl.classrooms
            index_classrooms = []
            # add classrooms
            for index, c in classrooms.items():
                if c.type == classroom:
                    index_classrooms.append(index)
            cl.classrooms = index_classrooms

            class_groups = cl.groups
            index_groups = []
            for name, index in groups.items():
                if name in class_groups:
                    # initialise order of subjects
                    if (cl.subject, index) not in subjects_order:
                        subjects_order[(cl.subject, index)] = [-1, -1, -1]
                    index_groups.append(index)
            cl.groups = index_groups

        self.groups = groups
        self.teachers = teachers
        self.classes = classes
        self.classrooms = classrooms
