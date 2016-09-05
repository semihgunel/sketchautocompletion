# Auto-Completion Framework on Sketched Symbols
We implemented the auto-completion system for sketched symbols as described in [here](http://iui.ku.edu.tr/sezgin_publications/2012/PR%202012%20Sezgin.pdf).

## Dependencies
* **scipy**,
* **numpy**,
* **matplotlib**,
* [sketchfe](https://github.com/ozymaxx/sketchfe)
* **libsvm**
* **pycuda** if the graphics card supports CUDA parallelization


You can install the first 3 libraries by typing the following in the terminal:
```
sudo apt-get install pip
sudo pip install numpy scipy matplotlib
```
The necessary steps to install the feature extractor can be found in the README file of [this repository](https://github.com/ozymaxx/sketchfe).

We use libSVM as the Support Vector Machine implementation, the necessary information about the installation can be found in [here](https://www.csie.ntu.edu.tw/~cjlin/libsvm/).

## Directory structure
* `clusterer/`: Source code of the constrained K-means clusterer
* `classifiers/`: Source code of SVM classification for every cluster
* `parallelMethod/`: In order to reduce the running time of training, we also parallelized the training pipeline and tested it. This folder contains the source code of that pipeline.
* `SVM/`: Source code of the interface, allowing us to train SVMs on clusters in a parallelized fashion
* `data/`: Source code of the script that extracts the feature of sketches to be trained and saves these features as CSV files.
* `predict/`: Source code of the prediction pipeline
* `server/`: Sketch classification server, which is used in the demonstration application.
* `test/`: Necessary scripts to test the classification performance on both [NicIcon](http://www.ralphniels.nl/pubs/niels-nicicon.pdf) and [Eitz]() data sets

## How to run/use
### Training
The predictor of the system needs a model which is trained on a sketch data set. To train a model, you should follow these steps:

* Open the terminal
* If there are only full sketches in the data set, extend the data set so that the possible drawable partial sub stroke combinations of the full sketches also exist. The sketches must be in XML format and must be separated into 2 main folders, `test/` for accuracy testing and `train/` for model training. Then, just set `symbolspat` variable as the path to the directory having these two folders, and type `cd data` and `python generatepartial.py`. However, if you have all the partial combinations, don't execute the Python file and proceed to the next step.
* Now we have the partials of the all full sketches and it's time for feature extraction. Again, just set `symbolspat` variable as the directory where the sketches will be trained (divided into `test/` and `train/` folders). Then run the feature extraction by typing `python savecsv.py`.
* Cluster the sketch instances by their features and construct an SVM model for each cluster. There are many alternative constrained clusterers:
  * `ckmeans.py`: The naive constrained K-means implementation, which can be found in [here](http://nichol.as/papers/Wagstaff/Constrained%20k-means%20clustering%20with%20background.pdf).
  * `cudackmeans.py`: CUDA-accelerated version of `ckmeans.py`.
  * `complexCKmeans.py`: Constrained K-means with voting. The details of this algorithm can be found in this technical report (to be put on the [lab's web page](https://iui.ku.edu.tr) soon).
  * `complexcudackmeans.py`: CUDA-accelerated version of `complexCKmeans.py`.
  The tests show that the running time of the constrained K-means algorithm is less than the naive one. Therefore our suggestion is to use the complex algorithm. Moreover, if the graphics driver of your machine supports CUDA parallelization, `complexcudackmeans.py` will be far better for you. Our trainer function named `train()` checks whether your machine has CUDA, and then calls the clusterer function accordingly. Although we included the naive implementation, we preferred to call the complex method as the default clusterer method.
  
  In order to call `train()`, just execute the following lines to check the availability of CUDA first:
  ```
  # check if pycuda is installed
  global cudaSupport
  import imp
  try:
      imp.find_module('pycuda')
      cudaSupport = True
  except ImportError:
      cudaSupport = False
  ```
  
  Then, call `train()` function in the following way. This function also saves the trained model.
  ```
  training_name = [name of the model]
  training_path = [path to the model which will be created]
  numclass = [number of classes]
  numfull = [number of full instances in train/ folder]
  numpartial = [number of partial instances in train/ folder]
  k = [number of clusters that will be created]
  kmeansoutput, classid, svm = train(training_name, training_path, numclass, numfull, numpartial, k)
  ```

### Prediction

## Contact
Ozan Can Altıok - Koç University - oaltiok15 at ku dot edu dot tr<br>
Ahmet Bağlan - Boğaziçi University - ahmet.baglan at boun dot edu dot tr<br>
Arda İçmez - Galatasaray University - aicmez at gmail dot com<br>
Semih Günel - Bilkent University - gunelsemih at gmail dot com<br>

* CKMeans algorithm takes feature array as 720xN (720 rows, N columns).
