"""
Phase 1: Convert faceage_model.h5 (Keras/TF) to ONNX format.

The .h5 file was saved with Python 3.6 + TF 2.6. Its Lambda layers contain
marshaled Python 3.6 bytecode that cannot be deserialized by Python >= 3.11.

This script works around the issue by:
  1. Rebuilding the architecture using keras-facenet (which creates fresh
     Lambda layers compatible with the current Python)
  2. Loading weights from the .h5 file by layer name
  3. Converting to ONNX via tf2onnx

Usage:
    pip install tensorflow tf2onnx onnx onnxruntime keras-facenet opencv-python-headless h5py
    python scripts/convert_h5_to_onnx.py
"""

import os
import sys

import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import h5py
import tensorflow as tf
import tf2onnx

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
H5_PATH = os.path.join(MODEL_DIR, "faceage_model.h5")
ONNX_PATH = os.path.join(MODEL_DIR, "faceage_model.onnx")


def build_faceage_model():
    """Reconstruct the FaceAge model architecture:
    Sequential([InceptionResNetV1(128), Dense(128,relu), BatchNorm, Dense(1,linear)])
    """
    from keras_facenet.inception_resnet_v1 import InceptionResNetV1

    base = InceptionResNetV1(input_shape=(160, 160, 3), classes=128)

    model = tf.keras.Sequential(
        [
            base,
            tf.keras.layers.Dense(128, activation="relu", name="dense_1"),
            tf.keras.layers.BatchNormalization(
                momentum=0.995,
                epsilon=0.001,
                scale=False,
                name="classifier_1_BatchNorm",
            ),
            tf.keras.layers.Dense(1, activation="linear", name="dense_2"),
        ],
        name="sequential_1",
    )
    model.build(input_shape=(None, 160, 160, 3))
    return model


def _set_layer_weights(layer, layer_group):
    """Load weights for a single layer from its h5 group."""
    # Navigate: group/layer_name/weight_datasets
    if layer.name in layer_group:
        layer_group = layer_group[layer.name]

    datasets = {}
    layer_group.visititems(
        lambda n, obj: datasets.update({n: obj[()]}) if isinstance(obj, h5py.Dataset) else None
    )
    if not datasets:
        return False
    if len(datasets) != len(layer.weights):
        return False

    # Match by shape
    weight_values = []
    used = set()
    for w in layer.weights:
        target_shape = tuple(w.shape)
        for dn, arr in datasets.items():
            if dn not in used and arr.shape == target_shape:
                weight_values.append(arr)
                used.add(dn)
                break
        else:
            return False

    layer.set_weights(weight_values)
    return True


def load_weights_from_h5(model, h5_path):
    """Load weights from legacy .h5 matching the nested group structure:
    model_weights/inception_resnet_v1/{layer_name}/...
    model_weights/{dense_1, classifier_1_BatchNorm, dense_2}/...
    """
    with h5py.File(h5_path, "r") as f:
        wg = f["model_weights"]
        loaded = 0
        failed = []

        # Load base InceptionResNet weights
        base_model = model.layers[0]  # The InceptionResNetV1
        irv1_group = wg["inception_resnet_v1"]

        for layer in base_model.layers:
            if not layer.weights:
                continue
            if layer.name in irv1_group:
                if _set_layer_weights(layer, irv1_group[layer.name]):
                    loaded += 1
                else:
                    failed.append(layer.name)
            else:
                failed.append(layer.name)

        # Load top-level Sequential layers (dense_1, batchnorm, dense_2)
        for layer in model.layers[1:]:
            if not layer.weights:
                continue
            if layer.name in wg:
                if _set_layer_weights(layer, wg[layer.name]):
                    loaded += 1
                else:
                    failed.append(layer.name)
            else:
                failed.append(layer.name)

        print(f"  Loaded weights for {loaded} layers")
        if failed:
            print(f"  WARNING: Failed to load {len(failed)} layers: {failed[:5]}...")


def main():
    if not os.path.isfile(H5_PATH):
        sys.exit(
            f"ERROR: {H5_PATH} not found.\n"
            "Download it from the GitHub releases page and place it in models/."
        )

    # Step 1: Build architecture
    print("Building model architecture ...")
    model = build_faceage_model()
    print(f"  Total parameters: {model.count_params():,}")

    # Step 2: Load weights
    print(f"Loading weights from {H5_PATH} ...")
    load_weights_from_h5(model, H5_PATH)

    # Step 3: Get a concrete function for tf2onnx
    print("Converting to ONNX (this may take a minute) ...")

    # Save as TF SavedModel format, then convert via tf2onnx CLI
    import shutil
    import subprocess

    saved_model_dir = os.path.join(MODEL_DIR, "_saved_model_tmp")
    if os.path.exists(saved_model_dir):
        shutil.rmtree(saved_model_dir)

    # Use tf.saved_model.save for compatibility with tf2onnx
    tf.saved_model.save(model, saved_model_dir)

    print("Running tf2onnx conversion from SavedModel ...")
    result = subprocess.run(
        [
            sys.executable, "-m", "tf2onnx.convert",
            "--saved-model", saved_model_dir,
            "--output", ONNX_PATH,
            "--opset", "13",
        ],
        capture_output=True, text=True,
        timeout=300,
    )
    print(result.stderr[-2000:] if result.stderr else "")
    if result.returncode != 0:
        sys.exit(f"tf2onnx conversion failed with code {result.returncode}")

    # Clean up temp SavedModel
    shutil.rmtree(saved_model_dir, ignore_errors=True)
    print(f"ONNX model saved to {ONNX_PATH}")

    # Step 4: Sanity check
    import onnxruntime as ort

    sess = ort.InferenceSession(ONNX_PATH)
    dummy = np.random.randn(1, 160, 160, 3).astype(np.float32)
    result = sess.run(None, {sess.get_inputs()[0].name: dummy})
    print(f"Sanity check — dummy prediction: {result[0]}")
    print("Conversion complete!")


if __name__ == "__main__":
    main()
