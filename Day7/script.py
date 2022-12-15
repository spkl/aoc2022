
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

    small_dirs = set()
    find_small_dirs(current_directory, small_dirs)
    print(small_dirs)
    size_of_small_dirs = sum(dir.get_total_size() for dir in small_dirs)
    print(size_of_small_dirs)

def find_small_dirs(dir: Directory, small_dirs: set):
    if dir.get_total_size() < 100000:
        small_dirs.add(dir)
    for sub_dir in dir.directories:
        find_small_dirs(sub_dir, small_dirs)

if __name__ == "__main__":
    main()