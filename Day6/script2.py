SEARCH_LENGTH = 14

def main():
    with open("input.txt") as f:
        inputs = f.readlines()
    
    for input in inputs:
        buffer = list()
        for index, character in enumerate(input):
            buffer.append(character)
            if len(buffer) > SEARCH_LENGTH:
                del buffer[0]
            if len(set(buffer)) == SEARCH_LENGTH:
                print(index + 1)
                break

            

if __name__ == "__main__":
    main()