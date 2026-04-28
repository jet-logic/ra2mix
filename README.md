# ra2mix

[![PyPI - Version](https://img.shields.io/pypi/v/ra2mix.svg)](https://pypi.org/project/ra2mix)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ra2mix.svg)](https://pypi.org/project/ra2mix)
[![PyPI - License](https://img.shields.io/pypi/l/ra2mix.svg)](https://pypi.org/project/ra2mix)

A python library for working with Red Alert 2 / Yuri's Revenge \*.mix files

Mix files are archive files used to store most game files from the games
**Command And Conquer Red Alert 2** and its expansion pack **Yuri's Revenge**.

This library allows you to interact with the mix files much like you'd interact with
zip files using a program like 7-zip -- except programmatically, of course 😎. You can
create mix files by archiving a list of several files, or read existing mix files
and do something with the archived files contained within it.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Reading a `*.mix` file](#reading-a-mix-file)
  - [Creating a `*.mix` file](#creating-a-mix-file)

## Installation

```bash
pip install ra2mix
```

## Usage

Import the package

```python
import ra2mix
```

### Reading a `*.mix` file

- **Read**:

  The `ra2mix.read` function can take a `*.mix` filepath and return a
  `dict[str, bytes]` object. The keys are filenames and the values are file data as
  bytes.

  ```python
  import ra2mix
  mix_filepath = "path/to/mixfile.mix"

  filemap = ra2mix.read(mix_filepath)
  print(f"filenames: {list(filemap.keys())}")

  for filename, file_data in filemap.items():
      # do something with the file data
  ```

- **Extract**:

  The `ra2mix.extract` function takes a `*.mix` filepath and an extraction folder
  path. The files contained in the mix file will be written to the folder.

  ```python
  import ra2mix
  mix_filepath = "path/to/mixfile.mix"
  extract_folder = "extract/to/folder"

  ra2mix.extract(mix_filepath, extract_folder)
  ```

---

### Creating a `*.mix` file

The `ra2mix.write` function supports three methods for specifying files to include in a
new `*.mix` file:

- `filemap`: A `dict[str, bytes]` object consisting of filenames and file data
- `folder_path`: A path to a folder; all files in the folder are added to the mix
- `filepaths`: A `list[str]` containing exact filepaths to include in the mix

```python
import ra2mix
mix_filepath = "path/to/mixfile.mix"

target_folder = "read/from/folder"

mix_data = ra2mix.write(mix_filepath, folder_path=target_folder)

# Optionally do something with mix_data if you want; file is already written to
# `mix_filepath`
```

---

### 🖥️ Command-Line Interface (CLI)

`ra2mix` includes a built-in CLI for quick archive operations without writing Python code. Once installed, you can invoke it as a standalone command or via the Python module:

```bash
ra2mix <command> [options]
# or
python -m ra2mix <command> [options]
```

### 📖 Available Commands

```bash
$ python -m ra2mix -h
usage: ra2mix [-h] {list,l,extract,x,create,c} ...

List, extract, create MIX files

positional arguments:
  {list,l,extract,x,create,c}
    list (l)            list files of RA2 MIX file
    extract (x)         extract files of RA2 MIX file
    create (c)          create RA2 MIX file from files
```

| Command   | Description                                  |
| --------- | -------------------------------------------- |
| `list`    | View contents of a `.mix` archive            |
| `extract` | Extract all files from a `.mix` archive      |
| `create`  | Pack files/folders into a new `.mix` archive |

### 🔍 List Contents

```bash
$ python -m ra2mix l -h
usage: ra2mix list [-h] [--sort-by-offset {ascending,descending,a,d}] mix_files [mix_files ...]

positional arguments:
  mix_files             path to the .mix files

options:
  -h, --help            show this help message and exit
  --sort-by-offset {ascending,descending,a,d}
                        Sort entries by offset
```

```bash
# Basic file listing
ra2mix list game.mix
```

### 📦 Extract Archive

```bash
$ python -m ra2mix l -h
usage: ra2mix list [-h] [--sort-by-offset {ascending,descending,a,d}] mix_files [mix_files ...]

positional arguments:
  mix_files             path to the .mix files

options:
  -h, --help            show this help message and exit
  --sort-by-offset {ascending,descending,a,d}
                        Sort entries by offset
```

```bash
# Extract to a specific folder
ra2mix extract game.mix -d output/
```

### 🛠️ Create Archive

```bash
$ python -m ra2mix c -h
usage: ra2mix create [-h] [--no-names-db] mix_file files [files ...]

positional arguments:
  mix_file       the mix file to create
  files          files to include

options:
  -h, --help     show this help message and exit
  --no-names-db  Dont add 'local mix database.dat'
```

```bash
# Pack all files from a directory
ra2mix create new.mix assets/

# Pack specific files
ra2mix create new.mix rules.ini art.ini audio01.wav
```
