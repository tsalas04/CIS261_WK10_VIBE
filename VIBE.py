# VIBE.py
# Student Grade Calculator

import os
import sys
import termios
import tty

STORAGE_FILE = "student_grades.txt"


class Student:
	def __init__(self, name, sid, test1, test2, test3):
		self.name = name
		self.id = sid
		self.test1 = float(test1)
		self.test2 = float(test2)
		self.test3 = float(test3)
		self.average = 0.0
		self.grade = ""
		self.calculate()

	def calculate(self):
		self.average = round((self.test1 + self.test2 + self.test3) / 3.0, 2)
		avg = self.average
		if avg >= 90:
			self.grade = "A"
		elif avg >= 80:
			self.grade = "B"
		elif avg >= 70:
			self.grade = "C"
		elif avg >= 60:
			self.grade = "D"
		else:
			self.grade = "F"

	def to_record(self):
		return f"{self.name}|{self.id}|{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}\n"

	@staticmethod
	def from_record(line):
		parts = line.strip().split("|")
		if len(parts) < 7:
			raise ValueError("Invalid record format")
		name, sid, t1, t2, t3, avg, grade = parts[:7]
		s = Student(name, sid, float(t1), float(t2), float(t3))
		# ensure stored average/grade are preserved (or recalculated)
		s.average = round(float(avg), 2)
		s.grade = grade
		return s


def read_single_key():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(fd)
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch


def load_records(filepath):
	students = []
	if not os.path.exists(filepath):
		return students
	try:
		with open(filepath, "r", encoding="utf-8") as f:
			for line in f:
				line = line.strip()
				if not line:
					continue
				try:
					s = Student.from_record(line)
					students.append(s)
				except Exception:
					# skip malformed lines
					continue
	except Exception as e:
		print(f"Error loading records: {e}")
	return students


def save_records(filepath, students):
	try:
		with open(filepath, "w", encoding="utf-8") as f:
			for s in students:
				f.write(s.to_record())
		print(f"Saved {len(students)} records to {filepath}")
	except Exception as e:
		print(f"Error saving records: {e}")


def add_student_interactive(students):
	try:
		name = input("Enter student name: ").strip()
		sid = input("Enter student ID: ").strip()
		t1 = float(input("Enter Test1 score: "))
		t2 = float(input("Enter Test2 score: "))
		t3 = float(input("Enter Test3 score: "))
	except ValueError:
		print("Invalid numeric input. Student not added.")
		return
	s = Student(name, sid, t1, t2, t3)
	students.append(s)
	print(f"Added {name} with average {s.average:.2f} ({s.grade})")


def display_students(students):
	if not students:
		print("No student records to display.")
		return
	header = f"{'Name':20} | {'ID':10} | {'T1':6} | {'T2':6} | {'T3':6} | {'Avg':6} | {'Grade':5}"
	print(header)
	print('-' * len(header))
	for s in students:
		print(f"{s.name:20} | {s.id:10} | {s.test1:6.2f} | {s.test2:6.2f} | {s.test3:6.2f} | {s.average:6.2f} | {s.grade:5}")


def class_statistics(students):
	if not students:
		print("No records for statistics.")
		return
	avgs = [s.average for s in students]
	highest = max(avgs)
	lowest = min(avgs)
	cls_avg = round(sum(avgs) / len(avgs), 2)
	print(f"Highest average: {highest:.2f}")
	print(f"Lowest average:  {lowest:.2f}")
	print(f"Class average:   {cls_avg:.2f}")


def search_student(students):
	name = input("Enter student name to search (case-insensitive): ").strip().lower()
	found = [s for s in students if s.name.lower() == name]
	if not found:
		print("No student found with that name.")
		return
	display_students(found)


def main():
	students = load_records(STORAGE_FILE)
	print(f"Loaded {len(students)} records from {STORAGE_FILE}")

	while True:
		print('\nMain Menu:')
		print('1) Add new student')
		print('2) Display all students')
		print('3) Class statistics')
		print('4) Search student by name')
		print('5) Save records')
		print('Press ESC to exit')
		print('Choose an option and press Enter, or press a single key for quick action: ', end='', flush=True)

		# read a single key without waiting for Enter
		ch = read_single_key()
		# If Enter was pressed (rare), prompt for input normally
		if ch == '\r' or ch == '\n':
			choice = input().strip()
		else:
			print(ch)
			choice = ch

		if choice == '\x1b':  # ESC
			print('Exiting...')
			break
		choice = choice.strip().lower()
		if choice == '1':
			add_student_interactive(students)
		elif choice == '2':
			display_students(students)
		elif choice == '3':
			class_statistics(students)
		elif choice == '4':
			search_student(students)
		elif choice in ('5', 's'):
			save_records(STORAGE_FILE, students)
		else:
			print('Unknown option. Please try again.')

	# Save on exit
	save_records(STORAGE_FILE, students)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\nInterrupted. Saving records before exit...')
		# attempt to save
		try:
			students  # type: ignore
		except NameError:
			pass
		else:
			save_records(STORAGE_FILE, students)
#Tomas Salas
#CIS261
#WK10 VIBE Coding

"Hello World"