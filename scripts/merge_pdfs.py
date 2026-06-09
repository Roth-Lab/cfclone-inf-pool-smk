from pypdf import PdfWriter

def main(args):
    
    merger = PdfWriter()
    
    for pdf in args.in_files:
        
        merger.append(pdf)
        
    merger.write(args.out_file)
    
    merger.close()
    

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i", "--in-files", nargs="+", required=True)
    
    parser.add_argument("-o", "--out-file", required=True)

    cli_args = parser.parse_args()

    main(cli_args)
   