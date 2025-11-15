from setuptools import setup, find_packages

setup(
    name="gitminer-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'typer[all]',
        'pydriller',
        'GitPython',
        'lizard',
        'bandit',
        'pandas',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'gitminer = gitminer.cli:app',
        ],
    },
    author="Seu Nome",
    author_email="seu.email@example.com",
    description="Uma ferramenta CLI para mineração de repositórios Git.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu_usuario/gitminer-cli", # Substitua pelo seu repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)