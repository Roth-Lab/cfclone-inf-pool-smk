import pandas as pd


def main(args):
   
    df_e = pd.read_csv(args.evidence_file, sep="\t")
    
    df_e = df_e.pivot(index="restart", columns="run_type", values="evidence")
    
    df_e = df_e.reset_index()
    
    df = pd.read_csv(args.tumour_content_file, sep="\t")

    df.add_prefix("tumour_content_", axis=1)
    
    df = df.merge(df_e, on="restart")
    
    df['bayes_factor'] = df["full"] - df["normal"]
    
    df = df.rename(columns={"full": "full_evidence", "normal": "normal_evidence"})
    
    df.insert(0, 'coverage', args.coverage)
    
    df.insert(1, 'tumour_content', args.tumour_content)
    
    df.insert(2, 'data_seed', args.data_seed)

    df.to_csv(args.out_file, index=False, sep="\t")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--out-file", required=True)
    
    parser.add_argument("-e", "--evidence-file", required=True)
    
    parser.add_argument("-t", "--tumour-content-file", required=True)
    
    parser.add_argument("--coverage", required=True, type=float)
    
    parser.add_argument("--tumour-content", required=True, type=float)
    
    parser.add_argument("--data-seed", required=True, type=int)
    
    cli_args = parser.parse_args()
    
    main(cli_args)
