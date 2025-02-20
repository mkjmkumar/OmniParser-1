# OmniParser: Screen Parsing tool for Pure Vision Based GUI Agent

<p align="center">
  <img src="imgs/logo.png" alt="Logo">
</p>

[![arXiv](https://img.shields.io/badge/Paper-green)](https://arxiv.org/abs/2408.00203)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

📢 [[Project Page](https://microsoft.github.io/OmniParser/)] [[Blog Post](https://www.microsoft.com/en-us/research/articles/omniparser-for-pure-vision-based-gui-agent/)] [[Models](https://huggingface.co/microsoft/OmniParser)] [[Huggingface demo](https://huggingface.co/spaces/microsoft/OmniParser)]

**OmniParser** is a comprehensive method for parsing user interface screenshots into structured and easy-to-understand elements, which significantly enhances the ability of GPT-4V to generate actions that can be accurately grounded in the corresponding regions of the interface. 

## News
- [2024/10] OmniParser is the #1 trending model on huggingface model hub (starting 10/29/2024). 
- [2024/10] Feel free to checkout our demo on [huggingface space](https://huggingface.co/spaces/microsoft/OmniParser)! (stay tuned for OmniParser + Claude Computer Use)
- [2024/10] Both Interactive Region Detection Model and Icon functional description model are released! [Hugginface models](https://huggingface.co/microsoft/OmniParser)
- [2024/09] OmniParser achieves the best performance on [Windows Agent Arena](https://microsoft.github.io/WindowsAgentArena/)! 

## Install 
Install environment:
```python
echo 'export PYTHONPATH="/workspace:$PYTHONPATH"' >> ~/.bashrc
source ~/.bashrc
echo $PYTHONPATH
/workspace:

pip install -r requirements.txt

apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libopencv-dev \
    python3-opencv
```

pip install --upgrade torch ultralytics

# Change directory to some other place to clone microsoft/OmniParser checkpoint
brew install git-lfs
git lfs install
git clone https://huggingface.co/microsoft/OmniParser

Then download the model ckpts files in: https://huggingface.co/microsoft/OmniParser, and put them under weights/, default folder structure is: weights/icon_detect, weights/icon_caption_florence, weights/icon_caption_blip2. 

brew install git-lfs
git lfs install
git clone https://huggingface.co/microsoft/OmniParser


Finally, convert the safetensor to .pt file. 
```python
python weights/convert_safetensor_to_pt.py
```

## Examples:
We put together a few simple examples in the demo.ipynb. 

## Gradio Demo
To run gradio demo, simply run:
```python
python gradio_demo.py
```
## Gradio Demo using gradio_demo_1.py
To run gradio demo, with Optimized Code for Quick Execution. Here’s a stripped-down version of your gradio_demo.py that removes unnecessary UI components and focuses only on the image upload and parsed screen elements output::
```python
python gradio_demo_1.py

## Gradio Demo using gradio_demo_2.py
To run gradio demo, with Optimized Code for Quick Execution. UI varaibles are added:
```python
python gradio_demo_2.py

## Gradio Demo using gradio_demo_2.py
To run gradio demo, with Optimized Code for Quick Execution. 
gradio_demo.py to read all parameters from a .env file, which will act as a centralized configuration. The default values will be moved to this file along with comments explaining each parameter.

```python
python gradio_demo_3.py


## Hosting as API, use below installation and run the api.py
pip install flask gunicorn torch Pillow python-dotenv
pip install flasgger


## Option-1 : Run below command to host the api
python python app.py

## Option-2 : Run below command to host the api
gunicorn -w 4 -b 0.0.0.0:58090 app:app --log-level info --capture-output --worker-class gthread --threads 4 --preload

## Option-3 : Run Gunicorn with the following command to capture logs in /workspace/gunicorn.log
gunicorn -w 1 -b 0.0.0.0:58090 app:app --log-level info --access-logfile gunicorn.log --error-logfile gunicorn.log --capture-output --timeout 120


## Option-4 CPU-Faster OCR: Run Gunicorn with the following command to capture logs in /workspace/gunicorn.log
gunicorn -w 1 -b 0.0.0.0:58090 app_cpu:app --log-level info --access-logfile gunicorn.log --error-logfile gunicorn.log --capture-output --timeout 120

## Option-5 GPU-Quality OCR: Run Gunicorn with the following command to capture logs in /workspace/gunicorn.log
gunicorn -w 1 -b 0.0.0.0:58090 app_gpu:app --log-level info --access-logfile gunicorn.log --error-logfile gunicorn.log --capture-output --timeout 120


## Call the OmniParser API
curl -X POST http://localhost:58090/process_image  -F "file=@/workspace/imgs/temp_image.png"


## You can access the Swagger documentation by navigating to:
http://localhost:58090/apidocs/

## Remember to run the gradio_demo_4_api.py first before calling the api

## Model Weights License
For the model checkpoints on huggingface model hub, please note that icon_detect model is under AGPL license since it is a license inherited from the original yolo model. And icon_caption_blip2 & icon_caption_florence is under MIT license. Please refer to the LICENSE file in the folder of each model: https://huggingface.co/microsoft/OmniParser.

## 📚 Citation
Our technical report can be found [here](https://arxiv.org/abs/2408.00203).
If you find our work useful, please consider citing our work:
Yes- Sure
```
@misc{lu2024omniparserpurevisionbased,
      title={OmniParser for Pure Vision Based GUI Agent}, 
      author={Yadong Lu and Jianwei Yang and Yelong Shen and Ahmed Awadallah},
      year={2024},
      eprint={2408.00203},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2408.00203}, 
}
```
apt install tree
tree -L 4 -I 'node_modules|git|ls_volume|ui|public'