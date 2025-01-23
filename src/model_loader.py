from llama_cpp import Llama


# TODO: Add config loading
class ModelLoader:
    _instance = None
    _model = None
    # DEFAULT_CONFIG_PATH = os.path.join(
    #     os.path.dirname(__file__), "model_loader_config.yaml"
    # )

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize LLM configuration with default values."""
        self.repo_id: str = "bartowski/Mistral-Nemo-Instruct-2407-GGUF"
        self.model_name: str = "Mistral-Nemo-Instruct-2407-Q4_K_S.gguf"
        self.n_gpu_layers: int = 20
        self.n_ctx: int = 4000

    def load_model(self):
        """Load the Llama model with configured parameters."""
        if self._model is None:
            try:
                self._model = Llama.from_pretrained(
                    repo_id=self.repo_id,
                    filename=self.model_name,
                    n_gpu_layers=self.n_gpu_layers,
                    n_ctx=self.n_ctx,
                )
            except Exception as e:
                raise RuntimeError(f"Failed to load LLM model: {str(e)}")
        return self._model

    # def _read_config(self, config_path: str) -> None:
    #     """Read the configuration from the specified file."""
    #     with open(config_path, "r") as f:
    #         config = yaml.load(f)
    #         self.repo_id = config.get("repo_id", self.repo_id)
    #         self.model_name = config.get("model_name", self.model_name)
    #         self.n_gpu_layers = config.get("n_gpu_layers", self.n_gpu_layers)
    #         self.n_ctx = config.get("n_ctx", self.n_ctx)
