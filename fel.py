import subprocess
from pathlib import Path
from xpm2txt import xpm2txt
from tap import Tap


class MyArgumentParser(Tap):
    trajectory_file: Path  # Input: GROMACS trajectory file of the simulated system
    structure_file: Path  # Input: GROMACS structure file of the simulated system
    eigenvalues: Path = Path(
        "eigenvalues.xvg"
    )  # Output: GROMACS .xvg file for calculated eigenvalues
    eigenvectors: Path = Path(
        "eigenvectors.trr"
    )  # Output: GROMACS .trr file for calculated eigenvectors
    xpixmap: Path = Path("covapic.xpm")  # Output: X PixMap compatible matrix file
    sort_by_column: int = 9999  # Sorts the output by a given column


def check_extension(file: Path, extension: list[str]) -> bool:
    return Path(file).suffix in extension


def calc_covar_eigenvec_eigenval(
    traj: Path, struct: Path, eigenval: Path, eigenvec: Path, xpixmap: Path
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        (
            f"gmx covar -s {Path(struct)} -f {Path(traj)} -o {Path(eigenval)} -v {Path(eigenvec)}"
            f" -xpma {Path(xpixmap)}"
        ),
        shell=True,
    )


def calc_pc1_pc2(
    traj: Path, struct: Path, eigenvec: Path
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        (
            f"gmx anaeig -f {Path(traj)} -s {Path(struct)} -v {Path(eigenvec)} -last 1 -proj pc1.xvg"
            " && "
            f"gmx anaeig -f {Path(traj)} -s {Path(struct)} -v {Path(eigenvec)} -first 2 -last 2 -proj pc2.xvg"
        ),
        shell=True,
    )


def concat_pc1_pc2() -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        "paste pc1.xvg pc2.xvg  | awk '{print $1, $2, $4}' > PC1PC2.xvg", shell=True
    )


def calc_gibbs_fe() -> subprocess.CompletedProcess[bytes]:
    return subprocess.run("gmx sham -f PC1PC2.xvg -ls FES.xpm", shell=True)


def convert_xpm_to_dat(column_sort: int = 9999) -> None:
    return xpm2txt(Path("FES.xpm"), Path("FEL.dat"), column_sort)


def fel(
    traj: Path,
    struct: Path,
    eigenval: Path,
    eigenvec: Path,
    xpixmap: Path,
    column_sort: int = 9999,
) -> None:
    calc_covar_eigenvec_eigenval(traj, struct, eigenval, eigenvec, xpixmap)
    calc_pc1_pc2(traj, struct, eigenvec)
    concat_pc1_pc2()
    calc_gibbs_fe()
    convert_xpm_to_dat(column_sort)


if __name__ == "__main__":

    args = MyArgumentParser().parse_args()

    check_traj: bool = check_extension(
        args.trajectory_file, [".xtc", ".trr", ".cpt", ".gro", ".g96", ".pdb", ".tng"]
    )
    check_struct: bool = check_extension(
        args.structure_file, [".tpr", ".gro", ".g96", ".pdb", ".brk", ".ent"]
    )

    if check_traj and check_struct:
        fel(
            Path(args.trajectory_file),
            Path(args.structure_file),
            Path(args.eigenvalues),
            Path(args.eigenvectors),
            Path(args.xpixmap),
            args.sort_by_column,
        )
    else:
        print("One or more invalid input files. Please check.")
