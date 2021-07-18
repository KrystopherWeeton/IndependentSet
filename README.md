### COMMANDS

`./exp.py` is used for running experiments. The structure is
```./exp.py {project} {experiment} {arguments}```

`./plot.py` is used for plotting experiment results. The structure is
```./plot.py {project} {plot_command} {arguments}```

NOTE: The arguments and commands depend on the project in question

### Quick Reference / Testing Commands

```
{
    ./exp.py ind-set heuristic -n 500 --num-trials 1 --file-name test --verbose
}
```

Runs the heuristic experiment in independent set on a small instance, storing the results in *test.pkl*

```python -i load_results.py --path "./independent_set/experiment_results/test.pkl"```

Loads the result from the previous command into the python shell, allowing manual examination