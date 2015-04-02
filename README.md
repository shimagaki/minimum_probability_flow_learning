# Minimum_probability_flow_learning
Python (Theano) implementation of Minimum Probability Flow learning code provided by Daniel Jiwoong Im.
The code includes minimum probability flow with one-bit flip and factored minimum probability flow.
For more information, see

```bibtex
@article{Im2015mpf,
  title={Understanding Minimum Probability Flow for RBMs Under Various Kinds of Dynamics},
  author={Im, Daniel Jiwoong and Buchman, Ethan and Taylor, Graham},
  journal={International Conference on Learning Representations (ICLR) Workshop Track},
  year={2015}
}
```

If you use this in your research, we kindly ask that you cite the above workshop paper

## Dependencies
Packages
* [numpy](http://www.numpy.org/)
* [Theano](http://deeplearning.net/software/theano/)
* [(Binarized) MNIST data](http://yann.lecun.com/exdb/mnist/)


## How to run
Entry code for one-bit flip and factored minimum probability flow for mnist data are 
```
    - mnist_1bit_mpf.py
    - mnist_fmpf.py
```

