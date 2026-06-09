import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt


colour_blind_friendly = {
    'blue': '#377eb8',
    'orange': '#ff7f00',
    'green': '#4daf4a',
    'pink': '#f781bf',
    'brown': '#a65628',
    'purple': '#984ea3',
    'grey': '#999999',
    'red': '#e41a1c',
    'yellow': '#dede00'
}


plot_settings = {
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    # "axes.labelweight": "bold",
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 8,
}


def plot(
    df_plot: pd.DataFrame,
    xlims: tuple[float, float] | None = None,
    figsize: tuple[float, float] | None = None,
    show: bool = False,
    output_path: str | None = None,
) -> None:
    with plt.rc_context(plot_settings):
        _plot(
            df_plot=df_plot,
            xlims=xlims,
            figsize=figsize,
            show=show,
            output_path=output_path,
        )
        
    
def _plot(
    df_plot: pd.DataFrame,
    xlims: tuple[float, float] | None = None,
    figsize: tuple[float, float] | None = None,
    show: bool = False,
    output_path: str | None = None,
) -> None:
    """
    Args:
        df_plot (pd.DataFrame): with the following columns:
            [
                'coverage',
                'tumour_content',
                'replicate',
                'mean',                 # cfclone 
                'median',               # cfclone
                'lower_hdi',            # cfclone
                'upper_hdi',            # cfclone 
                'normal_evidence',      # cfclone
                'full_evidence',        # cfclone
                'bayes_factor',         # cfclone
            ]
    """
    tumour_content = df_plot['tumour_content'].unique().tolist()
    num_covs = len(tumour_content)
    
    num_cols = int(np.ceil(np.sqrt(num_covs)))
    num_rows = int(np.ceil(num_covs / num_cols))
    
    if figsize is None:
        figsize = (num_cols * 5, num_rows * 5)
    
    fig = plt.figure(figsize=figsize, constrained_layout=True)
    gs = fig.add_gridspec(nrows=num_rows, ncols=num_cols)
    
    for i in range(num_rows):
        for j in range(num_cols):
            ax = fig.add_subplot(gs[i, j])
            idx = i * num_cols + j
            if idx < num_covs:
                df = df_plot[df_plot['tumour_content'] == tumour_content[idx]]
                plot_bf(
                    df=df,
                    xlims=xlims,
                    ax=ax,
                )
            else:
                ax.axis('off')
                
    fig.align_labels()
                
    if output_path is not None:
        plt.savefig(output_path)
    
    if show:
        plt.show()
        
    plt.close()
    
    

def plot_bf(
    df: pd.DataFrame,
    ax: plt.Axes,
    xlims: tuple[float, float] | None = None,
):
    # make sure dataframe is valid 
    tc = df['tumour_content'].unique().tolist()
    assert len(tc) == 1
    
    
    # plot bayes factor 
    c = get_colours(df['bayes_factor'])
    ax.scatter(
        x=df['coverage'], 
        y=df['bayes_factor'], 
        c=c,
    )
    
    # set xscale to be log 
    ax.set_xscale('log')
    if xlims is not None:
        ax.set_xlim(xlims)
    
    # add ylabel 
    ax.set_ylabel("Bayes Factor (ln)") 
    ax.set_title(f"Tumour Content: {tc[0]}")
    ax.set_xlabel("Coverage")
    
    # add legend 
    handles, labels = add_legend()
    ax.legend(handles=handles, labels=labels, loc='best')
    
    
def add_legend() -> tuple[list, list]:
    handles = []
    labels = []
    
    handles.append(
        plt.Line2D(
            xdata=[0],
            ydata=[0],
            marker='o',
            color='w',
            label='Detected',
            markerfacecolor=colour_blind_friendly['green'], 
            # markersize=8
        )
    )
    labels.append('Detected')
    
    handles.append(
        plt.Line2D(
            [0], [0], marker='o', color='w', label='Inconclusive',
            markerfacecolor=colour_blind_friendly['blue']
        )
    )
    labels.append('Inconclusive')
    
    handles.append(
        plt.Line2D(
            [0], [0], marker='o', color='w', label='Not Detected',
            markerfacecolor=colour_blind_friendly['red'],
        )
    )
    labels.append('Not Detected')
    
    return handles, labels
    
    
def get_colours(bayes_factors: np.ndarray) -> list[str]:
    c = []
    for bf in bayes_factors:
        if bf > 3.:
            # detected tumour fragment 
            c.append(colour_blind_friendly['green'])
        elif -3 < bf and bf < 3:
            # Inconclusive
            c.append(colour_blind_friendly['blue'])
        else:
            # Not detected
            c.append(colour_blind_friendly['red'])
    return c


def main(args):

    df = pd.read_csv(args.summary_tsv_file, sep="\t")
    
    plot(
        df_plot=df, 
        xlims=(5e-2, 15e1),
        output_path=args.out_file,
    )
    


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    # default0 = "/home/matteo/projects/cfdna/wfs/results/pulls/07/cfclone-fwd-sample-cal-smk/TFRI004/out_dir/summary_hdis.tsv"
    
    default0 = "/home/matteo/projects/cfdna/wfs/results/cfclone-inf-pool-power-calc-smk/TFRI004/out_dir/outputs/summary.tsv"

    default1 = "test.png"

    parser.add_argument("-i", "--summary-tsv-file", default=default0)

    parser.add_argument("-o", "--out-file", default=default1)

    cli_args = parser.parse_args()

    main(cli_args)
