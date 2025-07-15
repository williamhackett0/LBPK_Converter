# Little Big Planet Karting Archive Converter

This tool takes the archived community levels from archive.org (https://archive.org/details/LBPKServer) and converts them into offline saved tracks which can be played via your moon. 
- **No private server is required** - making this the first time you can play LBPK communtiy levels without a dedicated server.

## Usage

Download and extract the community levels from archive.org into a folder of your choice. Typically the folders have a unique ID as the folder name and inside have a `data.bin`
- i.e. `10183/data.bin` or `1835473/data.bin`

![Server Files Example](https://github.com/williamhackett0/LBPK_Converter/blob/main/assets/server_files_example.PNG)

Download the latest release [here](https://github.com/williamhackett0/LBPK_Converter/releases) or run the application with `python lbpk.py`.

This will open a GUI interface where you can select the folder containing all the server files extracked from the previous step (`10183/data.bin` etc). You can then select the output folder to place the converted track files. Clicking 'Convert' will then start the process.

Transfer any saves from your output foler (You will see there are 6 files) to your Ps3 via FTP or another method.
- Little Big Planet Kartings save locations can be found at `/dev_hdd0/game/NPEA00421_UCC/USRDIR/1/DATA/LOCAL/TRACK`. This may look different for you.
- Simply place the generated files into the TRACK folder (Your folder should have the below output). 

![Example FTP folder](https://github.com/williamhackett0/LBPK_Converter/blob/main/assets/ftp_example.PNG)

## Building

We use `pyinstaller` to create a build. Use `pyinstaller --noconsole --add-data "resources/*;." .\lbpk.py`

## Deep Dive

`data.bin` is a container file type which appears to contain similar data to local save files in LBPK. They appear in this order:
- .trk (Track data)
- .cm2 (Track Metadata)
- .nav (Havok Engine)
- .hud (Hud)

The files contained within data.bin are exactly the same file types found when saving a level locally on your moon. Therefore extracting these files we can simply add them to our own moon and play them as if they were our own creation.

The file begins with a `CTH header` which appears to always be 20 bytes.
- It also holds the size of the .NAV for the track which is helpful for extracting later.

`.TRK` holds the track data for the level. Its header contains the full size of the track.

`.CM2` is the most interesting as it holds all the metadata for the track. There's alot to unpack likely loads of little bits about the track such as race type etc. However currently we can easily extract:
- Track Name
- Track Description
- Unique ID (Used for the filename likely to verify integrity)

The `NAV` file appears to be related to HAVOK and more than likely used for computing the navigation mesh for AI drivers. It has many strings such as `hkRootLevelContainer` which are commonly found in HAVOK objects.

`.HUD` hold all the HUD information for the track. I haven't dived very much into this.