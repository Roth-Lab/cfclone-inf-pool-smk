### Runs cfClone using data generate via infinite pool


### Pulling results
```
rsync -r --include='*/' --include='*.tsv' --include='*.h5' --include='*.tsv.gz' --exclude='*' numbers:/path/to/out_dir . --progress
```