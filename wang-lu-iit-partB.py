import gzip, os

def main():
    gzfile = 'wang-lu-iit-partA-result.gz'
    txtfile = 'wang-lu-iit-partB-result.txt'
    
    if not os.path.exists(gzfile):
        print('ERROR: the input file %s does not exists!' % gzfile)
    
    fi = gzip.open(gzfile, 'rb')
    fo = open(txtfile, 'wb')
    
    fo.write(fi.read())
    fi.close()
    fo.close()    

if __name__ == '__main__':
    main()