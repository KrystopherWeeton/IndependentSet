#!env/bin/python3
import click

from independent_set.experiments.convergence import convergence_speed
from independent_set.experiments.heuristic import heuristic
from independent_set.experiments.rep_suc_aug import repeated_suc_aug
from independent_set.experiments.sa_distribution import sa_distribution
from independent_set.experiments.size import size
from independent_set.experiments.sparse_bt.run import run_sparse_bt
from independent_set.experiments.suc_aug_concentration import \
    suc_aug_concentration
from independent_set.experiments.successive_augmentation import \
    successive_augmentation

#from independent_set.experiments.phase_heuristic import phase_heuristic


@click.group()
def ind_set():
    pass

ind_set.add_command(size)
ind_set.add_command(heuristic)
ind_set.add_command(successive_augmentation)
ind_set.add_command(suc_aug_concentration)
ind_set.add_command(sa_distribution)
ind_set.add_command(repeated_suc_aug)
ind_set.add_command(convergence_speed)
ind_set.add_command(run_sparse_bt)

if __name__ == "__main__":
    ind_set()
