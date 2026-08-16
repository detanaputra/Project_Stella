import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.views.panels.hyperparams.base_section import BaseHyperparamSection

class BERTopicSection(BaseHyperparamSection):
    """UI section for BERTopic-specific hyperparameters."""

    def __init__(self, parent, state, controller):
        super().__init__(parent, state, controller)

        self.container = ttk.LabelFrame(self, text="BERTopic", padding=10)
        self.container.pack(fill=X, expand=YES)

        # --- Language ---
        lang_frame = ttk.Frame(self.container)
        lang_frame.pack(fill=X, pady=5)
        ttk.Label(lang_frame, text="Language:", width=20).pack(side=LEFT)
        self.lang_var = ttk.StringVar(value=state.algorithm_params.get('bertopic_language', 'english'))
        self._bind_param(self.lang_var, 'bertopic_language')
        self.lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.lang_var,
            values=["english", "multilingual"],
            state="readonly"
        )
        self.lang_combo.pack(side=LEFT, fill=X, expand=YES)
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_lang_change)

        # --- Model ---
        model_frame = ttk.Frame(self.container)
        model_frame.pack(fill=X, pady=5)
        ttk.Label(model_frame, text="Model:", width=20).pack(side=LEFT)

        self.model_options = {
            "english": ["all-MiniLM-L6-v2", "all-mpnet-base-v2"],
            "multilingual": ["paraphrase-multilingual-MiniLM-L12-v2"]
        }

        self.model_var = ttk.StringVar(value=state.algorithm_params.get('bertopic_embedding_model', 'all-MiniLM-L6-v2'))
        self._bind_param(self.model_var, 'bertopic_embedding_model')
        self.model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            state="readonly"
        )
        self.model_combo.pack(side=LEFT, fill=X, expand=YES)
        self._update_model_options()

        # --- Top N Words ---
        top_n_frame = ttk.Frame(self.container)
        top_n_frame.pack(fill=X, pady=5)
        ttk.Label(top_n_frame, text="Top N Words:", width=20).pack(side=LEFT)
        self.top_n_var = ttk.IntVar(value=state.algorithm_params.get('bertopic_top_n_words', 10))
        self._bind_param(self.top_n_var, 'bertopic_top_n_words')
        self.top_n_spin = ttk.Spinbox(top_n_frame, from_=5, to=50, textvariable=self.top_n_var, width=10)
        self.top_n_spin.pack(side=LEFT)

        # --- N-gram Range ---
        ngram_frame = ttk.Frame(self.container)
        ngram_frame.pack(fill=X, pady=5)
        ttk.Label(ngram_frame, text="N-gram Range:", width=20).pack(side=LEFT)

        self.ngram_start = ttk.IntVar(value=state.algorithm_params.get('bertopic_ngram_start', 1))
        self._bind_param(self.ngram_start, 'bertopic_ngram_start')
        self.ngram_start_spin = ttk.Spinbox(ngram_frame, from_=1, to=3, textvariable=self.ngram_start, width=2)
        self.ngram_start_spin.pack(side=LEFT)

        ttk.Label(ngram_frame, text=" to ").pack(side=LEFT)

        self.ngram_end = ttk.IntVar(value=state.algorithm_params.get('bertopic_ngram_end', 2))
        self._bind_param(self.ngram_end, 'bertopic_ngram_end')
        self.ngram_end_spin = ttk.Spinbox(ngram_frame, from_=1, to=3, textvariable=self.ngram_end, width=2)
        self.ngram_end_spin.pack(side=LEFT)

        # --- Min Topic Size ---
        min_size_frame = ttk.Frame(self.container)
        min_size_frame.pack(fill=X, pady=5)
        ttk.Label(min_size_frame, text="Min Topic Size:", width=20).pack(side=LEFT)
        self.min_size_var = ttk.IntVar(value=state.algorithm_params.get('bertopic_min_topic_size', 10))
        self._bind_param(self.min_size_var, 'bertopic_min_topic_size')
        self.min_size_spin = ttk.Spinbox(min_size_frame, from_=5, to=100, textvariable=self.min_size_var, width=10)
        self.min_size_spin.pack(side=LEFT)

        # --- NR Topics ---
        nr_topics_frame = ttk.Frame(self.container)
        nr_topics_frame.pack(fill=X, pady=5)
        ttk.Label(nr_topics_frame, text="NR Topics:", width=20).pack(side=LEFT)
        self.nr_topics_var = ttk.StringVar(value=state.algorithm_params.get('bertopic_nr_topics', 'auto'))
        self._bind_param(self.nr_topics_var, 'bertopic_nr_topics')
        self.nr_topics_combo = ttk.Combobox(
            nr_topics_frame,
            textvariable=self.nr_topics_var,
            values=["auto", "None", 5, 10, 15, 20, 25, 30],
            state="readonly"
        )
        self.nr_topics_combo.pack(side=LEFT, fill=X, expand=YES)

        # --- Low Memory ---
        low_mem_frame = ttk.Frame(self.container)
        low_mem_frame.pack(fill=X, pady=5)
        self.low_mem_var = ttk.BooleanVar(value=state.algorithm_params.get('bertopic_low_memory', False))
        self._bind_param(self.low_mem_var, 'bertopic_low_memory')
        self.low_mem_check = ttk.Checkbutton(low_mem_frame, text="Low Memory Mode", variable=self.low_mem_var)
        self.low_mem_check.pack(side=LEFT)

        # --- Calculate Probabilities ---
        calc_prob_frame = ttk.Frame(self.container)
        calc_prob_frame.pack(fill=X, pady=5)
        self.calc_prob_var = ttk.BooleanVar(value=state.algorithm_params.get('bertopic_calculate_probabilities', False))
        self._bind_param(self.calc_prob_var, 'bertopic_calculate_probabilities')
        self.calc_prob_check = ttk.Checkbutton(calc_prob_frame, text="Calculate Probabilities", variable=self.calc_prob_var)
        self.calc_prob_check.pack(side=LEFT)

    def _update_model_options(self):
        lang = self.lang_var.get()
        options = self.model_options.get(lang, self.model_options["english"])
        self.model_combo['values'] = options
        if self.model_var.get() not in options:
            self.model_var.set(options[0])

    def _on_lang_change(self, event=None):
        self._update_model_options()

    def get_params(self) -> dict:
        return {
            "bertopic_language": self.lang_var.get(),
            "bertopic_embedding_model": self.model_var.get(),
            "bertopic_top_n_words": self.top_n_var.get(),
            "bertopic_ngram_range": (self.ngram_start.get(), self.ngram_end.get()),
            "bertopic_min_topic_size": self.min_size_var.get(),
            "bertopic_nr_topics": self.nr_topics_var.get(),
            "bertopic_low_memory": self.low_mem_var.get(),
            "bertopic_calculate_probabilities": self.calc_prob_var.get()
        }
