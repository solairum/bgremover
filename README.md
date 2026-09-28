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

You need [Python](https://www.python.org/downloads/) 3.10 or newer.

```bash
git clone https://github.com/solairum/bgremover.git
cd bgremover

# Create an isolated environment for the project
python3 -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

The first time you use a model, it is downloaded automatically (170 MB to 1 GB depending on the model).

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
