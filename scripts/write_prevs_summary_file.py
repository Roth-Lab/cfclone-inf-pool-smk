import pandas as pd


def main(args):
    
    df = pd.read_csv(args.prevalence_file, sep="\t")

    df.insert(0, 'coverage', args.coverage)
    
    df.insert(1, 'tumour_content', args.tumour_content)
    
    df.insert(2, 'data_seed', args.data_seed)

    df.to_csv(args.out_file, index=False, sep="\t")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--out-file", required=True)
    
    parser.add_argument("-e", "--prevalence-file", required=True)
    
    parser.add_argument("--coverage", required=True, type=float)
    
    parser.add_argument("--tumour-content", required=True, type=float)
    
    parser.add_argument("--data-seed", required=True, type=int)
    
    cli_args = parser.parse_args()
    
    main(cli_args)
