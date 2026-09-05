# BERTopic Hyperparameter List and Instruction
## Instruction
1. implement the views/wizard/panel_hyperparams.py according to the configuration section below. Each Subsection (BERTopic, UMAP, and HDBSCAN) must be implemented in each Labelframe container and give label according to the name of its subsection. 
2. implement each subsection in different file for easier maintainability and put it inside the same folder. 
3. Pass the hyperparameter setting value to each object in bertopic.py, specifically in train() function. 
4. implement these hyperparameter configuration inputs in the main-window settings panel — `views/panels/algorithm_settings_panel.py`. Reuse the same subsection files from step 2 there and in the wizard's `views/wizard/panel_hyperparams.py`.


## Configuration:
### BERTopic
language
name: language
implementation: Combobox
options: ["english", "multilingual"]
default: "english"
behavior: if user select multilingual, only "paraphrase-multilingual-MiniLM-L12-v2" option is available in model selection below. if user select english, the model options are restored to initial option. 

model
name: model
implementation: Combobox
options : [
            "all-MiniLM-L6-v2",
            "all-mpnet-base-v2",
            "paraphrase-multilingual-MiniLM-L12-v2"
        ]
default: "all-MiniLM-L6-v2"

top_n_words
name: top_n_words
implementation: Spinbox
min: 5
max: 50
default: 10

n_gram_range
name: n_gram_range
implementation: Frame with two Spinbox (start, end)
min: 1
max: 3
default: (1, 2)

min_topic_size
name: min_topic_size
implementation: Spinbox
min: 5
max: 100
default: 10

nr_topics
name: nr_topics
implementation: Combobox
options: ["auto", "None", 5, 10, 15, 20, 25, 30]
default: "auto"

low_memory
name: low_memory
implementation: Checkbutton
default: False

calculate_probabilities
name: calculate_probabilities
implementation: Checkbutton
default: True

### UMAP
n_neighbors
name: n_neighbors
implementation: Spinbox
min: 2
max: 100
default: 15

n_components
name: n_components
implementation: Spinbox
min: 2
max: 50
default: 5

metric
name: metric
implementation: Combobox
options: ["cosine", "euclidean", "manhattan", "chebyshev", "minkowski"]
default: "cosine"

low_memory
name: low_memory
implementation: Checkbutton
default: False

### HDBSCAN
min_samples
name: min_samples
implementation: Spinbox
min: 1
max: 100
default: 10

min_cluster_size
name: min_cluster_size
implementation: Spinbox
min: 1
max: 100
default: 10

metric
name: metric
implementation: Combobox
options: ["euclidean", "manhattan", "chebyshev", "minkowski"]
default: "euclidean"