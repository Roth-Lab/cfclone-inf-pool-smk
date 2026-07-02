from pathlib import Path

from itertools import product

class ConfigManager(object):
    def __init__(self, config):
        self.config = config

    # WILDCARDS

    @property
    def coverage(self):
        return self.config["coverage"]
    
    @property
    def coverage_ids(self):
        return list(range(len(self.coverage)))

    @property
    def tumour_content(self):
        return self.config["tumour_content"]
    
    @property
    def tumour_content_ids(self):
        return list(range(len(self.tumour_content)))
    
    @property
    def num_data_replicates(self):
        return self.config["num_data_replicates"]
     
    @property
    def num_model_replicates(self):
        return self.config["num_model_replicates"]
  
    # DATA GENERATION SETTINGS 
    
    @property
    def clone_prevalences(self):
        return self.config['clone_prevalences']

    @property
    def read_length(self):
        return self.config["read_length"]
    
    # CFCLONE SETTINGS 
    
    @property
    def cfclone_config(self):
        return {
            "ctdna_file": str(self.cfclone_ctdna_template),
            "clone_cn_file": str(self.cfclone_clone_cn_template),
            "clone_tree_newick": str(self.clone_tree_nwk_file),
            "num_chains": self.num_chains,
            "num_rounds": self.num_rounds,
            "num_threads": self.num_threads,
            "num_restarts": self.num_model_replicates,
            "out_dir": "<out_dir>",
            "pipeline_dir": "<pipeline_dir>",
        }
        
    @property
    def num_chains(self):
        return self.config["num_chains"]

    @property
    def num_rounds(self):
        return self.config["num_rounds"]

    @property
    def num_threads(self):
        return self.config["num_threads"]
    
    @property
    def cfclone_use_outlier(self):
        return self.config['cfclone_use_outlier']
    
    @property
    def clone_tree_nwk_file(self):
        # return self.config['clone_tree_nwk_file']
        return self.config.get('clone_tree_nwk_file')

    # INPUT FILES FOR DATA GEN
    
    @property
    def clone_filter_file(self):
        return Path(self.config["clone_filter_file"]).resolve()

    @property
    def hapclone_data_file(self):
        return Path(self.config["hapclone_data_file"]).resolve()

    @property
    def hapclone_results_file(self):
        return Path(self.config["hapclone_results_file"]).resolve()

    @property
    def snp_file(self):
        return Path(self.config["snp_file"]).resolve()

    # OUTPUT DIRECTORIES FILES 
    
    @property
    def out_dir(self):
        return Path(self.config["out_dir"]).resolve()

    @property
    def pipeline_dir(self):
        return Path(self.config["pipeline_dir"]).resolve()

    @property
    def log_dir(self):
        return self.pipeline_dir.joinpath("log")
    
    @property
    def benchmark_dir(self):
        return self.pipeline_dir.joinpath("benchmark")

    @property
    def tmp_dir(self):
        return self.pipeline_dir.joinpath("tmp")
    
    # CFCLONE IO
   
    @property
    def cfclone_ctdna_dir(self):
        return self.out_dir.joinpath(
            "cfclone",
            "input",
            "ctdna",
            "coverage_{coverage_id}",
            "tc_{tumour_content_id}",
            "data_seed_{data_seed_id}",
        )
    
    @property
    def cfclone_ctdna_template(self):
        return self.cfclone_ctdna_dir.joinpath("ctdna.tsv.gz")
        
    @property
    def ctdna_plot_template(self):
        return self.out_dir.joinpath("ctdna_plot.png")
    
    @property
    def cfclone_clone_cn_dir(self):
        return self.out_dir.joinpath("cfclone", "input", "clone_cn")
    
    @property
    def cfclone_clone_cn_template(self):
        return self.cfclone_clone_cn_dir.joinpath("clone_cn.tsv.gz")

    @property
    def cfclone_clone_cn_template_input(self):
        return self.cfclone_clone_cn_dir.joinpath("clone_cn_input.tsv.gz")
   
    # OUTPUTTED BY CFCLONE-SMK
    
    @property
    def cfclone_dir(self):
        return self.out_dir.joinpath(
            "cfclone",
            "coverage_{coverage_id}",
            "tc_{tumour_content_id}",
            "data_seed_{data_seed_id}",
        )

    @property
    def cfclone_out_dir(self):
        return self.cfclone_dir.joinpath("out_dir")

    @property
    def cfclone_pipeline_dir(self):
        return self.cfclone_dir.joinpath("pipeline_dir")

    @property
    def experiment_configuration(self):
        return self.cfclone_out_dir.joinpath("config.yaml")

    @property
    def merged_tumour_content_file(self):
        return self.cfclone_out_dir.joinpath("tumour_content.tsv")
    
    @property
    def merged_evidence_file(self):
        return self.cfclone_out_dir.joinpath("evidence.tsv")
    
    @property
    def merged_prevalence_file(self):
        return self.cfclone_out_dir.joinpath("prevalence.tsv")

    @property
    def merged_summary_file(self):
        return self.cfclone_out_dir.joinpath("summary.tsv")
    
    @property
    def cfclone_restart_dir(self):
        return self.cfclone_out_dir.joinpath("restart_{seed}")
    
    @property
    def pairwise_ranks_file(self):
        return self.cfclone_restart_dir.joinpath("tables", "pairwise_ranks.tsv")
    
    # CFCLONE SUMMARY FILES 
    
    @property
    def cfclone_summary_file(self):
        return self.tmp_dir.joinpath(
            "cfclone",
            "coverage_{coverage_id}",
            "tc_{tumour_content_id}",
            "data_seed_{data_seed_id}",
            "cfclone_summary_file.tsv"
        )
        
    @property
    def cfclone_prevs_summary_file(self):
        return self.tmp_dir.joinpath(
            "cfclone",
            "coverage_{coverage_id}",
            "tc_{tumour_content_id}",
            "data_seed_{data_seed_id}",
            "cfclone_prevs_summary_file.tsv"
        )
    
    # SUMMARY FILES 
    
    @property
    def copied_config(self):
        return self.out_dir.joinpath("config.yaml")
    
    @property
    def summary_file(self):
        return self.out_dir.joinpath("summary.tsv")
    
    @property
    def prevs_summary_file(self):
        return self.out_dir.joinpath("prevs_summary.tsv")

    @property
    def pipeline_files(self) -> list[str]:
        
        file_templates = [
            self.experiment_configuration,
            self.merged_tumour_content_file,
            self.merged_evidence_file,
            self.merged_summary_file
        ]
        
        if self.clone_tree_nwk_file is not None:
            
            file_templates.append(self.merged_prevalence_file)
        
        cfclone_files = [
            str(file).format(
                coverage_id=cov,
                tumour_content_id=tc,
                data_seed_id=ds
            )
            for cov, tc, ds in product(
                self.coverage_ids,
                self.tumour_content_ids, 
                range(self.num_data_replicates)
                )
            for file in file_templates
        ]
        
        summary_files = [self.summary_file]
        
        if self.clone_tree_nwk_file is not None:
            
            summary_files.append(self.prevs_summary_file)
            
            
        rank_files = [
            str(self.pairwise_ranks_file).format(
                coverage_id=cov,
                tumour_content_id=tc,
                data_seed_id=ds,
                seed=ms
            )
            for cov, tc, ds, ms in product(
                self.coverage_ids,
                self.tumour_content_ids, 
                range(self.num_data_replicates),
                range(self.num_model_replicates)
                )
        ]
        
        return [self.copied_config] + cfclone_files + summary_files + rank_files

    
    def gather_files(self, file_template: str) -> list[str]:
        return [
            str(file_template).format(
                coverage_id=cov,
                tumour_content_id=tc,
                data_seed_id=ds,
            ) 
            for cov, tc, ds in product(
                self.coverage_ids, 
                self.tumour_content_ids, 
                range(self.num_data_replicates)
            )
        ]

    
    # HELPER FUNCTIONS FOR RULES 

    def get_coverage(self, wildcards):
        return float(self.coverage[int(wildcards.coverage_id)])

    def get_tumour_content(self, wildcards):
        return float(self.tumour_content[int(wildcards.tumour_content_id)])
    
    @property
    def get_cfclone_use_outlier_arg(self):
        if self.cfclone_use_outlier:
            return "--outlier"
        else:
            return "--no-outlier"
    
    def get_cfclone_use_outlier_arg_str(self, wildcards):
        str = self.get_cfclone_use_outlier_arg(wildcards)
        return str[2:]
    

    def get_log_file(self, template):
        parent, rel_path = self._get_relative_path(template)
        rel_path = rel_path.with_suffix(".log")
        return self.log_dir.joinpath(parent, rel_path)
    
    def get_benchmark_file(self, template):
        parent, rel_path = self._get_relative_path(template)
        rel_path = rel_path.with_suffix(".log")
        return self.benchmark_dir.joinpath(parent, rel_path)

    def _get_relative_path(self, template):
        try:
            rel_path = template.relative_to(self.pipeline_dir)
            parent = "working"
        except ValueError:
            rel_path = template.relative_to(self.out_dir)
            parent = "output"
        return parent, rel_path
    