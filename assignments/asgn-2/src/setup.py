from setuptools import setup

setup(
    name="rcognita",
    version="0.0.0",
    author="AIDynamicAction",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["rcognita"],
    install_requires=[
        "matplotlib == 3.6.3",
        "mpldatacursor-rcognita == 0.7.2",
        "numpy >= 1.20.1",
        "scipy >= 1.5.0",
        "svgpath2mpl == 0.2.1",
        "tabulate >= 0.8.7",
        "systems == 0.1.0",
        "shapely == 1.7.1",
        "tabulate==0.8.7",
        "recursive_monkey_patch==0.4.0",
        "omegaconf>=2.3.0",
        "hydra-core>=1.3.1",
        "hydra-joblib-launcher>=1.2.0",
        "pandas==1.4.0",
        "casadi==3.5.5",
        "dill==0.3.6",
        "plotly==5.13.0",
        "gitpython==3.1.30",
        "filelock==3.0.12",
        "streamlit==1.17.0",
        "tables==3.8.0",
        "mlflow==2.2.2",
    ],
    python_requires=">=3.6",
)
