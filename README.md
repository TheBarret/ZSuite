# ZPM

![afbeelding](https://github.com/TheBarret/ZPM/assets/25234371/50782d68-e92a-465f-ac5b-91893218c0d2)


- 10-11-2023 - V1.0.0 Added Prompter
- 11-11-2023 - v2.0.0 Added Seed Modifier


ComfyUI Workflow preset (from screenshot):
```
{
  "last_node_id": 26,
  "last_link_id": 32,
  "nodes": [
    {
      "id": 1,
      "type": "CheckpointLoaderSimple",
      "pos": [
        20,
        50
      ],
      "size": [
        315,
        98
      ],
      "flags": {},
      "order": 0,
      "mode": 0,
      "outputs": [
        {
          "name": "MODEL",
          "type": "MODEL",
          "links": [
            1
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "CLIP",
          "type": "CLIP",
          "links": [
            2
          ],
          "shape": 3,
          "slot_index": 1
        },
        {
          "name": "VAE",
          "type": "VAE",
          "links": null,
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "CheckpointLoaderSimple"
      },
      "widgets_values": [
        "mw4_crs15.ckpt"
      ],
      "locked": true
    },
    {
      "id": 9,
      "type": "VAELoader",
      "pos": [
        420,
        -60
      ],
      "size": [
        310,
        60
      ],
      "flags": {},
      "order": 1,
      "mode": 0,
      "outputs": [
        {
          "name": "VAE",
          "type": "VAE",
          "links": [
            10,
            17
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
      ],
      "locked": true
    },
    {
      "id": 2,
      "type": "LoadImageWithMetadata",
      "pos": [
        20,
        190
      ],
      "size": [
        320,
        450
      ],
      "flags": {},
      "order": 2,
      "mode": 0,
      "outputs": [
        {
          "name": "image",
          "type": "IMAGE",
          "links": [
            9
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
          "links": [],
          "shape": 3,
          "slot_index": 3
        },
        {
          "name": "seed",
          "type": "INT",
          "links": [
            20
          ],
          "shape": 3,
          "slot_index": 4
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
        "00041-264446564.png",
        "image"
      ],
      "locked": true
    },
    {
      "id": 15,
      "type": "Reroute",
      "pos": [
        770,
        70
      ],
      "size": [
        75,
        26
      ],
      "flags": {},
      "order": 12,
      "mode": 0,
      "inputs": [
        {
          "name": "",
          "type": "*",
          "link": 22
        }
      ],
      "outputs": [
        {
          "name": "INT",
          "type": "INT",
          "links": [
            23
          ],
          "slot_index": 0
        }
      ],
      "properties": {
        "showOutputText": true,
        "horizontal": false
      }
    },
    {
      "id": 6,
      "type": "Text to Conditioning",
      "pos": [
        770,
        120
      ],
      "size": {
        "0": 210,
        "1": 54
      },
      "flags": {
        "collapsed": true
      },
      "order": 19,
      "mode": 0,
      "inputs": [
        {
          "name": "clip",
          "type": "CLIP",
          "link": 3
        },
        {
          "name": "text",
          "type": "STRING",
          "link": 5,
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
            7
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "title": "Conditioning",
      "properties": {
        "Node name for S&R": "Text to Conditioning"
      },
      "widgets_values": [
        ""
      ]
    },
    {
      "id": 7,
      "type": "Text to Conditioning",
      "pos": [
        800,
        140
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
          "link": 4
        },
        {
          "name": "text",
          "type": "STRING",
          "link": 6,
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
            8
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "title": "Conditioning",
      "properties": {
        "Node name for S&R": "Text to Conditioning"
      },
      "widgets_values": [
        ""
      ]
    },
    {
      "id": 19,
      "type": "Int to float",
      "pos": [
        750,
        630
      ],
      "size": {
        "0": 210,
        "1": 50
      },
      "flags": {
        "collapsed": true
      },
      "order": 13,
      "mode": 0,
      "inputs": [
        {
          "name": "Value",
          "type": "INT",
          "link": 24,
          "widget": {
            "name": "Value"
          }
        }
      ],
      "outputs": [
        {
          "name": "FLOAT",
          "type": "FLOAT",
          "links": [
            25
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "title": "Value",
      "properties": {
        "Node name for S&R": "Int to float"
      },
      "widgets_values": [
        1
      ]
    },
    {
      "id": 20,
      "type": "floatToText _O",
      "pos": [
        850,
        630
      ],
      "size": {
        "0": 210,
        "1": 50
      },
      "flags": {
        "collapsed": true
      },
      "order": 15,
      "mode": 0,
      "inputs": [
        {
          "name": "float",
          "type": "FLOAT",
          "link": 25,
          "widget": {
            "name": "float"
          }
        }
      ],
      "outputs": [
        {
          "name": "STRING",
          "type": "STRING",
          "links": [
            26
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "title": "String",
      "properties": {
        "Node name for S&R": "floatToText _O"
      },
      "widgets_values": [
        0
      ]
    },
    {
      "id": 21,
      "type": "ShowText|pysssss",
      "pos": [
        740,
        600
      ],
      "size": [
        220,
        110
      ],
      "flags": {},
      "order": 18,
      "mode": 0,
      "inputs": [
        {
          "name": "text",
          "type": "STRING",
          "link": 26,
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
      "title": "Seed",
      "properties": {
        "Node name for S&R": "ShowText|pysssss"
      },
      "widgets_values": [
        "1090458469.0"
      ],
      "color": "#223",
      "bgcolor": "#335",
      "locked": true
    },
    {
      "id": 10,
      "type": "VAEEncodeTiled",
      "pos": [
        770,
        170
      ],
      "size": {
        "0": 210,
        "1": 80
      },
      "flags": {
        "collapsed": true
      },
      "order": 7,
      "mode": 0,
      "inputs": [
        {
          "name": "pixels",
          "type": "IMAGE",
          "link": 9
        },
        {
          "name": "vae",
          "type": "VAE",
          "link": 10
        }
      ],
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            27
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
      "id": 22,
      "type": "LatentUpscaleBy",
      "pos": [
        770,
        200
      ],
      "size": {
        "0": 260,
        "1": 90
      },
      "flags": {
        "collapsed": true
      },
      "order": 11,
      "mode": 0,
      "inputs": [
        {
          "name": "samples",
          "type": "LATENT",
          "link": 27
        }
      ],
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            28
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "title": "Upscaler",
      "properties": {
        "Node name for S&R": "LatentUpscaleBy"
      },
      "widgets_values": [
        "nearest-exact",
        1.3
      ]
    },
    {
      "id": 13,
      "type": "PreviewImage",
      "pos": [
        970,
        450
      ],
      "size": [
        270,
        260
      ],
      "flags": {},
      "order": 22,
      "mode": 0,
      "inputs": [
        {
          "name": "images",
          "type": "IMAGE",
          "link": 19
        }
      ],
      "properties": {
        "Node name for S&R": "PreviewImage"
      },
      "locked": true
    },
    {
      "id": 8,
      "type": "KSampler",
      "pos": [
        970,
        50
      ],
      "size": [
        280,
        260
      ],
      "flags": {},
      "order": 20,
      "mode": 0,
      "inputs": [
        {
          "name": "model",
          "type": "MODEL",
          "link": 12
        },
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 7
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 8
        },
        {
          "name": "latent_image",
          "type": "LATENT",
          "link": 28
        },
        {
          "name": "seed",
          "type": "INT",
          "link": 23,
          "widget": {
            "name": "seed"
          }
        }
      ],
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            15
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "KSampler"
      },
      "widgets_values": [
        998684823200100,
        "randomize",
        6,
        6,
        "dpmpp_sde_gpu",
        "normal",
        0.45
      ],
      "locked": true
    },
    {
      "id": 12,
      "type": "Reroute",
      "pos": [
        770,
        310
      ],
      "size": [
        75,
        26
      ],
      "flags": {},
      "order": 6,
      "mode": 0,
      "inputs": [
        {
          "name": "",
          "type": "*",
          "link": 17
        }
      ],
      "outputs": [
        {
          "name": "VAE",
          "type": "VAE",
          "links": [
            18
          ],
          "slot_index": 0
        }
      ],
      "properties": {
        "showOutputText": true,
        "horizontal": false
      }
    },
    {
      "id": 11,
      "type": "VAEDecodeTiled",
      "pos": [
        850,
        340
      ],
      "size": {
        "0": 280,
        "1": 80
      },
      "flags": {
        "collapsed": true
      },
      "order": 21,
      "mode": 0,
      "inputs": [
        {
          "name": "samples",
          "type": "LATENT",
          "link": 15
        },
        {
          "name": "vae",
          "type": "VAE",
          "link": 18
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            19
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
      "id": 5,
      "type": "EmbeddingPicker",
      "pos": [
        420,
        410
      ],
      "size": [
        310,
        150
      ],
      "flags": {},
      "order": 3,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {
          "name": "text",
          "type": "STRING",
          "links": [
            6
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
        "ng_deepnegative_v1_75t.pt",
        1,
        true,
        "embedding:easynegative"
      ],
      "color": "#322",
      "bgcolor": "#533",
      "locked": true
    },
    {
      "id": 25,
      "type": "Number to Text",
      "pos": [
        250,
        680
      ],
      "size": {
        "0": 140,
        "1": 30
      },
      "flags": {
        "collapsed": true
      },
      "order": 9,
      "mode": 0,
      "inputs": [
        {
          "name": "number",
          "type": "NUMBER",
          "link": 29
        }
      ],
      "outputs": [
        {
          "name": "STRING",
          "type": "STRING",
          "links": [
            30
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "title": "Signal",
      "properties": {
        "Node name for S&R": "Number to Text"
      },
      "color": "#223",
      "bgcolor": "#335"
    },
    {
      "id": 24,
      "type": "Number Counter",
      "pos": [
        120,
        680
      ],
      "size": {
        "0": 210,
        "1": 194
      },
      "flags": {
        "collapsed": true
      },
      "order": 4,
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
            29
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "float",
          "type": "FLOAT",
          "links": null,
          "shape": 3,
          "slot_index": 1
        },
        {
          "name": "int",
          "type": "INT",
          "links": null,
          "shape": 3,
          "slot_index": 2
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
        2048,
        1
      ],
      "color": "#223",
      "bgcolor": "#335"
    },
    {
      "id": 23,
      "type": "ZSUITE_PROMPTER",
      "pos": [
        420,
        750
      ],
      "size": [
        310,
        120
      ],
      "flags": {},
      "order": 14,
      "mode": 0,
      "inputs": [
        {
          "name": "trigger",
          "type": "STRING",
          "link": 30,
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
            31,
            32
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "ZSUITE_PROMPTER"
      },
      "widgets_values": [
        "__preamble__ minotaur zombie inspired by __artist__, (embedding:dishonored-portrait-styles:0.7), (embedding:emb-rrf2:0.7)",
        ""
      ],
      "color": "#223",
      "bgcolor": "#335",
      "locked": true
    },
    {
      "id": 26,
      "type": "ShowText|pysssss",
      "pos": [
        740,
        750
      ],
      "size": [
        220,
        120
      ],
      "flags": {},
      "order": 17,
      "mode": 0,
      "inputs": [
        {
          "name": "text",
          "type": "STRING",
          "link": 32,
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
      "title": "Wildcard",
      "properties": {
        "Node name for S&R": "ShowText|pysssss"
      },
      "widgets_values": [
        "faithfully depicted minotaur android inspired by Aaron Horkey, (embedding:dishonored-portrait-styles:0.7), (embedding:emb-rrf2:0.7)"
      ],
      "color": "#223",
      "bgcolor": "#335",
      "locked": true
    },
    {
      "id": 4,
      "type": "EmbeddingPicker",
      "pos": [
        420,
        220
      ],
      "size": [
        310,
        150
      ],
      "flags": {},
      "order": 16,
      "mode": 0,
      "inputs": [
        {
          "name": "text",
          "type": "STRING",
          "link": 31,
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
            5
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "EmbeddingPicker"
      },
      "widgets_values": [
        "illustration-style.pt",
        1,
        true,
        ""
      ],
      "color": "#232",
      "bgcolor": "#353",
      "locked": true
    },
    {
      "id": 3,
      "type": "LoraLoader",
      "pos": [
        420,
        50
      ],
      "size": [
        315,
        126
      ],
      "flags": {},
      "order": 5,
      "mode": 0,
      "inputs": [
        {
          "name": "model",
          "type": "MODEL",
          "link": 1
        },
        {
          "name": "clip",
          "type": "CLIP",
          "link": 2
        }
      ],
      "outputs": [
        {
          "name": "MODEL",
          "type": "MODEL",
          "links": [
            12
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "CLIP",
          "type": "CLIP",
          "links": [
            3,
            4
          ],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "LoraLoader"
      },
      "widgets_values": [
        "steampunkai.safetensors",
        1.33,
        1.33
      ],
      "locked": true
    },
    {
      "id": 14,
      "type": "ZSUITE_SEED_MODIFIER",
      "pos": [
        420,
        600
      ],
      "size": [
        310,
        110
      ],
      "flags": {},
      "order": 8,
      "mode": 0,
      "inputs": [
        {
          "name": "seed",
          "type": "INT",
          "link": 20,
          "widget": {
            "name": "seed"
          }
        }
      ],
      "outputs": [
        {
          "name": "INT",
          "type": "INT",
          "links": [
            22,
            24
          ],
          "shape": 3,
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "ZSUITE_SEED_MODIFIER"
      },
      "widgets_values": [
        1921,
        "randomize",
        0.1
      ],
      "color": "#223",
      "bgcolor": "#335",
      "locked": true
    }
  ],
  "links": [
    [
      1,
      1,
      0,
      3,
      0,
      "MODEL"
    ],
    [
      2,
      1,
      1,
      3,
      1,
      "CLIP"
    ],
    [
      3,
      3,
      1,
      6,
      0,
      "CLIP"
    ],
    [
      4,
      3,
      1,
      7,
      0,
      "CLIP"
    ],
    [
      5,
      4,
      0,
      6,
      1,
      "STRING"
    ],
    [
      6,
      5,
      0,
      7,
      1,
      "STRING"
    ],
    [
      7,
      6,
      0,
      8,
      1,
      "CONDITIONING"
    ],
    [
      8,
      7,
      0,
      8,
      2,
      "CONDITIONING"
    ],
    [
      9,
      2,
      0,
      10,
      0,
      "IMAGE"
    ],
    [
      10,
      9,
      0,
      10,
      1,
      "VAE"
    ],
    [
      12,
      3,
      0,
      8,
      0,
      "MODEL"
    ],
    [
      15,
      8,
      0,
      11,
      0,
      "LATENT"
    ],
    [
      17,
      9,
      0,
      12,
      0,
      "*"
    ],
    [
      18,
      12,
      0,
      11,
      1,
      "VAE"
    ],
    [
      19,
      11,
      0,
      13,
      0,
      "IMAGE"
    ],
    [
      20,
      2,
      4,
      14,
      0,
      "INT"
    ],
    [
      22,
      14,
      0,
      15,
      0,
      "*"
    ],
    [
      23,
      15,
      0,
      8,
      4,
      "INT"
    ],
    [
      24,
      14,
      0,
      19,
      0,
      "INT"
    ],
    [
      25,
      19,
      0,
      20,
      0,
      "FLOAT"
    ],
    [
      26,
      20,
      0,
      21,
      0,
      "STRING"
    ],
    [
      27,
      10,
      0,
      22,
      0,
      "LATENT"
    ],
    [
      28,
      22,
      0,
      8,
      3,
      "LATENT"
    ],
    [
      29,
      24,
      0,
      25,
      0,
      "NUMBER"
    ],
    [
      30,
      25,
      0,
      23,
      0,
      "STRING"
    ],
    [
      31,
      23,
      0,
      4,
      0,
      "STRING"
    ],
    [
      32,
      23,
      0,
      26,
      0,
      "STRING"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {},
  "version": 0.4
}
```
