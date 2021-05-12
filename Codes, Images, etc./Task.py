from tkinter import *

class Task:

    def __init__(self, name, subject, date, completed=False):
        self.name = name
        self.subject = subject
        self.date = date
        self.completed = completed

    def make_all_objects(self, filename):
        pass

    @staticmethod
    def get_tasks_from_line(date, subject, line):
        first_word = line.split(":")[0]
        word_list = line.split(",")
        # generate a new list without the subject name
        new_word_list = [word.replace(f"{first_word}: ","").strip(" \n") for word in word_list]

        # make every task an object and put the objects into a list
        task_object_list = []
        for word in new_word_list:
            if "(+)" in word:
                completed = True
            else:
                completed = False
            task_object_list.append(Task(word.strip("()").strip("(+)"), subject, date, completed))

        return task_object_list


    @staticmethod
    def date_subject_finder(filename):
        subjects = []

        with open(filename, "r") as f:
            lines = f.readlines()
            # categorize the lines by their first word
            for line in lines:
                first_word = line.split(":")[0]
                # find all the subjects
                if first_word != "Date" and first_word not in subjects and first_word != "\n":
                    subjects.append(first_word)
                # keep updating the date
                else:
                    if first_word == "Date":
                        date = line.split(": ")[1].strip("\n")

