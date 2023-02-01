# **Autogasuptake**
:: A simple Python script for automating the calculation and visualization of gas uptake from a raw data file ::

## **Introduction**
**Autogasuptake** is a convinient tool for automating the calculation and visualization of gas uptake from a raw csv file that contains the cylinder volume and the pressure of the gas in the experimental system. 

## **Requirements**
You will need below packages to run **Autogasuptake**. But don't worry, you can install them all with `pip` or `pip3`. Personally, I'm highly recommend you to use [Anaconda](anaconda.com) as your Python distribution. 
- `pandas`
- `matplotlib`
- `numpy`
- `scipy`
- `scikit-learn`
- `seaborn`
- `pyfiglet`
- `tabulate`

## **How to Install**
It is easy to install **Autogasuptake**. Just use `pip` or `pip3` to install it.
```
$ pip install autogasuptake
```
or 
```
$ pip3 install autogasuptake
```

## **How to Use**
### **(1) Graph plotting**
After installing **Autogasuptake**, you can execute it right in the terminal. 
But before you use it, you need to prepare csv files from your experimental data (mainly came from the LabVIEW program). Note that LabVIEW program exports the data in a csv file with space as the delimiter (but it's ok if you use comma (',') as delimiter. The program recognizes this and proceeds with data processing normally). It looks like this: 
```
570.000000 406.754852
569.799988 406.006744
569.799988 404.104126
569.799988 401.781738
```
The first column is the pressure (psi) of your system, and the second column is the volumn (mL) of the cylinder. Make sure to remember the location where you save these raw csv files. 

Then, deploy Autogasuptake in your terminal.
```
$ autogasuptake
```
The program initiates, and firstly asks you to make the `settings.txt` file if you don't have one. 
```
ERROR There is no `settings.txt` file in the current directory. I will make a new `settings.txt` file for you.
INFO The `settings.txt` file has been created. Please edit the file and run the program again.
```
If you have already have your own `settings.txt` file, you won't see this message.

<br>

The exported `settings.txt` file looks like this: 
```
###################################
############ SETTINGS.TXT #############
###################################
# NOTE: This file should be located in the directory where you are executing the program. This can be done by typing `pwd` in the terminal. Check your current location. 
# NOTE: You can mark `#` in front of the lines you don't want to use. 
# NOTE: This file should be named as `settings.txt`. If isn't, the program cannot load the settings. 

###########################################################
# Target directory where the raw data files are located. 
directory = ./ 

# Data collection frequency (in ms); the value when you set in the LabVIEW program. 
frequency = 300000

# Experimental temperature (in K) 
temperature = 276.3 

# Critical temperature of your interested gas (in K) 
tc = 209.5389

# Critical pressure of your interested gas (in bar) 
pc = 55.034

# Acentric factor of your interested gas 
omega = 0 

# Time unit (h, m, or s) 
tunit = m

# Whether to decorate the graph with research figure style (options: y, n) 
graph-decorate = y

# Plot type (options: line, scatter) 
plot-type = scatter

# Whether to include the title in the graph (options: y, n) 
include-title = n

# Output file type (options: png, pdf, svg) 
output-file-type = png 

# Equation of state model (options: rk, pr) 
eos = pr 

# Water mass you used in the experiment (in g) 
water-mass = 50

# Type of the hydrate (options: sI, sII, sH, and none)
hydrate-type = sII
```
* Basically, you should choose your interested gas and find its critical temperture, critical pressure, and acentric factor. And carefully modify `settings.txt` file according to your found values. Note that the demo `settings.txt` file is written for the calculation of gas uptake of $CO_2$ molecules. 
* After then, you can choose whether to decorate the graph with research figure style, whether to include the title in the graph, and the output file type. Especially, if you choose `y` for the graph decoration, the program will change the font-style, font-size, and line-width of the graph. If you write `n` for the graph decoration, the plot will be exported with the default style. If you want to know more about the <i>decorated</i> style and the <i>default</i> style, refer to the below comparison.
  (n) Default style | (y) Decorated style
  :-------------------------:|:-------------------------:
  <img src="https://github.com/wjgoarxiv/Autogasuptake/blob/56c7439fd725e2c75bba75cbc0e38537a7f80f63/withoutDECO.png"/> | <img src="https://github.com/wjgoarxiv/Autogasuptake/blob/56c7439fd725e2c75bba75cbc0e38537a7f80f63/withDECO.png"/> 
* You can also choose the equation of state model you want to use. Currently, the program supports two EOS models: Redlich-Kwong (RK) and Peng-Robinson (PR). The detailed information about the EOS models is given in the below section.
* The plot type can be either `line` or `scatter`. 
    (line) Line plot | (scatter) Scatter plot
  :-------------------------:|:-------------------------:
  <img src="https://github.com/wjgoarxiv/Autogasuptake/blob/5ea55edec6fd2e075a1f7b91ab327ab2411621e4/line.png"/> | <img src="https://github.com/wjgoarxiv/Autogasuptake/blob/5ea55edec6fd2e075a1f7b91ab327ab2411621e4/scatter.png"/>
  * If you choose `line`, the program will plot the gas uptake data with a line. Consecutively, the program will ask the line width that you want to use.
  * If you choose `scatter`, the program will plot the gas uptake data with a scatter plot. Consecutively, the program will ask the total number of points that you want to include in the plot. The program will divide the total number of points by the number of data points you have, and then plot the data points with the same interval.

### **(2) Making a new output CSV**
After the program outputs the graph, it collects the processed data and creates a new CSV file to provide to the user. After the program runs, check the target directory again. You can check the output file in the form below.
Pressure (psi) | Cylinder volume (mL) |	Pressure (bar) | Cylinder volume (L) | Time (min) | Delta_V (L) | Gas uptake (mol of gas) | Gas uptake (mol of gas / mol of water)
 :-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|
 | ... | ... | ... | ... | ... | ... | ... | ... |


## **Equation of State (EOS) information**
### **Redlich-Kwong (RK) EOS**
Redlich-Kwong EOS is one of the most popular EOSs. To calculate the compressibility factor ( $z$ ), the program uses the following equations:
$$Tr = \frac{T}{T_c}, \quad Pr = \frac{P}{P_c}$$
$$a = 0.42748 \frac{R^2 T_c^{2.5}}{P_c}, \quad b = 0.08664 \frac{RT_c}{P_c}$$
$$A = aP/RT^{2.5}, \quad B = bP/RT$$
$$z, where \space z^3 - z^2 + (A - B - B^2)z - AB = 0$$
Where $T$ is the experimental temperature, $T_c$ is the critical temperature, $P$ is the experimental pressure, $P_c$ is the critical pressure, $R$ is the gas constant, and $\omega$ is the acentric factor. $a$, $b$, $A$, and $B$ are the parameters of the EOS.
The z value is calculated by using the Newton's method. 

### **Peng-Robinson (PR) EOS**
Peng-Robinson EOS is more newer than Redlich-Kwong EOS and also one of the most popular EOSs. To calculate the compressibility factor ( $z$ ), the program uses the following equations:
$$Tr = \frac{T}{T_c}, \quad Pr = \frac{P}{P_c}$$
$$a = 0.45724 \frac{R^2 T_c^{2}}{P_c} \omega, \quad b = 0.07780 \frac{RT_c}{P_c}$$
$$\kappa = 0.37464 + 1.54226\omega - 0.26992\omega^2$$
$$\alpha = (1 + \kappa(1 - \sqrt{T_r}))^2$$
$$A = \frac{\alpha a p}{R^2 T^2}, \quad B = \frac{bp}{RT}$$
$$z, where \space z^3 - (1 - B)z^2 + (A - 2B - 3B^2)z - (AB - B^2 - B^3)= 0$$
Where $T$ is the experimental temperature, $T_c$ is the critical temperature, $P$ is the experimental pressure, $P_c$ is the critical pressure, $R$ is the gas constant, and $\omega$ is the acentric factor. $a$, $b$, $\kappa$, and $\alpha$ are the parameters of the Peng-Robinson EOS.
The z value is also calculated by using the Newton's method.

- [Reference](https://en.m.wikipedia.org/wiki/Cubic_equations_of_state#Peng%E2%80%93Robinson_equation_of_state)

## **Equations used**
### **Gas uptake equation**
The gas uptake (mol of gas / mol of water) is simply calculated by using the following equation: 
$$\frac{n_{gas}}{n_{water}} = \frac{P_{exp}\Delta{V}}{zRT_{exp}}\frac{1}{\frac{m_{water}}{M_{water}}}$$
Where $n_{gas}$ is the number of gas molecules, $n_{water}$ is the number of water molecules, $P_{exp}$ is the experimental pressure, $\Delta{V}$ is the volume change in ISCO syringe pump, $z$ is the compressibility factor, $R$ is the gas constant, $T_{exp}$ is the experimental temperature, $m_{water}$ is the mass of water, and $M_{water}$ is the molar mass of water.

### **Theoretical maximum gas uptake value calculation**
When the user select the `hydrate-type` option as sI, sII, and sH, the program will calculate the theoretical maximum gas uptake value. The program uses the following equation to calculate the theoretical maximum gas uptake value:
$$(sI) \space 2S·6L·46H_2O → \frac{8}{46} = 0.1739$$
$$(sII) \space 8S·16L·136H_2O → \frac{24}{136} = 0.1765$$
$$(sH) \space 3S·2M·1L·34H_2O → \frac{6}{34} = 0.1765$$
Where $S$ stands for the small cage, $M$ stands for the medium cage, and $L$ stands for the large cage. If you don't want to mark the theoretical maximum gas uptake value in your plot, you can simply select the `hydrate-type` option as `none`.
| When `hydrate-type` is on | When `hydrate-type` is `none` |
|:-------------------------:|:-------------------------:|
| <img src="https://github.com/wjgoarxiv/Autogasuptake/blob/fdcba57b15e9f03b0291c86239447776345dbeba/hydrate-type=on.png"/> | <img src="https://github.com/wjgoarxiv/Autogasuptake/blob/fdcba57b15e9f03b0291c86239447776345dbeba/hydrate-type=none.png" /> |

## **License**
- MIT License

## **Author**
- [wjgoarxiv](https://github.com/wjgoarxiv)
