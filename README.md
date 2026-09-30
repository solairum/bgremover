# bgremover

Remove the background from any image, **100% locally**. No account, no credits, no watermark, and your images never leave your computer.

A free and open-source alternative for people who just want a quick cutout.

## Features

- **Local processing**: the AI model runs on your own machine. Nothing is uploaded anywhere.
- **Several models to choose from**, all under permissive open-source licenses.
- **Mask cleanup**: removes semi-transparent "ghost" areas the model is unsure about.
- **Single subject mode**: keeps only the largest object (removes stray text, logos, fragments).
- **Two ways to use it**: a simple web interface in your browser, or the command line.

## Installation

You need **[Python](https://www.python.org/downloads/) 3.10 to 3.13, 64-bit**. The newest Python releases are sometimes not yet supported by the AI libraries, so 3.13 is the safest choice.

### 1. Get the code

**Option A: download (no tools needed, recommended)**
Click the green **Code** button at the top of this page, then **Download ZIP**. Unzip it (on Windows: right-click the ZIP, then **Extract All**; opening it with a double-click is not enough).

**Option B: with git**

```bash
git clone https://github.com/solairum/bgremover.git
cd bgremover
```

On macOS, if `git` is not installed, the system offers to install the developer tools: accept and try again. On Windows, install [Git for Windows](https://git-scm.com/download/win) first, then open a **new** terminal, or simply use option A.

### 2. Install and run

#### macOS / Linux

Open a terminal in the project folder (on macOS: right-click the folder in Finder, then **Services → New Terminal at Folder**) and run these commands one by one:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### Windows

1. **Install Python from [python.org](https://www.python.org/downloads/)**, not from the Microsoft Store. On the first screen of the installer, check **"Add python.exe to PATH"** before clicking *Install Now*. At the end, click **"Disable path length limit"** if offered.
2. **Install the [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)**. The AI engine needs it; without it, the app crashes with `DLL load failed`.
3. **Open a terminal in the project folder**: open the folder in File Explorer (the one that directly contains `app.py`), click the address bar, type `cmd` and press Enter. Use this Command Prompt rather than PowerShell.
4. **Run these commands one by one:**

```bat
py -3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

If Windows Defender asks whether Python may access the network, you can click *Cancel*: the app only runs on your own computer.

### Next times

The installation is done once. Every time you open a **new terminal**, activate the environment again, then start the app:

- macOS / Linux: `source .venv/bin/activate` then `python app.py`
- Windows: `.venv\Scripts\activate` then `python app.py`

You know the environment is active when `(.venv)` appears at the start of the line. The first time you use a model, it is downloaded automatically (170 MB to 1 GB depending on the model).

### Troubleshooting

| Problem | Solution |
|---|---|
| `python: command not found` (macOS) | Use `python3` outside the environment. Inside it (`(.venv)` visible), `python` works. |
| `python` opens the Microsoft Store or "is not recognized" (Windows) | Python was installed without PATH. Use `py` instead of `python`, or reinstall Python and check "Add python.exe to PATH". |
| `git` is not recognized (Windows) | Use option A (Download ZIP), or install Git for Windows and open a new terminal. |
| `Could not open requirements file` | The terminal is not in the right folder. After unzipping, the files are often in `bgremover-main\bgremover-main`. Type `dir` (Windows) or `ls` (macOS): you must see `app.py` and `requirements.txt`. |
| `No matching distribution found for onnxruntime`, `Microsoft Visual C++ 14.0 is required` or `metadata-generation-failed` | Your Python version is too recent or 32-bit. Install Python 3.13 64-bit, delete the `.venv` folder and start the installation again. |
| "Running scripts is disabled on this system" (Windows) | You are in PowerShell. Type `cmd`, press Enter, then activate the environment again. |
| `DLL load failed while importing onnxruntime` (Windows) | Install the Microsoft Visual C++ Redistributable (step 2 above). |
| `pip install` seems frozen | It downloads about 200 MB. Wait until you see `Successfully installed`. |
| `CERTIFICATE_VERIFY_FAILED` when downloading a model (macOS) | Go to **Applications → Python 3.x** and double-click **Install Certificates.command**. |

Still stuck? [Open an issue](https://github.com/solairum/bgremover/issues) with your operating system, your Python version (`python --version`) and the full error message.

## Usage

### Web interface

```bash
python app.py
```

Your browser opens on the interface: drop an image, pick a model, click **Remove background**. Stop the app with `Ctrl + C` in the terminal.

### Command line

```bash
python remove_bg.py photo.jpg
python remove_bg.py photo.jpg --model birefnet-general-lite --single-subject
python remove_bg.py --help
```

The result is saved as `photo_nobg.png` next to the original.

## Models

| Model | Quality | Download | License |
|---|---|---|---|
| `isnet-general-use` (default) | Good, fast | ~170 MB | Apache 2.0 |
| `birefnet-general-lite` | Very good edges, needs several GB of RAM | ~220 MB | MIT |
| `birefnet-general` | Best, very demanding | ~1 GB | MIT |
| `u2net` | Older, lighter | ~170 MB | Apache 2.0 |

Models with non-commercial licenses are deliberately left out, so the whole project stays free to use for anyone.

## Roadmap

- [x] Background removal (command line)
- [x] Local web interface
- [ ] In-browser version (no installation needed)
- [ ] Remove burned-in captions from videos

## Built with

- [rembg](https://github.com/danielgatis/rembg) for running the background removal models
- [Gradio](https://www.gradio.app/) for the web interface

## License

[MIT](LICENSE)
