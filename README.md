# bpmn-to-natural-language
Generating natural (Polish) language descriptions for simple BPMN models.

## How to use this program?
This is a Python library so you have to write a couple lines of Python code in order to use it.

To run this program you have to import `Translator` class from `./translator.py` file and run one of two available methods: `translate()` or `translate_to_text()`.
The first one returns a python list of lists of sentences. The second one returns an enumerated description as a text.

Example:

```python
from translator import Translator

translator = Translator('./bpmn_models/some_interesting_process.bpmn')

# 1) translate() method
description_lists = translator.translate()

for idx, desc in enumerate(description):
    print(f'Group {idx + 1}.\n')

    for sen_idx, sentence in enumerate(desc):
        print(f'Sentence {sen_idx + 1}: {sentence}\n')

    desc_list.append('\n')



# 2) translate_to_text() method
description_text = translator.translate_to_text()

print('Description:')
print(description_text)
```
