# TeleDeaf-Care

### Description

This is an API application built using Django REST Framework (DRF), which provides endpoints for various API functions. The system uses token-based authentication (JWT) to ensure security.

### Requirements

To run this application, you'll need:

- Python 3.10.11
- MySQL
- Additional dependencies are listed in requirements.txt.

### Installation

#### 1. Clone the repository

<pre>git clone https://github.com/DC8-AI/TeleDeaf-Care.git</pre>

#### 2. Install dependencies

<pre>pip install -r requirements.txt</pre>

#### 3. Set up the database

Set up a MySQL database:

<pre>CREATE DATABASE teledeafcare;</pre>

#### 4. Configure environment variables

Change configs to match with your local database

<pre>DB_NAME=teledeafcare
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=</pre>

#### 5. Run migrations

<pre>python manage.py migrate
</pre>

### Usage

#### 1. Run the server

<pre>python manage.py runserver
</pre>  

The API will be available at http://127.0.0.1:8000/.

### API document

https://docs.google.com/document/d/1sRB1Ho5VnbCmdY3Ao7GIKE7ndws0wevR1la6ZlnyVms/edit?usp=sharing

### Change model api
- Step 1: Copy the model file into the teledeaf-care-backend\src\export_model directory.
- Step 2: Open model_services.py and update the path to the new model file at MODEL_CONFIGS, corresponding to the API version that needs the model change.
- Step 3: Update the corresponding JSON file for that model (v1: sign_poc.json; v2: sign_poc_v2.json; v3: sign_poc_web.json).
- Step 4: Adjust the SEQ_LEN value to match the new model.

### Parameters Note
1. Change the second param of function process_data to 2 if use_semi_isolated was enable else 1
```
input_data = torch.unsqueeze(process_data(input_data, 2), dim=0).to(device)
```
2. Change parameters if train model changed to another param set
```
model = SiFormer(num_classes=len(label),
                      num_enc_layers=3, num_dec_layers=2, device=device,
                      IA_encoder=True, IA_decoder=False,
                      patience=1, cross_attn=True)
```

test grpc:
POST
http://127.0.0.1:8000/api/v5/api/sign-language/recognize?platform=web&language_code=vn

test rest:

