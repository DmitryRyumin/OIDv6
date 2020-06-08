# Download single or multiple classes from the Open Images V6 dataset

![PyPI](https://img.shields.io/pypi/v/oidv6)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oidv6)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/oidv6)
![PyPI - Status](https://img.shields.io/pypi/status/oidv6)
![PyPI - License](https://img.shields.io/pypi/l/oidv6)

| [Release history](https://github.com/DmitryRyumin/OIDv6/blob/master/NOTES.md) | [Documentation in Russian](https://github.com/DmitryRyumin/OIDv6/blob/master/README_RU.md) |
| --- | --- |

## Installation

```shell script
pip install oidv6
```

## Update

```shell script
pip install --upgrade oidv6
```

## Required packages

| Packages | Min version | Current version |
| -------- | ----------- | --------------- |
`requests` | `2.23.0` | ![PyPI](https://img.shields.io/pypi/v/requests) |
`numpy` | `1.18.4` | ![PyPI](https://img.shields.io/pypi/v/numpy) |
`pandas` | `1.0.4` | ![PyPI](https://img.shields.io/pypi/v/pandas) |
`progressbar2` | `3.51.3` | ![PyPI](https://img.shields.io/pypi/v/progressbar2) |
`opencv-contrib-python` | `4.2.0.34` | ![PyPI](https://img.shields.io/pypi/v/opencv-contrib-python) |
`awscli` | `1.18.69` | ![PyPI](https://img.shields.io/pypi/v/awscli) |

## Useful resources

- [Official site Open Images Dataset V6](https://storage.googleapis.com/openimages/web/index.html)
- [List of all classes that can be downloaded](https://github.com/DmitryRyumin/OIDv6/blob/master/oidv6/classes.txt)

## [Class for multiple download of the Open Images Dataset V6 dataset (OIDv6)](https://github.com/DmitryRyumin/OIDv6/blob/master/oidv6/OIDv6.py)

### Command line arguments

| Argument&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Type | Description | Valid Values |
| -------------------------- | ---  | -------- | ------------------- |
| command | str | Boot command | `downloader` |
| command | str | Language<br>`Default value: en` | `en`<br>`ru` |
| --dataset | str | The root directory for saving OIDv6<br>`Default value: OIDv6` | - |
| --type_data | str | Dataset<br>`Default value: train` | `train`<br>`validation`<br>`test`<br>`all` |
| --classes | str | Sequence of class names or text file | - |
| --limit | int | Images Upload Limit<br>`Default value: 0 (no limit)` | From `0` to `∞` |
| --multi_classes | bool | Downloading classes in one directory | No value |
| --yes | bool | Automatic download metadata | No value |
| --no_labels | bool | No labeling | No value |
| --hide_metadata | bool | Вывод метаданных | No value |
| --no_clear_shell | bool | Do not clean the console before running | No value |

<h4 align="center"><span style="color:#EC256F;">Examples</span></h4>

---

>  **Note!**Classes that are composed of several words should be surrounded by quotation marks (if they are passed directly to the command line). For example: `"Organ (Musical Instrument)"`

---

1. Downloading classes (`apple`, `banana`, `Kitchen & dining room table`) from the `train`, `validation` and `test` sets with labels in semi-automatic mode and image = `4` (Language: `Russian`)

    > CMD
    >
    > ```shell script
    > oidv6 downloader ru --dataset path_to_directory --type_data all --classes apple banana "Kitchen & dining room table" --limit 4
    > ```

2. Downloading training classes (`cat`, `dog`) from the `train` set with tags in automatic mode and image limit = `10` (Language: `English`)

    > CMD
    >
    > ```shell script
    > oidv6 downloader en --dataset path_to_directory --type_data train --classes Cat dOg --limit 10 --yes
    > ```

3. Downloading validation classes (see text file) from the `validation` set with labels in automatic mode and image limit = `10` (Language: `English`)

    > Text file
    >
    > ```text
    > person
    > Organ (Musical Instrument)
    > ```

    > CMD
    >
    > ```shell script
    > oidv6 downloader --dataset path_to_directory --type_data validation --classes text_file_path --limit 10 --yes
    > ```

4. Downloading classes (`axe`, `calculator`) in one directory from the `train`, `validation` and `test` sets with labels in automatic mode and image limit = `12` (Language: `English`)

    > CMD
    >
    > ```shell script
    > oidv6 downloader --dataset path_to_directory --type_data all --classes axe calculator --limit 12 --multi_classes --yes
    > ```