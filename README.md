# ZPM
Zephy's Prompt Machine

![afbeelding](https://github.com/TheBarret/ZPM/assets/25234371/e687d601-2268-4dc4-a133-eecdaacff2c4)


My custom node works very basic, it can replace a `__file__` with any random entry of the filename (without extension).
It does however need a re-init trigger to make sure it will cycle through a new prompt, the way I do this is 
by laying down two modules where one is just a randomizer and then converts the number to a string for the trigger input.

ComfyUI Workflow preset:
```
{
  "last_node_id": 27,
  "last_link_id": 45,
  "nodes": [
    {
      "id": 3,
      "type": "LoadImageWithMetadata",
      "pos": [
        30,
        190
      ],
      "size": {
        "0": 320,
        "1": 460
      },
      "flags": {},
      "order": 0,
      "mode": 0,
      "outputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "links": [
            12
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "mask",
          "type": "MASK",
          "links": null,
          "shape": 3
        },
        {
          "name": "positive",
          "type": "STRING",
          "links": [],
          "shape": 3,
          "slot_index": 2
        },
        {
          "name": "negative",
          "type": "STRING",
          "links": [
            15
          ],
          "shape": 3,
          "slot_index": 3
        },
        {
          "name": "seed",
          "type": "INT",
          "links": null,
          "shape": 3
        },
        {
          "name": "width",
          "type": "INT",
          "links": null,
          "shape": 3
        },
        {
          "name": "height",
          "type": "INT",
          "links": null,
          "shape": 3
        },
        {
          "name": "cfg",
          "type": "FLOAT",
          "links": null,
          "shape": 3
        },
        {
          "name": "steps",
          "type": "INT",
          "links": null,
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "LoadImageWithMetadata"
      },
      "widgets_values": [
        "00236-3358215029.png",
        "image"
      ]
    },
    {
      "id": 2,
      "type": "CheckpointLoaderSimple",
      "pos": [
        30,
        50
      ],
      "size": {
        "0": 320,
        "1": 100
      },
      "flags": {},
      "order": 1,
      "mode": 0,
      "outputs": [
        {
          "name": "MODEL",
          "type": "MODEL",
          "links": [
            28
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "CLIP",
          "type": "CLIP",
          "links": [
            25
          ],
          "shape": 3,
          "slot_index": 1
        },
        {
          "name": "VAE",
          "type": "VAE",
          "links": [
            13
          ],
          "shape": 3,
          "slot_index": 2
        }
      ],
      "properties": {
        "Node name for S&R": "CheckpointLoaderSimple"
      },
      "widgets_values": [
        "mw4_crs15.ckpt"
      ]
    },
    {
      "id": 10,
      "type": "PreviewImage",
      "pos": [
        360,
        400
      ],
      "size": {
        "0": 260,
        "1": 250
      },
      "flags": {},
      "order": 16,
      "mode": 0,
      "inputs": [
        {
          "name": "images",
          "type": "IMAGE",
          "link": 10
        }
      ],
      "properties": {
        "Node name for S&R": "PreviewImage"
      }
    },
    {
      "id": 17,
      "type": "Number to String",
      "pos": [
        520,
        180
      ],
      "size": {
        "0": 210,
        "1": 26
      },
      "flags": {
        "collapsed": true
      },
      "order": 7,
      "mode": 0,
      "inputs": [
        {
          "name": "number",
          "type": "NUMBER",
          "link": 24
        }
      ],
      "outputs": [
        {
          "name": "STRING",
          "type": "STRING",
          "links": [
            23
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "title": "Signal",
      "properties": {
        "Node name for S&R": "Number to String"
      },
      "color": "#232",
      "bgcolor": "#353"
    },
    {
      "id": 16,
      "type": "Number Counter",
      "pos": [
        390,
        180
      ],
      "size": {
        "0": 315,
        "1": 194
      },
      "flags": {
        "collapsed": true
      },
      "order": 2,
      "mode": 0,
      "inputs": [
        {
          "name": "reset_bool",
          "type": "NUMBER",
          "link": null
        }
      ],
      "outputs": [
        {
          "name": "number",
          "type": "NUMBER",
          "links": [
            24
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "float",
          "type": "FLOAT",
          "links": null,
          "shape": 3
        },
        {
          "name": "int",
          "type": "INT",
          "links": null,
          "shape": 3
        }
      ],
      "title": "Counter",
      "properties": {
        "Node name for S&R": "Number Counter"
      },
      "widgets_values": [
        "integer",
        "increment",
        0,
        1024,
        1
      ],
      "color": "#232",
      "bgcolor": "#353"
    },
    {
      "id": 22,
      "type": "KSampler",
      "pos": [
        1270,
        50
      ],
      "size": [
        310,
        260
      ],
      "flags": {},
      "order": 14,
      "mode": 0,
      "inputs": [
        {
          "name": "model",
          "type": "MODEL",
          "link": 38
        },
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 40
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 41
        },
        {
          "name": "latent_image",
          "type": "LATENT",
          "link": 43
        }
      ],
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            39
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "KSampler"
      },
      "widgets_values": [
        786428309311991,
        "randomize",
        6,
        6,
        "dpmpp_sde_gpu",
        "normal",
        0.5
      ],
      "locked": true
    },
    {
      "id": 7,
      "type": "Text to Conditioning",
      "pos": [
        640,
        100
      ],
      "size": {
        "0": 210,
        "1": 54
      },
      "flags": {
        "collapsed": true
      },
      "order": 8,
      "mode": 0,
      "inputs": [
        {
          "name": "clip",
          "type": "CLIP",
          "link": 27
        },
        {
          "name": "text",
          "type": "STRING",
          "link": 16,
          "widget": {
            "name": "text"
          }
        }
      ],
      "outputs": [
        {
          "name": "CONDITIONING",
          "type": "CONDITIONING",
          "links": [
            8,
            41
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "Text to Conditioning"
      },
      "widgets_values": [
        ""
      ],
      "color": "#322",
      "bgcolor": "#533"
    },
    {
      "id": 5,
      "type": "Zephys",
      "pos": [
        640,
        170
      ],
      "size": [
        290,
        160
      ],
      "flags": {},
      "order": 9,
      "mode": 0,
      "inputs": [
        {
          "name": "trigger",
          "type": "STRING",
          "link": 23,
          "widget": {
            "name": "trigger"
          }
        }
      ],
      "outputs": [
        {
          "name": "STRING",
          "type": "STRING",
          "links": [
            20,
            30
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "STRING",
          "type": "STRING",
          "links": [],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "Zephys"
      },
      "widgets_values": [
        "__preamble__ zombie, drippy, bloody, fine details, micro details, filigree, __punks__ theme, cinematic lighting, (embedding:emb-rrf2:0.3)",
        "",
        ""
      ],
      "color": "#232",
      "bgcolor": "#353"
    },
    {
      "id": 4,
      "type": "KSampler",
      "pos": [
        950,
        50
      ],
      "size": [
        315,
        262
      ],
      "flags": {},
      "order": 12,
      "mode": 0,
      "inputs": [
        {
          "name": "model",
          "type": "MODEL",
          "link": 29
        },
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 4
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 8
        },
        {
          "name": "latent_image",
          "type": "LATENT",
          "link": 14
        }
      ],
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            42
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "KSampler"
      },
      "widgets_values": [
        719074690849216,
        "randomize",
        6,
        6,
        "dpmpp_sde_gpu",
        "normal",
        0.35000000000000003
      ],
      "locked": true
    },
    {
      "id": 25,
      "type": "LatentUpscaleBy",
      "pos": [
        1270,
        360
      ],
      "size": [
        310,
        80
      ],
      "flags": {},
      "order": 13,
      "mode": 0,
      "inputs": [
        {
          "name": "samples",
          "type": "LATENT",
          "link": 42
        }
      ],
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            43
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "LatentUpscaleBy"
      },
      "widgets_values": [
        "nearest-exact",
        1.3
      ]
    },
    {
      "id": 11,
      "type": "VAELoader",
      "pos": [
        950,
        360
      ],
      "size": [
        310,
        80
      ],
      "flags": {},
      "order": 3,
      "mode": 0,
      "outputs": [
        {
          "name": "VAE",
          "type": "VAE",
          "links": [
            11
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "VAELoader"
      },
      "widgets_values": [
        "Anything-V3.0.vae.safetensors"
      ]
    },
    {
      "id": 9,
      "type": "VAEDecodeTiled",
      "pos": [
        950,
        480
      ],
      "size": [
        310,
        80
      ],
      "flags": {
        "collapsed": false
      },
      "order": 15,
      "mode": 0,
      "inputs": [
        {
          "name": "samples",
          "type": "LATENT",
          "link": 39
        },
        {
          "name": "vae",
          "type": "VAE",
          "link": 11
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            10
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "VAEDecodeTiled"
      },
      "widgets_values": [
        512
      ]
    },
    {
      "id": 13,
      "type": "VAEEncodeTiled",
      "pos": [
        450,
        120
      ],
      "size": {
        "0": 315,
        "1": 78
      },
      "flags": {
        "collapsed": true
      },
      "order": 6,
      "mode": 0,
      "inputs": [
        {
          "name": "pixels",
          "type": "IMAGE",
          "link": 12
        },
        {
          "name": "vae",
          "type": "VAE",
          "link": 13
        }
      ],
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            14
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "VAEEncodeTiled"
      },
      "widgets_values": [
        512
      ]
    },
    {
      "id": 6,
      "type": "Text to Conditioning",
      "pos": [
        640,
        130
      ],
      "size": {
        "0": 210,
        "1": 54
      },
      "flags": {
        "collapsed": true
      },
      "order": 10,
      "mode": 0,
      "inputs": [
        {
          "name": "clip",
          "type": "CLIP",
          "link": 26
        },
        {
          "name": "text",
          "type": "STRING",
          "link": 20,
          "widget": {
            "name": "text"
          }
        }
      ],
      "outputs": [
        {
          "name": "CONDITIONING",
          "type": "CONDITIONING",
          "links": [
            4,
            40
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "Text to Conditioning"
      },
      "widgets_values": [
        ""
      ],
      "color": "#232",
      "bgcolor": "#353"
    },
    {
      "id": 14,
      "type": "EmbeddingPicker",
      "pos": [
        640,
        540
      ],
      "size": [
        290,
        110
      ],
      "flags": {
        "collapsed": false
      },
      "order": 4,
      "mode": 0,
      "inputs": [
        {
          "name": "text",
          "type": "STRING",
          "link": 15,
          "widget": {
            "name": "text"
          }
        }
      ],
      "outputs": [
        {
          "name": "text",
          "type": "STRING",
          "links": [
            16
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "title": "Negative",
      "properties": {
        "Node name for S&R": "EmbeddingPicker"
      },
      "widgets_values": [
        "easynegative.safetensors",
        1,
        true,
        ""
      ],
      "color": "#322",
      "bgcolor": "#533"
    },
    {
      "id": 19,
      "type": "ShowText|pysssss",
      "pos": [
        640,
        370
      ],
      "size": [
        290,
        130
      ],
      "flags": {},
      "order": 11,
      "mode": 0,
      "inputs": [
        {
          "name": "text",
          "type": "STRING",
          "link": 30,
          "widget": {
            "name": "text"
          }
        }
      ],
      "outputs": [
        {
          "name": "STRING",
          "type": "STRING",
          "links": null,
          "shape": 6
        }
      ],
      "title": "Debugger",
      "properties": {
        "Node name for S&R": "ShowText|pysssss"
      },
      "widgets_values": [
        "precisely rendered zombie, drippy, bloody, fine details, micro details, filigree, Nanopunk theme, cinematic lighting, (embedding:emb-rrf2:0.3)"
      ],
      "color": "#232",
      "bgcolor": "#353"
    },
    {
      "id": 18,
      "type": "LoraLoader",
      "pos": [
        360,
        230
      ],
      "size": {
        "0": 260,
        "1": 130
      },
      "flags": {},
      "order": 5,
      "mode": 0,
      "inputs": [
        {
          "name": "model",
          "type": "MODEL",
          "link": 28
        },
        {
          "name": "clip",
          "type": "CLIP",
          "link": 25
        }
      ],
      "outputs": [
        {
          "name": "MODEL",
          "type": "MODEL",
          "links": [
            29,
            38
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "CLIP",
          "type": "CLIP",
          "links": [
            26,
            27
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "title": "LoRA",
      "properties": {
        "Node name for S&R": "LoraLoader"
      },
      "widgets_values": [
        "BIOMECHA.safetensors",
        1.35,
        1.35
      ]
    }
  ],
  "links": [
    [
      4,
      6,
      0,
      4,
      1,
      "CONDITIONING"
    ],
    [
      8,
      7,
      0,
      4,
      2,
      "CONDITIONING"
    ],
    [
      10,
      9,
      0,
      10,
      0,
      "IMAGE"
    ],
    [
      11,
      11,
      0,
      9,
      1,
      "VAE"
    ],
    [
      12,
      3,
      0,
      13,
      0,
      "IMAGE"
    ],
    [
      13,
      2,
      2,
      13,
      1,
      "VAE"
    ],
    [
      14,
      13,
      0,
      4,
      3,
      "LATENT"
    ],
    [
      15,
      3,
      3,
      14,
      0,
      "STRING"
    ],
    [
      16,
      14,
      0,
      7,
      1,
      "STRING"
    ],
    [
      20,
      5,
      0,
      6,
      1,
      "STRING"
    ],
    [
      23,
      17,
      0,
      5,
      0,
      "STRING"
    ],
    [
      24,
      16,
      0,
      17,
      0,
      "NUMBER"
    ],
    [
      25,
      2,
      1,
      18,
      1,
      "CLIP"
    ],
    [
      26,
      18,
      1,
      6,
      0,
      "CLIP"
    ],
    [
      27,
      18,
      1,
      7,
      0,
      "CLIP"
    ],
    [
      28,
      2,
      0,
      18,
      0,
      "MODEL"
    ],
    [
      29,
      18,
      0,
      4,
      0,
      "MODEL"
    ],
    [
      30,
      5,
      0,
      19,
      0,
      "STRING"
    ],
    [
      38,
      18,
      0,
      22,
      0,
      "MODEL"
    ],
    [
      39,
      22,
      0,
      9,
      0,
      "LATENT"
    ],
    [
      40,
      6,
      0,
      22,
      1,
      "CONDITIONING"
    ],
    [
      41,
      7,
      0,
      22,
      2,
      "CONDITIONING"
    ],
    [
      42,
      4,
      0,
      25,
      0,
      "LATENT"
    ],
    [
      43,
      25,
      0,
      22,
      3,
      "LATENT"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {},
  "version": 0.4
}
```
