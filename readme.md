# Read Me
## Description
A Python Library to Parse Neper Tess Files + Input Files. 
Furthermore the parsed Files can be used to create customized FEAP Input Skripts,
including initial conditions using a custom nucleation model.
## Dependecies
* numpy
* matplotlib
* mpl_toolkits.mplot3d (for generationg 3D plots) should be included in matplotlib
## Installation
Create a conda environment (python 3.*) including the dependencies listed below. Then cd in this directory and do
```bash
pip install .
```  
Maybe you want to clean the repo before installing it as module (examples.ipynb, example folder).  
A much more useful way to import the module to make ongoing changes is by importing it from a folder without installing it to an anaconda environment. 
The following code is used to set the path variable pointing to a clone of this repo.
```python
%load_ext autoreload
%autoreload 2
import sys
sys.path.append('C:\\Users\\sft7rng\\Desktop\\NeperTools')
``` 
Note that the first to lines are only necessary if you want to reload the module automatically after every change. Afterwards the module can be imported as usual:
```python
import nepertools.inp
import nepertools.tess
import nepertools.materials
import nepertools.nmodel
import nepertools.writer
``` 
## Example
Examples for 2(2D), 3,12(3D) martensite variants are given in the examples folder. This includes the .tess, .inp as well as the Output (FEAP input script). The codes necessary together with some visualizations is given in the example.ipynb Jupyter notebook.

## Sample Skript
For a given .tess + .inp file as well as a config File. The following skript will create the according FEAP input skript:  
```python
#imports 
import nepertools.inp
import nepertools.tess
import nepertools.materials
import nepertools.nmodel
import nepertools.writer
#defining path for each files, here in example folder 
tessfile_path = 'examples/2m/micro_2d.tess'
inpfile_path = 'examples/2m/micro_2d.inp'
configfile_path = 'examples/2m/config.json'
outputfile_path = 'examples/2m/Ioutput'
#parse tess file
tparser = nepertools.tess.TESS_Parser(tessfile_path) 
tf = tparser.parse()
#parse mesh
parser = nepertools.inp.InpFileParser(inpfile_path,4)
mesh = parser.parse()
#create materials
MC = nepertools.materials.Material_Creator(configfile_path)
MC.create_material_list(tf.orientation_list)
#create initial conditions (nucleus model)
NM = nepertools.nmodel.NucleusModel2D(configfile_path,mesh,tf)
NM.create_model()
#create outputfile
Fwriter = nepertools.writer.FEAPWriter(outputfile_path,configfile_path,mesh,MC.material_list)
Fwriter.write_materials()
Fwriter.write_mesh()
Iwriter = nepertools.writer.NucleusWriter(outputfile_path,configfile_path,NM)
Iwriter.write_np()
```
The output script is ready for a FEAP Simulation. The solve script may need to be varied.
## Config Files
For each generation, a config file is used which defines the parameters of the later FEAP input script as well as the parameters to generate the initial conditions (nucleation model). For a detailed overview of the possible parameters see one of the example config files in the example folder. The config file is divided in 4 sections:
#### 1. general
* user_element_number - defines the user element which is later used in FEAP. Note that not every user element is defined in FEAP itself, but any input will be copied to the FEAP input script without checking.
* scale - is used to scale the microstructure. The Neper structures should be of scale 1-1(-1) to make calculation easy. This factor scales the microstructure to the desired dimensions
* nodes_per_elementt - 4 in 2D, 8 in 3DHere are general parameters for each step defined. Notable are:
#### 2. constants
Should be self-explanatory. Defines the constants which are copied 1:1 to FEAP Input script.
#### 3. materials
Constans for the materials. Note that list for elasticitys as well as eigenstrains need to contain at least the relevant number of entries for the wanted variants. More entries are not considered so feel free to add as many as you want.
#### 4. nmodel
Defines the parameter for the nucleation model to create the initial conditions.
* radius - defines the nuclei radius. Note that this value is between 0 and 0.5 and is relative to the edge length of the given domain(1). 0.01 would be a radius of 0.01 of the edge length.
* quantity - defines the nuclei quantity. Note that there may be some differences depending on the total grains as well as the chosen probabilities
* grain_prob - between 0 and 1, probability of a nuclei spawning in a grain
* bound_prob - between 0 and 1, probability of a nuclei spawning on a boundary
* triple_prob - between 0 and 1, probabilty of a nuclei spawnign on a triple (node in 2D vertex in 3D)  

note that grain_prob, bound_prob and triple_prob should sum up to 1
## To Do
* Visualization only works for structures which have coordinates between 0 and 1 -> should be adaptive