body:
{
  "frames": [
    {
      "midEyes": [{"x": 0.484, "y": 0.354, "z": -0.008}],
      "leftHand": [
        {"x": 0.485, "y": 0.335, "z": -0.017},
        {"x": 0.484, "y": 0.341, "z": -0.008},
        {"x": 0.482, "y": 0.314, "z": -0.014},
        {"x": 0.486, "y": 0.329, "z": -0.018},
        {"x": 0.485, "y": 0.320, "z": -0.017},
        {"x": 0.484, "y": 0.300, "z": -0.009}
      ],
      "rightHand": [],
      "lip": []
    },
    {
      "midEyes": [{"x": 0.484, "y": 0.354, "z": -0.008}],
      "leftHand": [
        {"x": 0.485, "y": 0.335, "z": -0.017},
        {"x": 0.484, "y": 0.341, "z": -0.008},
        {"x": 0.482, "y": 0.314, "z": -0.014},
        {"x": 0.486, "y": 0.329, "z": -0.018},
        {"x": 0.485, "y": 0.320, "z": -0.017},
        {"x": 0.484, "y": 0.300, "z": -0.009}
      ],
      "rightHand": [],
      "lip": []
    },
    {
      "midEyes": [{"x": 0.484, "y": 0.354, "z": -0.008}],
      "leftHand": [
        {"x": 0.485, "y": 0.335, "z": -0.017},
        {"x": 0.484, "y": 0.341, "z": -0.008},
        {"x": 0.482, "y": 0.314, "z": -0.014},
        {"x": 0.486, "y": 0.329, "z": -0.018},
        {"x": 0.485, "y": 0.320, "z": -0.017},
        {"x": 0.484, "y": 0.300, "z": -0.009}
      ],
      "rightHand": [],
      "lip": []
    },
    {
      "midEyes": [{"x": 0.484, "y": 0.354, "z": -0.008}],
      "leftHand": [
        {"x": 0.485, "y": 0.335, "z": -0.017},
        {"x": 0.484, "y": 0.341, "z": -0.008},
        {"x": 0.482, "y": 0.314, "z": -0.014},
        {"x": 0.486, "y": 0.329, "z": -0.018},
        {"x": 0.485, "y": 0.320, "z": -0.017},
        {"x": 0.484, "y": 0.300, "z": -0.009}
      ],
      "rightHand": [],
      "lip": []
    },
    {
      "midEyes": [{"x": 0.484, "y": 0.354, "z": -0.008}],
      "leftHand": [
        {"x": 0.485, "y": 0.335, "z": -0.017},
        {"x": 0.484, "y": 0.341, "z": -0.008},
        {"x": 0.482, "y": 0.314, "z": -0.014},
        {"x": 0.486, "y": 0.329, "z": -0.018},
        {"x": 0.485, "y": 0.320, "z": -0.017},
        {"x": 0.484, "y": 0.300, "z": -0.009}
      ],
      "rightHand": [],
      "lip": []
    },
    {
      "midEyes": [{"x": 0.484, "y": 0.354, "z": -0.008}],
      "leftHand": [
        {"x": 0.485, "y": 0.335, "z": -0.017},
        {"x": 0.484, "y": 0.341, "z": -0.008},
        {"x": 0.482, "y": 0.314, "z": -0.014},
        {"x": 0.486, "y": 0.329, "z": -0.018},
        {"x": 0.485, "y": 0.320, "z": -0.017},
        {"x": 0.484, "y": 0.300, "z": -0.009}
      ],
      "rightHand": [],
      "lip": []
    },
    {
      "midEyes": [{"x": 0.484, "y": 0.354, "z": -0.008}],
      "leftHand": [
        {"x": 0.485, "y": 0.335, "z": -0.017},
        {"x": 0.484, "y": 0.341, "z": -0.008},
        {"x": 0.482, "y": 0.314, "z": -0.014},
        {"x": 0.486, "y": 0.329, "z": -0.018},
        {"x": 0.485, "y": 0.320, "z": -0.017},
        {"x": 0.484, "y": 0.300, "z": -0.009}
      ],
      "rightHand": [],
      "lip": []
    },
    {
      "midEyes": [{"x": 0.484, "y": 0.354, "z": -0.008}],
      "leftHand": [
        {"x": 0.485, "y": 0.335, "z": -0.017},
        {"x": 0.484, "y": 0.341, "z": -0.008},
        {"x": 0.482, "y": 0.314, "z": -0.014},
        {"x": 0.486, "y": 0.329, "z": -0.018},
        {"x": 0.485, "y": 0.320, "z": -0.017},
        {"x": 0.484, "y": 0.300, "z": -0.009}
      ],
      "rightHand": [],
      "lip": []
    },
    {
      "midEyes": [{"x": 0.484, "y": 0.354, "z": -0.008}],
      "leftHand": [
        {"x": 0.485, "y": 0.335, "z": -0.017},
        {"x": 0.484, "y": 0.341, "z": -0.008},
        {"x": 0.482, "y": 0.314, "z": -0.014},
        {"x": 0.486, "y": 0.329, "z": -0.018},
        {"x": 0.485, "y": 0.320, "z": -0.017},
        {"x": 0.484, "y": 0.300, "z": -0.009}
      ],
      "rightHand": [],
      "lip": []
    },
    {
      "midEyes": [{"x": 0.484, "y": 0.354, "z": -0.008}],
      "leftHand": [
        {"x": 0.485, "y": 0.335, "z": -0.017},
        {"x": 0.484, "y": 0.341, "z": -0.008},
        {"x": 0.482, "y": 0.314, "z": -0.014},
        {"x": 0.486, "y": 0.329, "z": -0.018},
        {"x": 0.485, "y": 0.320, "z": -0.017},
        {"x": 0.484, "y": 0.300, "z": -0.009}
      ],
      "rightHand": [],
      "lip": []
    }
  ],
  "previous_word": ""
}