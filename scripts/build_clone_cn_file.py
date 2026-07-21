import numpy as np
import pandas as pd

def main(args):
    df = pd.read_csv(args.in_file, sep="\t")

    df = df[["chrom", "beg", "end", "cluster_id", "cn_A", "cn_B"]].drop_duplicates()

    df = df.rename(
        columns={"cn_A": "cn_a", "cn_B": "cn_b", "beg": "start", "cluster_id": "clone"}
    )

    df["clone"] = df["clone"].astype(int)

    if args.clone_filter_file is not None:
        
        clone_df = pd.read_csv(args.clone_filter_file, sep="\t")

        clone_df = clone_df[clone_df["keep"]]

        clones = clone_df["clone_id"].astype(int).unique()

        df = df[df["clone"].isin(clones)]

    df.to_csv(args.out_file, index=False, sep="\t")


if __name__ == "__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in-file", required=True)

    parser.add_argument("-o", "--out-file", required=True)

    parser.add_argument("-c", "--clone-filter-file", default=None)

    cli_args = parser.parse_args()

    main(cli_args)
