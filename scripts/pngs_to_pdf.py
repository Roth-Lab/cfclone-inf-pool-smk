
import img2pdf
from pathlib import Path

def main(args):
    
    files = [Path(f).joinpath('src', 'trace_plot.png') for f in args.in_files]

    with open(args.out_file, "wb") as f:
        
        f.write(img2pdf.convert(files))



if __name__ == "__main__":
    
    from argparse import ArgumentParser
    
    default0 = ['/home/matteo/projects/cfdna/wfs/results/cfclone-fwd-sample-dup-clone/TFRI004/out_dir/tmp/snp_0/tc_0/cp_0/sample_outlier_model_1/num_bins_0/sampler_0/cfclone_use_outlier_1/cfclone_use_rdr_1/cfclone_use_baf_1/replicate_0/results/fit/full/src/trace_plot.png']
    
    parser = ArgumentParser()
    
    parser.add_argument("--in-files", "-i", type=str, nargs="+", default=default0)
    
    parser.add_argument("--out-file", "-o", type=str, default="out.pdf")
    
    cli_args = parser.parse_args()
    
    main(cli_args)