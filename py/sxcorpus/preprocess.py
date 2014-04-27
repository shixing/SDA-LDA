import sys

def preprocess_wiki(fn,output_fn):
    f = open(fn)
    output = open(output_fn,'w')
    lid = 0
    for line in f:
        line = line.strip().split()
        line = line[2:-1]
        line = ' '.join(line)
        line = line[1:-4]
        line = line.decode('string_escape')
        output.write(line+'\n')
        lid += 1
    f.close()
    output.close()

def main():
    fn = sys.argv[1]
    output_fn = sys.argv[2]
    preprocess_wiki(fn,output_fn)

if __name__ == '__main__':
    main()
