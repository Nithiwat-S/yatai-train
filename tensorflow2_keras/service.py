
import bentoml
import numpy as np
from bentoml.io import Image, NumpyNdarray
from PIL.Image import Image as PILImage

mnist_runner = bentoml.tensorflow.get("u00_tensorflow_mnist:latest").to_runner()

svc = bentoml.Service(
    name="u00_tensorflow_mnist_demo",
    runners=[mnist_runner],
)

@svc.api(input=Image(), output=NumpyNdarray(dtype="float32"))
async def predict_image(f: PILImage) -> "np.ndarray":
    assert isinstance(f, PILImage)
    arr = np.array(f)/255.0
    assert arr.shape == (28, 28)

    # We are using greyscale image and our PyTorch model expect one
    # extra channel dimension
    arr = np.expand_dims(arr, (0, 3)).astype("float32") # reshape to [1, 28, 28, 1]
    return await mnist_runner.async_run(arr)
