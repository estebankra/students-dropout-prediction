import enum


class ValidModelVersionSortFields(enum.Enum):
    CREATED_AT = "created_at"
    VERSION = "version"
    NUM_SAMPLES = "num_samples"
    NUM_FEATURES = "num_features"
    ACCURACY = "accuracy"
    PRECISION = "precision"
    RECALL = "recall"
    F1_SCORE = "f1_score"


class ModelVersionStatus(enum.Enum):
    PENDING = "PENDING"
    TRAINING = "TRAINING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
