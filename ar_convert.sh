#!/bin/sh
docker exec fbx2ar mkdir $1_out
docker exec fbx2ar fbx2gltf -b /$1.fbx --output /$1_out/$1.glb
docker exec fbx2ar usd_from_gltf /$1_out/box.glb /$1_out/$1.usdz
docker cp fbx2ar:$1_out/$1.usdz /Users/keenangray/Downloads/
