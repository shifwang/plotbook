# Plotbook

Plotbook allows you to make beautiful plots in Jupyter notebook interactively via ipywidgets. It helps people make beautiful plots faster, especially those who routinely use packages such as matplotlib, plotly, and seaborn. Some highlights:
1. Plot type inference: automatically infer the possible types of plot given the input data.
2. Use widgets to do fine-tuning.

## Installation
You can install via pip:

```
pip install plotbook
```

In order for widgets to work, make sure you also need to install the following jupyter extensions:

```
jupyter nbextension install jupyter-js-widgets plotlywidget
```

Check if the extensions are enabled:

```
jupyter nbextension list
```

## Demos
Example images in the jupyter notebook:

![Example1](https://github.com/shifwang/plotbook/blob/master/imgs/example1.png)
![Example2](https://github.com/shifwang/plotbook/blob/master/imgs/example2.png)
![Example3](https://github.com/shifwang/plotbook/blob/master/imgs/example3.png)
