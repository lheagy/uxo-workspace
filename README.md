**[contents](#Contents) | [usage](#Usage) | [running the notebooks](#running-the-notebooks) | [issues](#issues) | [citation](#citation) | [license](#license)**

# Workspace: Machine learning for classifying unexploded ordnance (UXO) from electromagnetic data

This is a workspace for exploring the use of CNNs for classifying UXO from EM data  (see [(Heagy et al., 2020)](./https://github.com/simpeg-research/heagy-et-al-2020-uxo-seg/blob/master/heagy-et-al-seg-2020.pdf))

## Contents

There are 5 notebooks in this repository: 

1. [forward_modelling_example.ipynb](./forward_modelling_example.ipynb): This notebook contains a simple example of running a forward simulation using BTInvert
2. [plot_survey.ipynb](./plot_survey.ipynb): This notebook loads up data from the test plot and plots it
3. [plotting_test_data_and_noise.ipynb](./plotting_test_data_and_noise.ipynb): In this notebook, I look at the test plot data to get a sense of the background signal. This generates the file `noise_test_plot.npz`
4. [train-synthetic-data.ipynb](./train-synthetic-data.ipynb): This notebook uses PyTorch to set up a convolutional neural network to classify UXO from EM data. The training relies purely on synthetic data. It includes a classification of the test plot data
5. [train-with-noise-from-field-data.ipynb](./train-with-noise-from-field-data.ipynb): This notebook uses PyTorch to set up a convolutional neural network to classify UXO from EM data. The training samples field data that we know is background from `noise_test_plot.npz`. It includes a classification of the test plot data

## Usage

To run the first notebook, you need BTInvert from [Black Tusk Geophysics](http://www.btgeophysics.com/). All notebooks are set up with the path to BTInvert set as: `"../../UXO_protected/+BTInvertPY"`

To run the notebooks locally, you will need to have python installed,
preferably through [anaconda](https://www.anaconda.com/download/) .

You can then clone this repository. From a command line, run

```
git clone https://github.com/lheagy/uxo-workspace.git
```

Then `cd` into the `uxo-workspace` directory:

```
cd uxo-workspace
```

To setup your software environment, we recommend you use the provided conda environment

```
conda env create -f environment.yml
conda activate uxo-workspace
```

Alternatively, you can use `pypi` to install the requirements. 

```
pip install -r requirements.txt
```

You can then launch Jupyter

```
jupyter notebook
```

Jupyter will then launch in your web-browser.

## Running the notebooks

Each cell of code can be run with `shift + enter` or you can run the entire notebook by selecting `cell`, `Run All` in the toolbar.

<img src="https://em.geosci.xyz/_images/run_all_cells.png" width=80% align="middle">

For more information on running Jupyter notebooks, see the [Jupyter Documentation](https://jupyter.readthedocs.io/en/latest/)

## Issues

Please [make an issue](https://github.com/lheagy/uxo-workspace/issues) if you encounter any problems while trying to run the notebooks.

## Citation

If you build upon or use these examples in your work, please cite:

Heagy, L. J., Oldenburg, D. W., Pérez, F. & Beran, L. (2020, submitted). Machine learning for classifying unexploded ordnance from electromagnetic data. In SEG Technical Program Expanded Abstracts 2020. Society of Exploration Geophysicists.

```
@inproceedings{Heagy2020,
author = {Heagy, Lindsey J. and Oldenburg, Douglas W and Pérez, Fernando and Beran, Laurens},
booktitle = {SEG Technical Program Expanded Abstracts 2020 (submitted)},
doi = {10.1190/segam2015-5931035.1},
publisher = {Society of Exploration Geophysicists},
title = {{Machine learning for classifying unexploded ordnance from electromagnetic data}},
year = {2020}
}
```

## License
These notebooks are licensed under the [MIT License](/LICENSE) which allows academic and commercial re-use and adaptation of this work.

