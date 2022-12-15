
class File:
    name: str
    size: int

    def __init__(self):
        pass

    def __str__(self):
        return f"{self.size} {self.name}"

    def __repr__(self):
        return self.__str__()

class Directory:
    name: str
    parent: object
    directories: list
    files: list[File]

    def __init__(self):
        self.directories = []
        self.files = []

    def get_total_size(self):
        return sum(file.size for file in self.files) \
            + sum(dir.get_total_size() for dir in self.directories)

    def __str__(self):
        return f"dir {self.name}"

    def __repr__(self):
        return self.__str__()

def main():
    with open("input.txt") as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    current_directory: Directory = None
    for line in lines:
        if line.startswith("$"):
            cmd = line.split(" ")[1]
            if cmd == "cd":
                arg = line.split(" ")[2]
                if arg == "..":
                    current_directory = current_directory.parent
                    continue
                new_directory = Directory()
                new_directory.name = arg
                new_directory.parent = current_directory
                if current_directory is not None:
                    current_directory.directories.append(new_directory)
                current_directory = new_directory
            elif cmd == "ls":
                pass
        else:
            size, name = line.split(" ")
            if size == "dir":
                continue
            file = File()
            file.name = name
            file.size = int(size)
            current_directory.files.append(file)
    
    while current_directory.parent is not None:
        current_directory = current_directory.parent

    all_dirs = set()
    find_all_dirs(current_directory, all_dirs)
    
    disk_space_max = 70000000
    disk_space_free = disk_space_max - current_directory.get_total_size()
    needed_space = 30000000
    need_to_free = needed_space - disk_space_free
    
    dirs_by_size = list(all_dirs)
    dirs_by_size.sort(key=lambda x: x.get_total_size())
    for dir in dirs_by_size:
        if dir.get_total_size() >= need_to_free:
            print(dir)
            print(dir.get_total_size())
            break

def find_all_dirs(dir: Directory, all_dirs: set):
    all_dirs.add(dir)
    for sub_dir in dir.directories:
        find_all_dirs(sub_dir, all_dirs)

if __name__ == "__main__":
    main()