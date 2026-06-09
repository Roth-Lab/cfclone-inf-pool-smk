from snakemake.utils import min_version, validate

min_version("9.12")

conda: "envs/global.yaml"

validate(config, "schemas/config.schema.yaml")

from utils import ConfigManager

config = ConfigManager(config)

pathvars:
    out_dir=str(config.cfclone_out_dir),
    pipeline_dir=str(config.cfclone_pipeline_dir),


onsuccess:
    config.notification(
        on="success",
        workflow="cfclone-inf-pool-power-calc-smk",
        configfile=workflow.configfiles[0],
    )


onerror:
    config.notification(
        on="error", 
        workflow="cfclone-inf-pool-power-calc-smk",
        configfile=workflow.configfiles[0],
    )


rule all:
    input:
        config.pipeline_files,


rule build_config_file:
    input:
        workflow.configfiles[0]
    output:
        config.copied_config
    shell:
        "cp {input} {output}"


rule build_cfclone_clone_cn_files:
    input:
        c=config.clone_filter_file,
        i=config.hapclone_results_file,
    output:
        config.cfclone_clone_cn_template,
    # params:
    #     config.get_num_bins_arg
    conda:
        "envs/python.yaml"
    log:
        config.get_log_file(config.cfclone_clone_cn_template),
    shell:
        "(python scripts/build_clone_cn_file.py "
        "-c {input.c} "
        "-i {input.i} "
        # "-n {params} "
        "-o {output} ) >{log} 2>&1"


rule build_cfclone_ctdna_file:
    input:
        c=config.cfclone_clone_cn_template,
        d=config.hapclone_data_file,
        r=config.hapclone_results_file,
        s=config.snp_file,
    output:
        config.cfclone_ctdna_template,
    params:
        r=config.read_length,
        p=config.clone_prevalences,
        c=config.get_coverage,
        t=config.get_tumour_content,
    conda:
        "envs/python.yaml"
    log:
        config.get_log_file(config.cfclone_ctdna_template),
    benchmark:
        config.get_benchmark_file(config.cfclone_ctdna_template),
    shell:
        "(python scripts/build_data.py "
        "--out-file {output} "
        "--hapclone-data-file {input.d} "
        "--hapclone-results-file {input.r} "
        "--snp-file {input.s} "
        "--coverage {params.c} "
        "--read-length {params.r} "
        "--seed {wildcards.data_seed_id} "
        "--tumour-content {params.t} "
        "--clone-prevalence-prior 1 "
        "--clone-prevalence-file {params.p}) >{log} 2>&1"


rule build_cfclone_input_clone_cn_file:
    input:
        config.cfclone_clone_cn_template
    output:
        config.cfclone_clone_cn_template_input
    conda:
        "envs/python.yaml"
    log:
        config.get_log_file(config.cfclone_clone_cn_template_input),
    params:
        config.clone_prevalences
    shell:
        "(python scripts/build_clone_cn_input_file.py "
        "-i {input} "
        "-o {output} "
        "--clone-prevalences-file {params}) >{log} 2>&1"


module cfclone:
    snakefile:
        # "../cfclone-smk/Snakefile"
        "../dups/cfclone-smk/Snakefile"
    config:
        config.cfclone_config


use rule * from cfclone as cfclone_*


use rule run_cfclone from cfclone as cfclone_run_cfclone with:
    input:
        c=config.cfclone_clone_cn_template_input,
        i=config.cfclone_ctdna_template,
    params:
        o=config.get_cfclone_use_outlier_arg,


# rule build_replicate_summary:
#     input:
#         e=config.replicate_evidence_template,
#         t=config.replicate_tumour_content_template,
#     output:
#         config.replicate_summary_template
#     params:
#         c=config.get_coverage_arg,
#         t=config.get_tumour_content_arg,
#     conda:
#         "envs/python.yaml"
#     log:
#         config.get_log_file(config.replicate_summary_template)
#     shell:
#         "(python scripts/write_summary_file.py "
#         "-e {input.e} "
#         "-t {input.t} "
#         "-o {output} "
#         "--coverage {params.c} "
#         "--tumour-content {params.t} "
#         "--replicate {wildcards.data_seed} ) >{log} 2>&1"


# rule merge_summaries:
#     input:
#         config.get_summaries
#     output:
#         config.summary_file,
#     conda:
#         "envs/python.yaml"
#     log:
#         config.get_log_file(config.summary_file),
#     shell:
#         "(python scripts/merge_tables.py -i {input} -o {output}) >{log} 2>&1"
