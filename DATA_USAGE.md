# ESConv source, use and redistribution

This project uses ESConv from the official [CoAI repository](https://github.com/thu-coai/Emotional-Support-Conversation), commit `f262d062ad74cb39b17ea476facc81568ddcba24`. The source and terms were checked on November 23, 2026.

The repository's [license](data/source/LICENSE) is **Creative Commons Attribution-NonCommercial 4.0 International**. It allows noncommercial sharing and adaptation, provided the source is credited, supplied notices are retained, the license is included or linked, and changes are identified. It does not allow implying endorsement or adding restrictions that prevent others from using the license. The official [README](data/source/README.md) also states that the data and code are for academic research use only. I am using the dataset for this coursework, with no commercial deployment planned.

Attribution: **Copyright © 2021 CoAI Group, Tsinghua University. All rights reserved.** ESConv accompanies Siyang Liu et al. (2021), [Towards Emotional Support Dialog Systems](https://aclanthology.org/2021.acl-long.269/). Retain this attribution and the included license when sharing the sample. The license includes an as-is/no-warranties disclaimer; privacy/personality rights are outside its grant.

The included sample keeps 80 neutral opening messages from full-data training conversations and the original strategy label of each next response. Response text is blanked, and later messages and original conversation metadata are removed. [data/make_sample.py](data/make_sample.py) contains the greeting list and selection procedure. No text or labels were invented. I use this small sample to show that the code runs offline; its repeated greetings and label distribution do not represent the full dataset.

Full conversations and processed context files stay in local `data/raw/` and `data/processed/` folders, which are excluded from Git. The current implementation does not send ESConv text to a language-model API. The dataset license does not establish that a chatbot is clinically effective or approved for deployment.

The exact source URLs and SHA-256 hashes are saved in [acquisition.json](data/source/acquisition.json). [config.py](config.py) fixes the dataset version. Running `python data/download.py` downloads or verifies the four official files and reports an error if a hash does not match.
