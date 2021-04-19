# Qualia structure generator

[![pipeline status](https://gitlab.com/till_johanndeiter/qualiagenerator/badges/master/pipeline.svg)](https://gitlab.com/till_johanndeiter/qualiagenerator/-/commits/master)

This python commandline application provides the automatic acquisition of qualia structures for english nouns. A qualia structure detected the meaning and ambiguity of a word. The meaning is divided into the four categories *formal* (Domain), *constiutive* (Components), *agentive* (Creation) and *telic* (Application). For example, this is a possible qualia structure of the word *dog*:


```
Qualia theorem: dog
    formal: [animal, pet],
    constitutive: [tail, leg, tyke, nose],
    agentive: [breed, copulate, adopt],
    telic: [hunt, guard, play]
```
The categories are called *qualia roles* and the elements *qualia elements*.

# Installation

Supported python version: 3.8

We recommend using a virtual environment especially to avoid dependency problems. 

Create virutal environment:

```
python -m pip install --user virtualenv

python -m venv env

source env/bin/activate (For Windows: env\Scripts\activate)
```

Install requirements:

```
pip install -r requirements.txt
```


# Arguments

The qualia theorems can be directly passed by argument. 

```
python qualia_generator.py dog cat human
```

```
-w, --writeToFile  If flag is used, output will be written to file
-i INPUT_FILE, --inputFile INPUT_FILE File with line separated qualia theorems
-o OUTPUT, --output OUTPUT Output directory of created structures
-d, --debug Print or write additional debug structure with more information like metric value and origin of extracted element
-t TOPK, --topK TOPK  Maximal length of qualia roles
--inflectionDict INFLECTIONDICT Filepath of lookup table of words which are not inflectable by pyinflect
```

For example:

```
python qualia_generator.py -i=qualiaTheorems -o=results --topK=50 --debug -w
```

Will create for every word in the file qualiaTheorems the qualia structure with a maximal length of 50 elements per role and write the structure to a .qs file in the folder results. A .qs file will print the  The file inflectionDict will be used as a lookup table for words, which are not inflectable by pyinflect.

For the automatic acquisition multiple strategies are available. 


```
-c {g,google,b,bert,mb,modifiedBert}, --creation {g,google,b,bert,mb,modifiedBert} Creation strategy
```

# Google

This strategy uses the pattern extraction of serach results. Requests will be executed and qualia elements will be extracted by using the dependency tree of [Spacy](https://spacy.io/usage/linguistic-features). For this a Custom Search Engine and An API Key is required. [Here](https://linuxhint.com/google_search_api_python/) you find instructions for both. The qualia elements will be ranked by a metric. The keys and metric can be passed by argument.

```
-m {webP,webJack,webPMI,occurrenceInPattern,numOfSources}, --metric {webP,webJack,webPMI,occurrenceInPattern,numOfSources}
-k KEYS, --keys KEYS  File with api keys
```
For example:

```
python qualia_generator.py dog -c=g --key=apiKeys --top_k=50 --metric=numOfSources
```

Will use the google strategy and rank the qualia elements by the number of search results in which the element occured. The required API Keys are taken from the files apiKeys. Each key has a limit of 100 daily requests. The folder .searchRequests will be created to save serach requests.


# BERT

This strategy uses the wordprection from the pretrained model [BERT](https://huggingface.co/transformers/model_doc/bert.html).

For example:

```
python qualia_generator.py dog -c=b
```

Will use the BERT strategy for creation.

# Modified BERT

This strategy is also based on the word prediction but use the dependency tree to validate the predictions.

```
python qualia_generator.py dog -c=mb
```

# Tests

We recommend [pytest](https://pytest.org/) to run the unit tests. 

Installation:

```
pip install pytest
```

Run tests:

```
pytest -v
```


The test classes in the folder ignoreInCI only work if the limit of the api keys is not reached. So we excluded them from the CI pipeline.


# Documentation

We recommend [pdoc](https://pdoc3.github.io/pdoc/) the generate the documentation files.

Installation:

```
pip install pdoc3
```

Generate documentation:

```
pdoc --html src
```

# Evaluation Notebook

We recommend [jupyter](https://jupyter.org/) to run the evaluation script.

```
pip install notebook
```

Run notebook:

```
jupyter notebook
```

## License

[The Unlicense](https://choosealicense.com/licenses/unlicense/)


# Contact

If you have questions, issues or feedback: 

tjohanndeiter@techfak.de
