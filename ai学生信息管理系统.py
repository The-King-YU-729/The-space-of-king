import json

# 这是一个“学生管理系统”的主文件。
# 使用 JSON 文件来保存学生数据，程序启动时会自动读取 students.json。
# 通过命令行输入来实现：添加、查看、查找、删除学生信息。

# JSON 文件名常量：数据存储位置
FILE_NAME = "students.json"


class StudentManager:
    # 构造函数：创建对象时自动加载已有学生数据
    def __init__(self):
        # self.students 用来保存所有学生信息
        # 它的类型是列表，列表中的每一项是一个字典，表示一个学生
        self.students = self.load_students()

    # 读取学生数据：从 JSON 文件中读取内容
    def load_students(self):
        try:
            # 打开文件并读取内容
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)  # 把 JSON 字符串转换成 Python 对象

                # 只有当文件内容是列表时，才认为是合法数据
                # 例如：[ {"name": "张三", "age": 18, "score": 90.5}, ... ]
                if isinstance(data, list):
                    return data
                return []
        except FileNotFoundError:
            # 如果文件不存在，说明还没有学生数据，返回空列表
            return []
        except json.JSONDecodeError:
            # 如果 JSON 格式有问题，说明文件内容损坏或不是标准 JSON
            print("文件内容异常，已按空列表处理。")
            return []

    # 保存学生数据：把内存中的列表写回 JSON 文件
    def save_students(self):
        try:
            # "w" 表示写入模式；ensure_ascii=False 保证中文不被转义
            # indent=2 让 JSON 文件格式更整齐，方便查看
            with open(FILE_NAME, "w", encoding="utf-8") as f:
                json.dumps(self.students, f, ensure_ascii=False, indent=2)
            print("保存成功")
        except Exception as e:
            # 任何写入错误都会被捕获，并打印错误信息
            print(f"保存失败：{e}")

    # 添加学生：从键盘读取姓名、年龄、成绩并保存到列表中
    def add_student(self):
        # 读取姓名并去掉前后空格
        name = input("请输入学生姓名：").strip()
        if not name:
            print("姓名不能为空。")
            return

        # 年龄必须是整数，所以用 int() 转换
        try:
            age = int(input("请输入学生年龄："))
        except ValueError:
            print("年龄必须是数字。")
            return

        # 成绩通常可能带小数，所以用 float() 转换
        try:
            score = float(input("请输入学生成绩："))
        except ValueError:
            print("成绩必须是数字。")
            return

        # 每个学生用一个字典表示
        # 例如：{"name": "李四", "age": 20, "score": 88.5}
        student = {
            "name": name,
            "age": age,
            "score": score
        }

        # 把学生对象加入列表
        self.students.append(student)
        print("学生添加成功")

        # 添加后立即写入文件，保证数据不会丢失
        self.save_students()

    # 查看学生列表：把所有学生按顺序打印出来
    def show_students(self):
        if not self.students:
            print("当前没有学生信息。")
            return

        print("学生列表：")
        # enumerate(self.students, start=1) 让序号从 1 开始
        for i, student in enumerate(self.students, start=1):
            # student 是字典，student['name'] 读取姓名
            print(f"{i}. {student['name']} | 年龄: {student['age']} | 成绩: {student['score']}")

    # 查找学生：根据姓名搜索学生信息
    def search_student(self):
        name = input("请输入要查找的学生姓名：").strip()
        found = False  # 标记是否找到

        # 遍历所有学生，逐个检查名字
        for student in self.students:
            if student["name"] == name:
                print(f"找到学生：{student}")
                found = True
                break

        if not found:
            print("没有找到该学生。")

    # 删除学生：根据姓名删除对应记录
    def delete_student(self):
        name = input("请输入要删除的学生姓名：").strip()

        # 直接循环列表，找到名字相同的学生就删除
        for student in self.students:
            if student["name"] == name:
                self.students.remove(student)
                print(f"已删除学生：{name}")
                self.save_students()  # 删除后立刻保存到文件
                return

        print("没有找到该学生。")

    # 程序主菜单：循环展示选项，直到用户选择退出
    def run(self):
        while True:
            print("\n===== 学生管理系统 =====")
            print("1. 添加学生")
            print("2. 查看学生")
            print("3. 查找学生")
            print("4. 删除学生")
            print("5. 退出")

            choice = input("请选择功能（1-5）：").strip()

            # 根据用户输入执行不同功能
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.show_students()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.delete_student()
            elif choice == "5":
                print("退出系统。")
                break
            else:
                print("输入错误，请重新选择。")


# 程序启动入口：创建 StudentManager 对象并运行菜单循环
if __name__ == "__main__":
    manager = StudentManager()
    manager.run()