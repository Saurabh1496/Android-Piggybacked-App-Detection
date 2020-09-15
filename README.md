# Piggybacked App-Detection
Piggybacked Apps are apps that contain malicious code which is grafted on benign app before repackaging.\
This command-line application helps in classifying an android app as piggybacked or not.

## Dependencies
  * [Apktool](https://ibotpeaches.github.io/Apktool/)
  * [Networkx](https://networkx.github.io/)
  * [Numpy](http://www.numpy.org/)
  * [Scikit-learn](http://scikit-learn.org/stable/index.html)
  

## Running
The program can be started by running **main.py** and passing the file name(if in current directory) or relative path of the android app as command-line argument.
  ```
 python main.py sample.apk
 ```

## Working
  * It first Disassemble the app using Apktool.
  * Then parses all the smali files and make a directed call-graph of functions in the app, where an edge orginates from callee method and points to called method.
  * Then based on a sensitive-api list, the call-graph is divided into mutually exclusive(sensitive-api) sub-graphs, each consisting of sensitive-api('s) and neighbouring nodes within depth of not more than level-3.
  * The Subgraph with the highest sensitive score(pre-calculated from the Dataset) is selected and some features are extracted from it [[1]](#1).
  * Permission-based features are also added to for better distinction.
  * At last, the Random Forest is used as a classification model.

## References
<a id="1">[1]</a> 
M. Fan, J. Liu, W. Wang, H. Li, Z. Tian and T. Liu, "DAPASA: Detecting Android Piggybacked Apps Through Sensitive Subgraph Analysis," in IEEE Transactions on Information Forensics and Security, vol. 12, no. 8, pp. 1772-1785, Aug. 2017, doi: 10.1109/TIFS.2017.2687880.