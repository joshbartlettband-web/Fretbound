# Shared tone fix for Gemini art (it comes out flat with yellowed whites): contrast about the image's own mean brightness, then the whites
# (bright, near-neutral pixels) lifted, fading in with brightness and out with saturation so coloured paint is left alone.
# usage: from arttone import tone; rgb=tone(rgb_uint8_array, mask=opaque_bool, contrast=1.10, whites=1.10)
import numpy as np
def tone(rgb,mask=None,contrast=1.10,whites=1.10):
    a=rgb.astype(float); L=a@[0.299,0.587,0.114]; m=L[mask].mean() if mask is not None and mask.any() else L.mean()
    a=(a-m)*contrast+m
    L=a@[0.299,0.587,0.114]; sat=(a.max(2)-a.min(2))/np.maximum(1,a.max(2))
    w=np.clip((L-140)/60,0,1)*np.clip(1-(sat-0.2)/0.25,0,1)
    a=a*(1+(whites-1)*w[...,None])
    return np.clip(a,0,255).astype(np.uint8)
