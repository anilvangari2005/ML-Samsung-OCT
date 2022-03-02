# ML-Samsung-OCT
FourthBrain machine learning capstone project on Samsung OCT

## FlaskApp setup

Version requirements 
1. Python = 2.7.17
2. tensorflow = 2.4.3
3. h5py = 2.10.0
4. matplotlib = 3.3.4
5. Flask = 1.1.2

Download and place the model files at suggested location below
1. backend/FlaskApp/static/model/Optic_net-3-classes-Srinivasan2014.h5
2. backend/FlaskApp/static/model/Optic_net-4_classes-Kermany2018.hdf5

Install requirements

```bash
cd backend/FlaskApp/
pip install -r requirements.txt
```
Run Flask app

```bash
cd backend/
export FLASK_APP=FlaskApp
export FLASK_ENV=development
flask run
```