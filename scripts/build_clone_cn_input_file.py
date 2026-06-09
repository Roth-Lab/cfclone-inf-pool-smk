import pandas as pd

def main(args):
    
    df_cn = pd.read_csv(args.in_file, sep="\t")

    df_cn["clone"] = df_cn["clone"].astype(int)
    
    # GET CLONES USED IN WHEN SIMULATED DATA 
            
    if args.clone_prevalences_file != 'from_prior':
        
        # IF TSV SPECIFIED, ONLY USE CLONES WITH NON-ZERO PREVALENCE
        
        clones_used = (
            
            pd.read_csv(args.clone_prevalences_file, sep="\t")
            
            # .loc[lambda df: df['prevalence'] > 0.0, 'clone_id']
            
            .loc[lambda df: df['mean_prevalence'] > 0.0, 'clone_id']
            
            .tolist()
        )
        
    else:
        
        # PRIOR ON CLONE PREVALENCES INCLUDES ALL CLONES 
        
        clones_used = df_cn["clone"].unique().tolist()
        
    df_cn_input = df_cn[df_cn["clone"].isin(clones_used)].copy()

    df_cn_input.to_csv(args.out_file, index=False, sep="\t")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in-file", required=True)

    parser.add_argument("-o", "--out-file", required=True)

    parser.add_argument("-c", "--clone-prevalences-file", required=True)

    cli_args = parser.parse_args()

    main(cli_args)
