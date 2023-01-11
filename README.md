## Evaluator Package

---

Designed to allow for more streamlined evaluation of chatbot components using a variety of metrics.

---

### Directories

`template/`

Contains template classes, outlining expected behaviour of evaluator components. New evaluator packages need to adhere to the expected behaviour outlined here to maintain cross-package compatibility.

`example/`

Contains an example implementation of the template classes to evaluate sample conversations and chatbots.

`utils/`

Contains package-agnostic utility functions and variables. i.e. saving and loading conversation.

`plugins/`

Contains plugins/add-ons for the evaluator package. Insutrctions are included for metrics.

---

### Quick Start

The main entry point for the program is the `run_eval.py` file, which loads the global configurations stored in `./config.json` and attempts to run the evaluation script in `./{target_dir}/__init__.py`

For example, running the default script

```
python3 run_eval.py
```

Will run `./example/__init__.py`

### New Components

New packages should implement at the very least, an evaluator object (`templates.evaluator` &rarr; `BaseEvaluator`) and a `{package}/__init__.py` file that allows for the main program entry to target said package. New metrics can be added in `{package}/metrics/` implementing the `templates/metrics/template_metrics.py` &rarr; `BaseEvalMetric` class.

For document-wise evaluation, the aforementioned metrics, `__init__.py` and evaluator can be sufficient.

For chatbot evaluation (WIP), additional chatbot wrapper needs to be implemented (see `example/chatbot.py`)

---
