

class State:
    def __init__(self) -> None:
        pass


def preprocess(text):
    text = text.lower()
    for i,ch in enumerate(text):
        if ch in "!#$%&'()*+,-/:;<=>?@[\]^_{|}~`":
            text[i] = ""
    
    sentences =  text.split()
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def levenshtien_dist(s1:str,s2:str):
    n,m = len(s1),len(s2)
    
    return 

def heuristic():
    return

def a_start_search():
    return

def main():
    test_case = "./test_cases/test1/" # Edit case
    file1 = open(test_case+'file1.txt','r')
    file2 = open(test_case+'file2.txt','r')
    
    text1 = preprocess(file1.read())
    text2 = preprocess(file2.read())
    for each in text1:
        print(each)
        
    for each in text2:
        print(each)

    file1.close()
    file2.close()

if __name__ == "__main__":
    main()