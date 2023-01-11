## DialogRPT Dialog Evaluation Metric

---

Implementation of an evaluation metric using [DialogRPT](https://github.com/golsun/DialogRPT)

---

### Quick start

1. Drag and drop this directory into your working `metrics` directory.

2. Download/Clone a DialogRPT model into this directory i.e. the upvote-downvote (updown) model from https://huggingface.co/microsoft/DialogRPT-updown

```
git clone https://huggingface.co/microsoft/DialogRPT-updown
```

3. Install requirements

```
pip install -r requirements.txt
```

4. Add the metric into your evaluator. Example in `evaluator.py`:

```
from [Your Directory].metrics.dialogrpt import DialogRPTMetric

...

self.metrics = [
    ...
    DialogRPTMetric(os.path.join(config['local_dir'], 'metrics/dialogrpt/DialogRPT-updown'))
]

```