#        print ("\n","Subjects: ", subjects, "\n")

        return date, subjects

    @staticmethod
    def add_to_today(filename, tasks_list):
        with open(filename, "r") as f:
            lines = f.readlines()

            print ("All lines: ", lines)

            # Find the lastest date and all the subjects
            date, subject_list = Task.date_subject_finder(filename)
            # Create blank list to insert tasks (categorized by subject)
            subject_task_list = list(" "*len(subject_list))

            # Put tasks in the list created above
            for line in lines:
                first_word = line.split(":")[0]
                if first_word in subject_list:
                    index = subject_list.index(first_word)
                    # Find the tasks (get rid of the subject name and "next line" operator)
                    subject_task_list[index] = line.replace(f"{first_word}: ", "").strip("\n").strip("")

            # Add new tasks into the list
            new_subject_task_list = []
            for index, subject_task in enumerate(subject_task_list):
                # Do not change the original file if add nothing
                if len(tasks_list[index]) == 0 or tasks_list[index][0] == "":
                    new_subject_task_list.append(f"{subject_list[index]}: {subject_task}\n")
                else:
                    task_string = ""
                    for i, task in enumerate(tasks_list[index]):
                        if i != len(tasks_list[index]) - 1:
                            task_string += f"{task}(),"
                        else:
                            task_string += f"{task}()\n"
                    # Replace "None" by new tasks if there was no tasks before
                    if subject_task == "None(+)":
                        new_subject_task_list.append(f"{subject_list[index]}: {task_string}")
                    else:
                        new_subject_task_list.append(f"{subject_list[index]}: {subject_task},{task_string}")

            # Create a new lines list with new tasks added
            new_lines_list = lines.copy()
            index = lines.index(f"Date: {date}\n")
            new_lines_list[index+1:len(lines)] = new_subject_task_list

            # write the new line list to the file
            with open(filename, "w") as f:
                for new_lines in new_lines_list:
                    f.write(new_lines)


    @staticmethod
    def add_to_tomorrow(date, tasks_list, filename):
        with open(filename, "a") as f:

            latest_date, subject_list = Task.date_subject_finder(filename)

            # start a new date section in the file
            f.write(f"\nDate: {date}\n")
            for index, subject in enumerate(subject_list):
                # print (subject_list)
                # put the tasks in one subject in a string (if there is at least one task belong to that subject)
                # insert "None" if add nothing to the subject
                task_string = ""
                if len(tasks_list[index]) == 0 or tasks_list[index][0] == "":
                    task_string = "None(+)\n"
                else:
                    for i, task in enumerate(tasks_list[index]):
                        # Add "Next line" operator to the last element
                        if i != len(tasks_list[index]) - 1:
                            task_string += f"{task}(),"
                        else:
                            task_string += f"{task}()\n"
                f.write(f"{subject}: {task_string}")

    @staticmethod
    def find_date(filename):
        with open(filename, "r") as f:
            lines = f.readlines()

            # filter out the line that indicate date
            date_list = []
            for line in lines:
                first_word = line.split(":")[0]
                if first_word == "Date":
                    date_list.append(line.strip("Date: ").strip("\n"))

            return date_list

    # filter when read the file
    @staticmethod
    def filter(date,subjects,completed,filename):
        with open(filename, "r") as f:
            line_list = f.readlines()

            # get the latest day and a list of all subjects
            lastest_date, all_subjects = Task.date_subject_finder(filename)

            # implement the filter process if the input is not "All"
            if date != "All":
                for i,line in enumerate(line_list):
                    if date in line:
                        date_index = i
                # pick all the tasks from that day
                first_filtered_line_list = line_list[date_index:date_index+len(all_subjects)+1]
            else:
                # return the unchanged list if the input is "All"
                first_filtered_line_list = line_list

            # implement the filter process if the input is not "All"
            second_filtered_line_list = []
            if subjects != "All":
                for line in first_filtered_line_list:
                    # still keep the "date" line in the list
                    if "Date" in line:
                        second_filtered_line_list.append(line)
                    # only add the lines with the appropriate subject
                    for subject in subjects:
                        if subject in line:
                            second_filtered_line_list.append(line)
            else:
                # return the unchanged list if the input is "All"
                second_filtered_line_list = first_filtered_line_list

            # implement the filter process if the input is not "All"
            third_filtered_line_list = []
            if completed != "All":
                for line in second_filtered_line_list:
                    # still keep the "date" line in the list
                    if "Date: " in line:
                        third_filtered_line_list.append(line)
                    else:
                        # divide the line into tasks and filter out the tasks that has been completed
                        tasks = line.split(",")
                        tasks_copy = tasks.copy()
                        subject = tasks_copy[0].split(":")[0]
                        tasks[0] = tasks[0].strip(f"{subject}: ")
                        # put the tasks back together into a string
                        if line != '\n':
                            if completed == "Completed":
                                new_line_string = ",".join([task for task in tasks if "(+)" in task])
                                third_filtered_line_list.append(f"{subject}: {new_line_string}")
                            else:
                                new_line_string = ",".join([task for task in tasks if "(+)" not in task])
                                third_filtered_line_list.append(f"{subject}: {new_line_string}")
                        else:
                            third_filtered_line_list.append('\n')
            else:
                # return the unchanged list if the input is "All"
                third_filtered_line_list = second_filtered_line_list

        return third_filtered_line_list

    @staticmethod
    def add_new_subject_to_file(filename, subject_name):
        latest_date, subject_list = Task.date_subject_finder(filename)
        subject_list_lower = [subject.lower() for subject in subject_list]

        # repeat repeated if the subject already existed (will pop up a window)
        if subject_name.lower() in subject_list_lower:
            return "Repeated"
        else:
            with open(filename, "r") as f:
                # get the texts in the file
                lines = f.readlines()

                # make a copy of the texts to be modified
                lines_copy = lines.copy()

                # since the list gets longer when keep adding the subject,
                # so add a variable to keep track of how many times the subject has been added
                add_counter = 0
                for i, line in enumerate(lines_copy):
                    if subject_list[-1] in line:
                        lines.insert(i+1+add_counter, f"{subject_name}: None(+)\n")
                        add_counter += 1

            # write the new content to the file (overwrite the previous version)
            with open(filename, "w") as f:
                for line in lines:
                    f.write(line)

            return "Success"

    @staticmethod
    def make_it_complete(filename, completed_objects):
        with open(filename, "r") as f:
            lines = f.readlines()
            lines_copy = lines.copy()

        latest_date,subjects = Task.date_subject_finder(filename)
        latest_date_list = [line for line in lines if latest_date in line]
        latest_date_index = lines.index(latest_date_list[0])

        for index, line in enumerate(lines_copy):
            if index > latest_date_index:
                for object in completed_objects:
                    if object.subject == line.split(":")[0]:
                        lines[index] = lines[index].replace(f"{object.name}()", f"{object.name}(+)")

        with open(filename, "w") as f:
            for line in lines:
                f.write(line)
