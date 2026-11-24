# ESConv source, use and redistribution

Checked November 23, 2026, against the official [CoAI repository](https://github.com/thu-coai/Emotional-Support-Conversation), commit `f262d062ad74cb39b17ea476facc81568ddcba24`.

The repository [LICENSE](data/source/LICENSE) is **Creative Commons Attribution-NonCommercial 4.0 International**. It permits noncommercial sharing and adaptations with attribution, preservation of supplied notices, a license link/text, and identification of modifications. Do not imply endorsement or impose restrictions that prevent exercising the license. The official [README](data/source/README.md) additionally describes the data/code as for academic research use only. This coursework stays within that purpose; commercial deployment is outside this project's scope.

Attribution: **Copyright © 2021 CoAI Group, Tsinghua University. All rights reserved.** ESConv accompanies Siyang Liu et al. (2021), [Towards Emotional Support Dialog Systems](https://aclanthology.org/2021.acl-long.269/). Retain this attribution and the included license when sharing the sample. The license includes an as-is/no-warranties disclaimer; privacy/personality rights are outside its grant.

Bundled modifications: select 80 neutral opening-message excerpts from full-data training conversations, retain actual next-response strategy labels, blank response content, and remove later messages and all original conversation metadata. The text allowlist and selection procedure are in [data/make_sample.py](data/make_sample.py); no synthetic text or labels were introduced. This narrow sample is for academic pipeline demonstration. Its label distribution and repeated greetings are not representative of full ESConv.

Full conversations and derived context files remain local under ignored `data/raw/` and `data/processed/`. No ESConv content is sent to a language-model API. No clinical claims or consent for deployment follow from this license.

Immutable URLs and SHA-256 values are saved in [acquisition.json](data/source/acquisition.json). [config.py](config.py) pins the source. `python data/download.py` downloads/verifies the four official files; never silently substitutes another dataset version.
