## GROMACS Utilities
A collection of small scripts for use with GROMACS files

# Usage
```sh
usage: fel.py --trajectory_file TRAJECTORY_FILE --structure_file STRUCTURE_FILE [--eigenvalues EIGENVALUES] [--eigenvectors EIGENVECTORS] [--xpixmap XPIXMAP] [--sort_by_column SORT_BY_COLUMN] [-h]

options:
  --trajectory_file TRAJECTORY_FILE
                        (Path, required) Input: GROMACS trajectory file of the simulated system
  --structure_file STRUCTURE_FILE
                        (Path, required) Input: GROMACS structure file of the simulated system
  --eigenvalues EIGENVALUES
                        (Path, default=eigenvalues.xvg)
  --eigenvectors EIGENVECTORS
                        (Path, default=eigenvectors.trr)
  --xpixmap XPIXMAP     (Path, default=covapic.xpm) Output: X PixMap compatible matrix file
  --sort_by_column SORT_BY_COLUMN
                        (int, default=9999) Sorts the output by a given column
  -h, --help            show this help message and exit
  ```

# Running
Run

E.g.
```sh
python fel.py --trajectory_file md.xtc --structure_file md.gro
```
