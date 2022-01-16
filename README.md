# EXIF-Extract-JPG

Extract EXIF data from images. This program is for .JPG and .TIFF format files. The program coule be extended to support .HEUI, .PNG and other formats. Note that most social media
sities strip exif data from uploaded photos

# Usage

1. Copy all the images to the `./images` directory
2. Start the script

- Start the script normally

```
python3 exiftool.py
```

- Start the script without showing the logo in the terminal (an ASCII banner)

```
python3 exiftool.py -nl
or
python3 exiftool.py --nologo
```

- Start the script in verbose mode (Show important stuff hapenning the script)

```
python3 exiftool.py -v
or
python3 exiftool.py --verbose
```

- Start the script in debug mode (Show everything that is happening the script)

```
python3 exiftool.py -d
or
python3 exiftool.py --debug
```

- Start the script in silent mode (Show nothing in the terminal)

```
python3 exiftool.py -s
or
python3 exiftool.py --silent
```

- Start the script and change the name of the output results file (a CSV file). Defaults to `output.csv`

```
python3 exiftool.py -o "customName.csv"
or
python3 exiftool.py --output "customName.csv"
```
