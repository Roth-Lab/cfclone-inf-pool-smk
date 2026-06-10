from pathlib import Path

from itertools import product

from snakemake.shell import shell

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

    # @property
    # def num_bins(self):
    #     return self.config['num_bins']

    @property
    def read_length(self):
        return self.config["read_length"]
    
    # CFCLONE SETTINGS 
    
    @property
    def cfclone_config(self):
        return {
            "ctdna_file": str(self.cfclone_ctdna_template),
            "clone_cn_file": str(self.cfclone_clone_cn_template),
            "clone_tree_newick": str(None), # cfclone-smk needs o.w. schema validation
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
    def merged_summary_file(self):
        return self.cfclone_out_dir.joinpath("summary.tsv")
    
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
    
    # SUMMARY FILES 
    
    @property
    def copied_config(self):
        return self.out_dir.joinpath("config.yaml")
    
    @property
    def summary_file(self):
        return self.out_dir.joinpath("summary.tsv")

    @property
    def pipeline_files(self) -> list[str]:
        
        file_templates = (
            self.experiment_configuration,
            self.merged_tumour_content_file,
            self.merged_evidence_file,
            self.merged_summary_file
        )
        
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
        
        return [self.copied_config] + cfclone_files

    
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
    
    # @property
    # def get_num_bins_arg(self):
    #     num_bins_args = self.num_bins
    #     if num_bins_args == "all":
    #         return num_bins_args
    #     else:
    #         return int(num_bins_args)
        
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
    
    # HELPERS FOR NOTIFICATIONS
    
    @property
    def email(self) -> str:
        return self.config.get("email", "lepurmatteo@gmail.com")
    
    def notification(self, on: str, workflow: str, configfile: str, imgs: list[str] | None = None) -> None:

        configfile = Path(configfile).resolve()

        msg_template = "configfile:{config}"

        msg = msg_template.format(config=configfile)

        subj_template = "-s {wf}:{n}"

        subj = subj_template.format(wf=workflow, n=on)

        if on == "success":
            
            if imgs is not None:

                img_template = "-a {img} "
                
                imgs = self.get_imgs_to_send(imgs)

                att = ""

                for i in imgs:

                    att0 = img_template.format(img=i)

                    att += att0

                cmd_template = "echo {msg} | mail {sub} {att} {email}"

                cmd = cmd_template.format(msg=msg, sub=subj, att=att, email=self.email)
            
            else:
                
                cmd_template = "echo {msg} | mail {sub} {att} {email}"

                cmd = cmd_template.format(msg=msg, sub=subj, att=att, email=self.email)

        else:

            cmd_template = "echo {msg} | mail {sub} {email}"

            cmd = cmd_template.format(msg=msg, sub=subj, email=self.email)

        shell(cmd)
    
    
    @staticmethod
    def get_imgs_to_send(imgs: list[str]) -> list[str]:
        
        LIMIT = 10240000
        
        ALLOWED = LIMIT * 0.66
        
        total_size = 0
        
        allowed_imgs = []
        
        for img in imgs:
            
            file_path = Path(img)
            
            file_size = file_path.stat().st_size
            
            total_size += file_size
            
            if total_size < ALLOWED:
                
                allowed_imgs.append(file_path)
                
            else:
                
                total_size -= file_size
                
        return allowed_imgs
            
