---
layout: post
title:  "Conditional generative models for inverse problems"
date:   2019-07-09
desc: "Inverse problems with conditional generative models"
keywords: "inverse problems conditional generative models"
categories: [Machine Learning]
tags: [GAN,VAE, generative models, inverse problems, neural networks, machine learning]
icon: inverse-icon.png
---
<div class="blog_text">
For my research, I need to be able to create complicated light patterns in my holographic optical tweezer setup (see e.g. Dynamic holographic optical tweezers, Curtis et al, 2002). My setup features a so-called spatial light modulator (SLM), essentially a liquid crystal screen with 800x600 pixels. Each pixel can advance or delay the phase of the incoming laser beam. In theory, this should allow me to shape the beam in any way I want. In practice, I need to know which value I should assign to each pixel of this SLM to create that particular beam shape.<br><br>

Mathematically speaking, the SLM-transformation I wish to train my network on is a non-linear matrix-to-matrix problem. My images are intensity only, so no additional colour channels. The transformation that the SLM imparts on the beam can be formally written down in an approximative form. However, the ensueing equations governing the intensity that the camera perceives cannot be solved for the SLM pattern in many cases.<br> <br>

That is not a simple problem. In fact, its non-trivial enough, that there are mountains of literature about it (there always are).<br><br>

I thought that deep learning might be one way to solve this problem. <br><br>

The following pictures should give you an impression of the transformation. You see pictures of the hologram with lots of striped patterns (left) and pictures of the corresponding laser light intensity fields (right). I am interested in creating a model which takes me from the intensity on the right to the SLM pattern on the left, so in the inverse direction.<br>

<div class="blog_img">
    <!-- ![edit]({{ site.img_path }}/inverseProblems/cVAEholo.gif) -->
    <img src="{{ site.img_path }}/inverseProblems/holo_to_intensity.png">
</div>
The grayscale of the SLM patterns on the left encode the phase shift that each pixel of the SLM imparts on the beam. The colorised pattern on the right shows the intensity distribution that the CMOS camera in my setup perceives. <br>

<i> More coming soon... </i>

Below you find a first glimpse of hologram-predictions made by my model.<br>
<div class="blog_img">
    <!-- ![edit]({{ site.img_path }}/inverseProblems/cVAEholo.gif) -->
    <img src="{{ site.img_path }}/inverseProblems/cVAEholo.gif">
</div>
</div>