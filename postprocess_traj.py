import subprocess
from pathlib import Path
from tap import Tap


class MyArgumentParser(Tap):
    trajectory_file: Path  # Input: GROMACS trajectory file of the simulated system
    structure_file: Path  # Input: GROMACS structure file of the simulated system


def center_traj(
    tpr: Path = Path("md.tpr"), traj: Path = Path("md.xtc")
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        f"gmx trjconv -s {tpr} -f {traj} -o md_noPBC.xtc -center -pbc mol -ur rect",
        shell=True,
    )


def fit_traj(
    tpr: Path = Path("md.tpr"),
    traj: Path = Path("md_noPBC.xtc"),
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        f"gmx trjconv -s {tpr} -f {traj} -o md_fit.xtc -fit rot+trans", shell=True
    )


def postprocess(
    tpr: Path = Path("md.tpr"),
    unprocessed_traj: Path = Path("md.xtc"),
    centered_traj: Path = Path("md_noPBC.xtc"),
) -> None:
    center_traj(tpr, unprocessed_traj)
    fit_traj(tpr, centered_traj)


if __name__ == "__main__":

    args = MyArgumentParser().parse_args()
    postprocess(args.structure_file, args.trajectory_file)
